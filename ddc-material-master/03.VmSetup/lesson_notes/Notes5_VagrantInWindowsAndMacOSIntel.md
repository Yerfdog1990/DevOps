# Installing and Using Vagrant on Windows and macOS (Intel)

---

## Overview

Vagrant is a **command-line VM automation tool** — not a graphical application. It manages the full lifecycle of virtual machines: creating, configuring, and cleaning them up. Vagrant is **not a replacement** for hypervisors like VirtualBox or VMware — it sits **on top of them**, using them as providers.

### The Problem Vagrant Solves

Managing VMs manually is painful:

- OS installation involves many tedious steps and takes a long time
- Multiplied effort for every additional VM
- High risk of **human error** across many manual steps
- Replicating the same setup on another machine requires doing everything from scratch
- Documentation of all steps is error-prone and hard to maintain

Vagrant addresses all of these by automating the entire process.

---

## Prerequisites

Before using Vagrant, you need:

- **Oracle VM VirtualBox** installed (default provider for Vagrant)
- **Vagrant** installed on your machine
- A terminal to run commands:
    - **Windows** → use **Git Bash**
    - **macOS** → use **Terminal**

---

## Core Concepts (Quick Recap)

| Concept | Description |
|---|---|
| **Box** | A pre-built VM image stored on Vagrant Cloud (like a template) |
| **Vagrantfile** | A text file (Ruby syntax) describing VM settings — RAM, CPU, IP, provisioning, etc. |
| **Vagrant Cloud** | Online registry of freely available boxes at [app.vagrantup.com](https://app.vagrantup.com) |
| **Provider** | The hypervisor Vagrant uses to create VMs (default: VirtualBox) |
| **Provisioning** | Commands executed automatically after the VM boots |

Boxes are downloaded once and stored locally. Multiple VMs can be created from the same box without re-downloading.

---

## Step-by-Step: Creating Your First Vagrant VMs

### 1. Open Your Terminal

- **Windows:** Open **Git Bash**
- **macOS:** Open **Terminal**

Check your current directory:
```bash
pwd
```

### 2. Create a Working Directory

**Windows (using F drive or C drive):**
```bash
mkdir /f/vagrant-vms
cd /f/vagrant-vms
```

**macOS (using Desktop):**
```bash
mkdir ~/Desktop/vagrant-vms
cd ~/Desktop/vagrant-vms
```

Create subdirectories for each VM:
```bash
mkdir centos
mkdir ubuntu
ls    # confirm both folders are created
```

---

## Setting Up a CentOS VM

### 3. Find a Box on Vagrant Cloud

Go to [app.vagrantup.com](https://app.vagrantup.com) and search for **centos-stream-9**.

Recommended box: `eurolinux-vagrant/centos-stream-9`

- Supports VirtualBox, libvirt, VMware Workstation
- Verify VirtualBox is listed under supported providers before using

Copy the box name exactly from the Vagrant Cloud page.

### 4. Initialize the Vagrantfile

Navigate into the centos folder and initialize:

```bash
cd /f/vagrant-vms/centos        # Windows
# OR
cd ~/Desktop/vagrant-vms/centos # macOS

vagrant init eurolinux-vagrant/centos-stream-9
```

This creates a `Vagrantfile` in the current directory. Confirm with:
```bash
ls
cat Vagrantfile    # print contents (note: capital V)
```

The key line in the Vagrantfile will be:
```ruby
config.vm.box = "eurolinux-vagrant/centos-stream-9"
```

> **Tip:** If you make a typo in the box name during `vagrant init`, just open the Vagrantfile in Notepad (Windows) or any text editor (macOS) and correct the `config.vm.box` line. Save and continue.

### 5. Start the VM

```bash
vagrant up
```

What happens during `vagrant up`:
1. Vagrant reads the Vagrantfile
2. Checks if the box exists locally — if not, downloads it from Vagrant Cloud
3. Contacts VirtualBox to create the VM using that box
4. Boots the VM

> **Common errors on Windows:**
> - `schannel: next InitializeSecurityContext` error → caused by **antivirus** — disable it and retry
> - `VBox hardening 0x80...` error → also antivirus-related — fully disable antivirus
> - **VPN connected** → disconnect it before running `vagrant up`
> - **Corporate/proxy network** → switch to a different internet connection

### 6. Verify and Access the VM

```bash
vagrant status        # check if VM is running
vagrant ssh           # log into the VM via SSH
```

Inside the VM, the prompt changes — you're now in the guest machine:
```bash
whoami        # shows: vagrant
pwd           # shows: /home/vagrant
sudo -i       # switch to root user
whoami        # shows: root
exit          # logout from root
exit          # logout from the VM entirely
```

### 7. Manage the VM Lifecycle

```bash
vagrant halt      # gracefully power off the VM
vagrant up        # power it back on (no re-download, no re-create)
vagrant reload    # reboot + re-apply Vagrantfile changes
vagrant destroy   # permanently delete the VM (prompts y/N)
```

> **Important:** After `vagrant destroy`, the VM is gone — but the **box file is kept** locally. Running `vagrant up` again will create a brand new VM from scratch.

---

## Setting Up an Ubuntu VM

### 1. Find the Ubuntu Box

Search Vagrant Cloud for **ubuntu jammy**.

Recommended box: `ubuntu/jammy64` (Ubuntu 22.04 LTS "Jammy Jellyfish")

### 2. Initialize and Start

```bash
cd /f/vagrant-vms/ubuntu        # Windows
# OR
cd ~/Desktop/vagrant-vms/ubuntu # macOS

vagrant init ubuntu/jammy64
vagrant up
```

### 3. Verify and Access

```bash
vagrant status
vagrant ssh
```

Inside the VM:
```bash
whoami        # vagrant
sudo -i       # switch to root
exit          # back to vagrant user
exit          # back to host machine
```

### 4. Power Off

```bash
vagrant halt
```

---

## Checking All VMs at Once

When you have multiple VMs across different folders, use:

```bash
vagrant global-status
```

This shows all known Vagrant VMs with their state and folder location. Example output:

```
id       name    provider   state    directory
---------------------------------------------------------------
abc123   default virtualbox running  /f/vagrant-vms/ubuntu
def456   default virtualbox poweroff /f/vagrant-vms/centos
```

To clean up stale/old entries:
```bash
vagrant global-status --prune
```

---

## Listing Downloaded Boxes

```bash
vagrant box list
```

Shows all box images stored on your local machine. Each project reuses downloaded boxes — no re-download needed.

To remove a box:
```bash
vagrant box remove <box-name>
```

---

## Key Commands Summary

| Command | Description |
|---|---|
| `vagrant init <boxname>` | Create a Vagrantfile with the specified box |
| `vagrant up` | Create VM (if new) or power on (if existing) |
| `vagrant ssh` | SSH into the running VM |
| `vagrant halt` | Gracefully power off the VM |
| `vagrant reload` | Reboot and re-apply Vagrantfile changes |
| `vagrant destroy` | Delete the VM entirely |
| `vagrant status` | Show status of VM in current folder |
| `vagrant global-status` | Show status of all Vagrant VMs |
| `vagrant global-status --prune` | Clean up stale VM entries |
| `vagrant box list` | List all downloaded boxes |
| `vagrant box remove <name>` | Remove a downloaded box |
| `cat Vagrantfile` | Print Vagrantfile contents |
| `history` | Show all previously executed commands |

---

## Navigation Tips (Git Bash / Terminal)

```bash
pwd           # print current directory
ls            # list folder contents
cd <folder>   # move into a folder
cd ..         # go one level up
clear         # clear the screen
history       # show command history
↑ / ↓         # scroll through previous commands
Tab           # auto-complete folder/file names
```

**Pasting in Git Bash (Windows):**
- `Shift + Insert`
- Or right-click → Paste

---

## Important Rules to Remember

1. **Always be in the correct folder** when running Vagrant commands — the Vagrantfile must be present in the current directory.
2. **Never manage VMs directly through VirtualBox** after setting them up with Vagrant — Vagrant won't know about changes made outside of it and may report incorrect status.
3. **Power off VMs before shutting down your computer** — use `vagrant halt` first.
4. **Keep your CentOS and Ubuntu VMs** — they will be used throughout the Linux section for practice.
5. If a VM is destroyed accidentally, just run `vagrant up` in the correct folder to recreate it.

---

## Folder Structure Reference

```
vagrant-vms/
├── centos/
│   └── Vagrantfile    ← eurolinux-vagrant/centos-stream-9
└── ubuntu/
    └── Vagrantfile    ← ubuntu/jammy64
```

---

