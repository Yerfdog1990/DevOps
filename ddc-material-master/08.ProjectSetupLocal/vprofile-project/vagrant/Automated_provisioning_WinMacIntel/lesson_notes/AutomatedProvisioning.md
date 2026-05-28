# Automated Provisioning

## Overview

The manual setup required logging into each VM individually and executing commands one by one. Automated provisioning eliminates all of that. Vagrant's built-in **shell provisioner** is used to automatically run a shell script on each VM the moment it is created — so the entire five-VM stack is set up with a single command from the host machine.

This is the same stack, the same services, and the same configuration as the manual setup. The difference is that every setup step is encoded into shell scripts that run without any manual intervention.

---

## How It Works

The key addition to the `Vagrantfile` is one line per VM:

```ruby
db01.vm.provision "shell", path: "mysql.sh"
```

This tells Vagrant: *when this VM boots for the first time, run the shell script at this path inside the VM.* Each VM has its own dedicated script in the same folder as the `Vagrantfile`.

### The Automated Vagrantfile

```ruby
Vagrant.configure("2") do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true

  ### DB vm ####
  config.vm.define "db01" do |db01|
    db01.vm.box = "centos/stream9"
    db01.vm.hostname = "db01"
    db01.vm.network "private_network", ip: "192.168.56.15"
    db01.vm.provider "virtualbox" do |vb|
      vb.memory = "600"
    end
    db01.vm.provision "shell", path: "mysql.sh"
  end

  ### Memcache vm ####
  config.vm.define "mc01" do |mc01|
    mc01.vm.box = "centos/stream9"
    mc01.vm.hostname = "mc01"
    mc01.vm.network "private_network", ip: "192.168.56.14"
    mc01.vm.provider "virtualbox" do |vb|
      vb.memory = "600"
    end
    mc01.vm.provision "shell", path: "memcache.sh"
  end

  ### RabbitMQ vm ####
  config.vm.define "rmq01" do |rmq01|
    rmq01.vm.box = "centos/stream9"
    rmq01.vm.hostname = "rmq01"
    rmq01.vm.network "private_network", ip: "192.168.56.16"
    rmq01.vm.provider "virtualbox" do |vb|
      vb.memory = "600"
    end
    rmq01.vm.provision "shell", path: "rabbitmq.sh"
  end

  ### Tomcat vm ###
  config.vm.define "app01" do |app01|
    app01.vm.box = "centos/stream9"
    app01.vm.hostname = "app01"
    app01.vm.network "private_network", ip: "192.168.56.12"
    app01.vm.provision "shell", path: "tomcat.sh"
    app01.vm.provider "virtualbox" do |vb|
      vb.memory = "800"
    end
  end

  ### Nginx VM ###
  config.vm.define "web01" do |web01|
    web01.vm.box = "ubuntu/jammy64"
    web01.vm.hostname = "web01"
    web01.vm.network "private_network", ip: "192.168.56.11"
    web01.vm.provider "virtualbox" do |vb|
      vb.memory = "800"
    end
    web01.vm.provision "shell", path: "nginx.sh"
  end

end
```

### VM and Script Map

| VM | IP Address | OS | Script |
|----|------------|-----|--------|
| `db01` | `192.168.56.15` | CentOS Stream 9 | `mysql.sh` |
| `mc01` | `192.168.56.14` | CentOS Stream 9 | `memcache.sh` |
| `rmq01` | `192.168.56.16` | CentOS Stream 9 | `rabbitmq.sh` |
| `app01` | `192.168.56.12` | CentOS Stream 9 | `tomcat.sh` |
| `web01` | `192.168.56.11` | Ubuntu Jammy 64 | `nginx.sh` |

> Note: In the automated setup, `rmq01` uses IP `192.168.56.16` (not `.13` as in the manual setup). Always refer to the Vagrantfile in the folder you are using.

---

## Shell Script Basics

Each script begins with:

```bash
#!/bin/bash
```

This is called a **shebang**. It tells the system to open a Bash shell interpreter and run all the commands in the file through it — the same shell you use interactively.

Two techniques used in scripts that differ from manual setup:

**Variables** — used to avoid repeating values like the database password:

```bash
DATABASE_PASS='admin123'
```

Then referenced as `$DATABASE_PASS` wherever needed.

**Here Document (`cat <<EOT`)** — used to create multi-line files from within a script, since you cannot use `vi` or copy-paste in a non-interactive shell:

```bash
cat <<EOT > /path/to/file
line 1
line 2
EOT
```

Everything between `<<EOT` and the closing `EOT` is written into the file. This is how the Tomcat systemd service file and Nginx configuration are created in the automated scripts.

---

## The Scripts

### `mysql.sh` — Database Setup (db01)

```bash
#!/bin/bash
DATABASE_PASS='admin123'
sudo yum update -y
sudo yum install epel-release -y
sudo yum install git zip unzip -y
sudo yum install mariadb-server -y

sudo systemctl start mariadb
sudo systemctl enable mariadb

cd /tmp/
git clone -b main https://github.com/hkhcoder/vprofile-project.git

sudo mysqladmin -u root password "$DATABASE_PASS"
sudo mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
sudo mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.user WHERE User=''"
sudo mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%'"
sudo mysql -u root -p"$DATABASE_PASS" -e "FLUSH PRIVILEGES"
sudo mysql -u root -p"$DATABASE_PASS" -e "create database accounts"
sudo mysql -u root -p"$DATABASE_PASS" -e "grant all privileges on accounts.* TO 'admin'@'localhost' identified by 'admin123'"
sudo mysql -u root -p"$DATABASE_PASS" -e "grant all privileges on accounts.* TO 'admin'@'%' identified by 'admin123'"
sudo mysql -u root -p"$DATABASE_PASS" accounts < /tmp/vprofile-project/src/main/resources/db_backup.sql
sudo mysql -u root -p"$DATABASE_PASS" -e "FLUSH PRIVILEGES"

sudo systemctl restart mariadb

sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --zone=public --add-port=3306/tcp --permanent
sudo firewall-cmd --reload
sudo systemctl restart mariadb
```

**Key differences from manual setup:**

- All MySQL commands are run directly from the shell using `mysql -u root -p"$PASSWORD" -e "SQL QUERY"` — no interactive MySQL prompt
- The DB dump is imported from a path inside the cloned repo: `/tmp/vprofile-project/src/main/resources/db_backup.sql`
- The admin user is granted access from `'%'` (any host) rather than just `'app01'`, which is a broader grant suitable for automated environments
- Firewall rules are included and applied automatically

---

### `memcache.sh` — Memcached Setup (mc01)

```bash
#!/bin/bash
sudo dnf install epel-release -y
sudo dnf install memcached -y
sudo systemctl start memcached
sudo systemctl enable memcached
sudo systemctl status memcached
sed -i 's/127.0.0.1/0.0.0.0/g' /etc/sysconfig/memcached
sudo systemctl restart memcached
firewall-cmd --add-port=11211/tcp
firewall-cmd --runtime-to-permanent
firewall-cmd --add-port=11111/udp
firewall-cmd --runtime-to-permanent
sudo memcached -p 11211 -U 11111 -u memcached -d
```

The same steps as the manual setup encoded directly into a script. The `sed` command replaces the bind address, and firewall ports are opened automatically.

---

### `rabbitmq.sh` — RabbitMQ Setup (rmq01)

```bash
#!/bin/bash
sudo yum install epel-release -y
sudo yum update -y
sudo yum install wget -y
cd /tmp/
dnf -y install centos-release-rabbitmq-38
dnf --enablerepo=centos-rabbitmq-38 -y install rabbitmq-server
systemctl enable --now rabbitmq-server
firewall-cmd --add-port=5672/tcp
firewall-cmd --runtime-to-permanent
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl status rabbitmq-server
sudo sh -c 'echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config'
sudo rabbitmqctl add_user test test
sudo rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
sudo systemctl restart rabbitmq-server
```

Identical to the manual setup commands, automated in sequence. User creation, permissions, and config file generation all happen without intervention.

---

### `tomcat.sh` — Tomcat + Application Build & Deploy (app01)

This is the most complex script. It handles Tomcat installation, the Maven build, and application deployment in one pass.

```bash
#!/bin/bash
TOMURL="https://archive.apache.org/dist/tomcat/tomcat-10/v10.1.26/bin/apache-tomcat-10.1.26.tar.gz"
dnf -y install java-17-openjdk java-17-openjdk-devel
dnf install git wget unzip zip -y
cd /tmp/
wget $TOMURL -O tomcatbin.tar.gz
EXTOUT=`tar xzvf tomcatbin.tar.gz`
TOMDIR=`echo $EXTOUT | cut -d '/' -f1`
useradd --shell /sbin/nologin tomcat
rsync -avzh /tmp/$TOMDIR/ /usr/local/tomcat/
chown -R tomcat.tomcat /usr/local/tomcat

rm -rf /etc/systemd/system/tomcat.service

cat <<EOT>> /etc/systemd/system/tomcat.service
[Unit]
Description=Tomcat
After=network.target

[Service]
User=tomcat
Group=tomcat
WorkingDirectory=/usr/local/tomcat
Environment=JAVA_HOME=/usr/lib/jvm/jre
Environment=CATALINA_PID=/var/tomcat/%i/run/tomcat.pid
Environment=CATALINA_HOME=/usr/local/tomcat
Environment=CATALINE_BASE=/usr/local/tomcat
ExecStart=/usr/local/tomcat/bin/catalina.sh run
ExecStop=/usr/local/tomcat/bin/shutdown.sh
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl start tomcat
systemctl enable tomcat

cd /tmp/
wget https://archive.apache.org/dist/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.zip
unzip apache-maven-3.9.9-bin.zip
cp -r apache-maven-3.9.9 /usr/local/maven3.9
export MAVEN_OPTS="-Xmx512m"

git clone -b local https://github.com/hkhcoder/vprofile-project.git
cd vprofile-project
/usr/local/maven3.9/bin/mvn install
systemctl stop tomcat
sleep 20
rm -rf /usr/local/tomcat/webapps/ROOT*
cp target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
systemctl start tomcat
sleep 20
systemctl stop firewalld
systemctl disable firewalld
systemctl restart tomcat
```

**Notable script techniques:**

- `TOMURL` variable stores the download URL so it only needs to be defined once
- `` EXTOUT=`tar xzvf tomcatbin.tar.gz` `` — captures the tar output in a variable
- `` TOMDIR=`echo $EXTOUT | cut -d '/' -f1` `` — extracts the folder name from the output dynamically, so the script works even if the version number changes
- `cat <<EOT>>` — writes the entire systemd service file in place without needing a text editor
- `sleep 20` — pauses between stopping/starting Tomcat to give it time to fully shut down before the WAR is swapped
- The firewall is **disabled** on `app01` since Nginx (on `web01`) handles external traffic; Tomcat only needs to be reachable from `web01` within the private network
- Maven is downloaded from the Apache archive URL; if this fails in your environment, refer to the Maven download troubleshooting section in the Code Build & Deploy notes

---

### `nginx.sh` — Nginx Setup (web01)

```bash
apt update
apt install nginx -y
cat <<EOT > vproapp
upstream vproapp {
  server app01:8080;
}

server {
  listen 80;
  location / {
    proxy_pass http://vproapp;
  }
}
EOT

mv vproapp /etc/nginx/sites-available/vproapp
rm -rf /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/vproapp /etc/nginx/sites-enabled/vproapp

systemctl start nginx
systemctl enable nginx
systemctl restart nginx
```

The Nginx config is written using `cat <<EOT` into a temporary file `vproapp`, then moved to the correct location with `mv`. This is equivalent to creating the file manually with `vi`.

---

## The `application.properties` File

In automated provisioning, the `application.properties` file is included in the repository and baked into the WAR at build time by Maven. Its contents define all backend connection settings:

```properties
# JDBC Configuration for Database Connection
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://db01:3306/accounts?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull
jdbc.username=admin
jdbc.password=admin123

# Memcached Configuration — Active and Standby Host
# For Active Host
memcached.active.host=mc01
memcached.active.port=11211
# For Standby Host
memcached.standBy.host=127.0.0.2
memcached.standBy.port=11211

# RabbitMQ Configuration
rabbitmq.address=rmq01
rabbitmq.port=5672
rabbitmq.username=test
rabbitmq.password=test

# Elasticsearch Configuration
elasticsearch.host=192.168.1.85
elasticsearch.port=9300
elasticsearch.cluster=vprofile
elasticsearch.node=vprofilenode
```

All hostnames (`db01`, `mc01`, `rmq01`) are resolved via the `/etc/hosts` entries managed automatically by the `hostmanager` plugin in the Vagrantfile. No manual `/etc/hosts` edits are needed in the automated setup.

---

## Bringing Up the Stack

Open Git Bash (or your terminal), navigate to the automated provisioning folder — the one containing the `Vagrantfile` and all `.sh` scripts — and run:

```bash
vagrant up
```

### What Happens During `vagrant up`

Vagrant provisions each VM **sequentially**, in the order they are defined in the `Vagrantfile`. You do not need to do anything during this process — just wait.

The order and rough behaviour:

1. **db01** — VM boots, Vagrant waits for it to stabilise, then runs `mysql.sh`. This includes a `yum update` and cloning the source code, so it takes a few minutes.
2. **mc01** — boots and runs `memcache.sh`.
3. **rmq01** — boots and runs `rabbitmq.sh`. This takes longer because it installs Erlang and its many dependencies via `yum`.
4. **app01** — boots and runs `tomcat.sh`. This includes the Maven build, which downloads all Java dependencies and compiles the source code — the longest provisioning step.
5. **web01** — boots and runs `nginx.sh`.

> **Expected total time: 15 to 30 minutes**, depending on your internet connection speed. The `yum update` and Maven dependency downloads are the main factors.

You will see provisioning output scrolling in the terminal as each script runs. A VM is complete when you see `==> vmname: Machine booted and ready!` followed by the script output finishing without errors.

### Accessing the Application

Once all VMs are provisioned, open a browser. You can access the application using either the IP address or the hostname:

```
http://192.168.56.11
```

or simply:

```
http://web01
```

The hostname `web01` works because the Vagrant hostmanager plugin updates your host machine's `/etc/hosts` file automatically (`config.hostmanager.manage_host = true` in the Vagrantfile). No manual DNS or hosts file editing is needed.

### Important: Provisioning Only Runs Once

Vagrant runs the shell scripts **only when a VM is first created**. If you stop and restart existing VMs, the scripts do not run again — Vagrant simply powers the VMs back on in their existing state.

This means:

```bash
# First time — creates VMs and runs all provisioning scripts
vagrant up

# Subsequent runs — just starts the already-configured VMs, no scripts run
vagrant up
```

---

## Managing the Stack

### Check VM Status

```bash
vagrant status
```

Shows whether each VM is running, powered off, or not created.

### Stop the Stack Without Destroying It

```bash
vagrant halt
```

This powers off all VMs cleanly. Your configuration and data are preserved. Run `vagrant up` again from the same directory to bring everything back up — no reprovisioning, just a normal boot.

### Bring Up a Single VM

```bash
vagrant up db01
```

### Re-Run Provisioning on an Existing VM

```bash
vagrant provision db01
```

---

## Tearing Down

```bash
vagrant destroy --force
```

This destroys all five VMs permanently. Because the entire setup is automated, rebuilding the full stack from scratch requires only `vagrant up` again.

---

## Infrastructure as Code

This automated setup is an example of **Infrastructure as Code (IaC)** — the practice of defining and managing infrastructure (servers, services, configuration) through files and scripts rather than manual steps.

| Property | What it means for this project |
|----------|-------------------------------|
| **Automated** | `vagrant up` builds the entire stack without manual intervention |
| **Repeatable** | Every `vagrant up` produces an identical environment |
| **Version-controlled** | The `Vagrantfile` and shell scripts can be stored in Git like any other code |
| **Documented** | The scripts themselves serve as living documentation of how the stack is set up |

This is the foundation for more advanced IaC tools covered later in the course — Ansible, CloudFormation, Terraform — which apply the same principle at greater scale.

---

## Manual vs Automated — Key Differences

| Aspect | Manual | Automated |
|--------|--------|-----------|
| Setup trigger | SSH into each VM, run commands one by one | `vagrant up` from host machine |
| File creation | `vi` editor | `cat <<EOT` here documents |
| MySQL queries | Interactive MySQL prompt | `mysql -e "..."` from shell |
| `/etc/hosts` | Manually verified and updated | Managed by Vagrant hostmanager plugin |
| Firewall on app01 | Configured and enabled | Disabled (Nginx on web01 handles external access) |
| Error recovery | Manual diagnosis and re-execution | Fix the script, run `vagrant provision` |
| Repeatability | Requires following steps each time | Identical environment every `vagrant up` |

---

## Next Step

With automated provisioning in place, the same validation steps apply — access `http://192.168.56.11` in the browser and work through the five-service validation checks covered in the Browser Validation notes.

---