# Installing and Using Vagrant on macOS Apple Silicon (M1, M2, M3, M4, M5)

---

## Important: This Guide is for Apple Silicon Macs Only

If your Mac has an **M1, M2, M3, M4, or M5 chip**, this guide is for you.
If you have an **Intel-based Mac**, refer to `Notes5_VagrantInWindowsAndMacOSIntel.md` instead.

---

## CPU Architecture Background

There are two major CPU architectures in use:

| Architecture | Used By |
|---|---|
| **ARM** | Apple Silicon Macs (M1, M2, M3, M4, M5) |
| **x86** | Intel and AMD chips (Windows PCs, older Macs) |

This distinction matters because most VM tools and software were originally built for x86. On Apple Silicon, additional tools are needed to bridge this gap.

---

## Tools Required

| Tool | Purpose |
|---|---|
| **Rosetta** | Allows x86-based apps to run on ARM (Apple Silicon) |
| **VMware Fusion** | Hypervisor — creates and runs virtual machines (replaces VirtualBox on Apple Silicon) |
| **Vagrant** | VM automation tool — manages the VM lifecycle on top of VMware Fusion |
| **Vagrant VMware Provider** | Plugin that lets Vagrant communicate with VMware Fusion |

> **Note:** On Apple Silicon, we use **VMware Fusion** instead of VirtualBox. VirtualBox does not have full Apple Silicon support. VMware Fusion is free for personal use.

---

## Installation Steps

### Step 1 — Install Rosetta

Rosetta allows x86-based applications to run on your ARM-based Mac. Open **Terminal** and run:

```bash
softwareupdate --install-rosetta
```

Wait for installation to complete before proceeding.

---

### Step 2 — Install Vagrant via Homebrew

Use Homebrew (`brew`) to install Vagrant:

```bash
brew install vagrant
```

This may take a few minutes. Enter your password when prompted. Wait until the installation completes successfully before moving on.

---

### Step 3 — Download VMware Fusion

VMware is now owned by **Broadcom**, so downloads are handled through the Broadcom portal.

1. Go to [https://support.broadcom.com](https://support.broadcom.com) and **register** for a free account
2. Fill in your email address and complete the verification
3. Once registered, **log in** to your Broadcom account
4. In the top dropdown, select **VMware Cloud Foundation**
5. Navigate to **My Downloads**
6. Click the link: *"Free software downloads available here"*
7. Search for **VMware Fusion** and click on it
8. Expand the version list and select **13.6.2** (or the latest available)
9. Accept the terms checkbox and click **HTTPS Download**
10. Complete any additional profile verification (address, city, etc.) if prompted
11. Click **Download** to start the download

---

### Step 4 — Install VMware Fusion

1. Locate the downloaded `.dmg` file and **double-click** it
2. Double-click the **VMware Fusion** icon inside
3. Click **Open** when prompted
4. Enter your **Mac password**
5. Click **Agree** on the license agreement
6. Select **"I want to license VMware Fusion for personal use"**
7. Click **Continue**, then **Done**
8. Click **Cancel** on the setup wizard — we will use VMware Fusion through Vagrant, not directly

---

### Step 5 — Enable VMware Fusion Accessibility Permissions

1. Go to **System Settings → Privacy & Security → Accessibility**
2. Find **VMware Fusion** in the list and **toggle it ON**
3. If VMware Fusion is not listed:
    - Click the **+** (plus) button
    - Enter your password
    - Navigate to **Applications** and select **VMware Fusion**
    - Click **Open**

---

### Step 6 — Install the Vagrant VMware Provider (via Homebrew)

This installs the underlying driver that allows Vagrant to use VMware:

```bash
brew install vagrant-vmware-utility
```

Enter your password when prompted. Wait for completion.

---

### Step 7 — Install the Vagrant VMware Plugin

This installs the Vagrant plugin that connects Vagrant to VMware Fusion:

```bash
vagrant plugin install vagrant-vmware-desktop
```

Wait for this to complete. All installation steps are now done.

---

## Creating Virtual Machines

We will create **two VMs** — one running Ubuntu and one running CentOS — all through the command line.

### Folder Structure

```
~/Desktop/vms/
├── ubuntu/
│   └── Vagrantfile
└── centos/
    └── Vagrantfile
```

---

## Setting Up the Ubuntu VM

### 1. Navigate to Home Directory and Create Folder

```bash
cd                                    # go to home directory
mkdir -p Desktop/vms/ubuntu           # create nested folders in one command
cd Desktop/vms/ubuntu                 # enter the ubuntu folder
pwd                                   # confirm you are in the right place
```

### 2. Create the Vagrantfile

```bash
vim Vagrantfile
```

Inside vim:
1. Press **`i`** to enter Insert mode (you'll see `-- INSERT --` at the bottom)
2. Paste the Ubuntu VM configuration content (provided in the lecture document)
3. Press **`Escape`** to exit insert mode
4. Type **`:wq`** and press **Enter** to save and quit

Verify the file:
```bash
ls              # should show Vagrantfile
cat Vagrantfile # prints the file content
```

### 3. Start the Ubuntu VM

```bash
vagrant up
```

- A VMware Fusion window may pop up — **minimize it**, do not use it directly
- If you see an error on the first run, press the **up arrow** and run `vagrant up` again
- Wait for the VM to fully boot

### 4. Log Into the VM

```bash
vagrant ssh
```

The prompt will change — this confirms you are now inside the VM. Inside the VM:

```bash
ip addr show    # view the VM's IP address
exit            # logout and return to macOS terminal
```

Observe the prompt to confirm you are back on your Mac.

---

## Setting Up the CentOS VM

### 1. Go Back to Home and Create CentOS Folder

```bash
cd                                    # return to home directory
mkdir -p Desktop/vms/centos
cd Desktop/vms/centos
```

### 2. Create the Vagrantfile

```bash
vim Vagrantfile
```

Inside vim:
1. Press **`i`** for Insert mode
2. Paste the CentOS VM configuration content (provided in the lecture document)
3. Press **`Escape`**
4. Type **`:wq`** and press **Enter**

Verify:
```bash
ls
cat Vagrantfile
```

### 3. Start the CentOS VM

```bash
vagrant up
```

Minimize any VMware Fusion window that appears.

### 4. Log Into the VM

```bash
vagrant ssh
```

Inside the VM:
```bash
ip addr show    # verify IP address
exit            # return to macOS terminal
```

---

## VM Lifecycle Commands

These commands must be run from **inside the VM's folder** (where the Vagrantfile lives):

| Command | Description |
|---|---|
| `vagrant up` | Create VM (if new) or power it on (if existing) |
| `vagrant ssh` | Log into the running VM |
| `vagrant halt` | Gracefully power off the VM |
| `vagrant reload` | Reboot and re-apply Vagrantfile changes |
| `vagrant destroy` | Permanently delete the VM (prompts y/N) |
| `vagrant status` | Show status of the VM in current folder |
| `vagrant global-status` | Show status of **all** Vagrant VMs on the machine |

### Example Workflow

```bash
cd ~/Desktop/vms/ubuntu
vagrant up          # power on
vagrant ssh         # log in
# ... do work ...
exit                # log out from VM
vagrant halt        # power off
```

---

## Checking All VMs at Once

```bash
vagrant global-status
```

Shows all VMs, their status, and which folder they live in:

```
id       name    provider       state    directory
-----------------------------------------------------------------
abc123   default vmware_fusion  running  /Users/you/Desktop/vms/ubuntu
def456   default vmware_fusion  poweroff /Users/you/Desktop/vms/centos
```

To clean up stale/old entries:
```bash
vagrant global-status --prune
```

---

## Bringing Up VMs — Quick Reference

**Whenever you need the Ubuntu VM:**
```bash
cd ~/Desktop/vms/ubuntu
vagrant up
vagrant ssh
```

**Whenever you need the CentOS VM:**
```bash
cd ~/Desktop/vms/centos
vagrant up
vagrant ssh
```

---

## Navigation Tips (macOS Terminal)

```bash
pwd             # print current directory
ls              # list folder contents
cd <folder>     # move into a folder
cd ..           # go one level up
cd              # go to home directory
clear           # clear the terminal screen
history         # show all previously run commands
↑ / ↓           # scroll through previous commands
Tab             # auto-complete folder/file names
```

---

## Key Differences vs. Intel Mac / Windows Setup

| Feature | Intel Mac / Windows | Apple Silicon Mac |
|---|---|---|
| **Hypervisor** | VirtualBox | VMware Fusion |
| **Extra tool needed** | None | Rosetta |
| **Extra installs** | None | `vagrant-vmware-utility` + `vagrant-vmware-desktop` plugin |
| **Vagrant install method** | Binary / package manager | Homebrew (`brew install vagrant`) |
| **VM window** | VirtualBox GUI | VMware Fusion window (minimize — don't use directly) |

---

## Important Rules to Remember

1. **Always be in the correct folder** when running Vagrant commands — the Vagrantfile must be present in the current directory.
2. **Never manage VMs directly through VMware Fusion** — use Vagrant commands only. Changes made outside Vagrant won't be tracked and may cause status errors.
3. **Power off VMs before shutting down your Mac** — use `vagrant halt` first.
4. **Keep your Ubuntu and CentOS VMs** — they will be used throughout the Linux section.
5. If a VM is destroyed, simply run `vagrant up` in the correct folder to recreate it.
6. Use **`vagrant destroy`** only when you intentionally want to delete the VM — all data inside it will be lost.

---
