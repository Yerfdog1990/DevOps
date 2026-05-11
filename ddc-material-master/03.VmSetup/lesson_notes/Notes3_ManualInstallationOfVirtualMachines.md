# Manual Virtual Machine Installation

## Overview

This guide covers the complete process of manually setting up virtual machines using Oracle VirtualBox, including prerequisites, VM creation, operating system installation, and network configuration for both CentOS Stream 9 and Ubuntu Server.

## Prerequisites (Windows Only)

### 1. Enable Virtualization in BIOS
**Critical Step**: This is not an operating system setting - you must access BIOS during boot.

#### How to Access BIOS:
- Reboot your computer
- During boot, press the appropriate key based on your computer manufacturer:
  - **F2**, **F12**, **Delete**, or **Escape** (varies by manufacturer)
- Look for virtualization settings with names like:
  - Virtualization Technology (VTx)
  - Intel Virtualization Technology
  - Secure Virtual Machine
  - Virtualization

#### Verification:
If you only see 32-bit options in VirtualBox, virtualization is not enabled in BIOS.

### 2. Disable Conflicting Windows Features
Access Windows Features through Start Menu search:

#### Disable These Settings:
- Microsoft Hyper-V
- Windows Hypervisor Platform
- Windows Subsystem for Linux (WSL)
- Docker Desktop
- Virtual Machine Platform

#### Steps:
1. Search for "Turn Windows features on or off"
2. Uncheck all hypervisor-related options
3. Click OK and reboot computer

### 3. Network Precautions
- Power off computer
- Reboot router
- Power on computer
- This prevents VM IP address issues

## VirtualBox VM Creation

### Version Check
- Open Oracle VirtualBox
- Check version: Help → About VirtualBox (example: 7.1.4)

### Creating CentOS VM
1. Click **New** (gear symbol)
2. **Name**: centosvm (or any preferred name)
3. **Type**: Linux
4. **Version**: Red Hat (64-bit)
   - If only 32-bit appears, VT is not enabled in BIOS
5. **Hardware Settings**:
   - **Memory**: 2048 MB (2 GB) - minimum 1024 MB (1 GB)
   - **CPU**: 2 processors
   - **Hard Disk**: 20 GB dynamically allocated
     - Ensure "Pre-allocate Full Size" is NOT checked

### Creating Ubuntu VM
1. Click **New**
2. **Name**: ubuntuvm
3. **Type**: Linux
4. **Version**: Ubuntu (64-bit)
5. **Hardware Settings**:
   - **Memory**: 2048 MB (2 GB)
   - **CPU**: 2 processors
   - **Hard Disk**: 25 GB (default for Ubuntu)

## Operating System Installation Files

### CentOS Stream 9
1. Search: "CentOS Stream 9 ISO download"
2. Navigate to official CentOS site
3. Download: `boot.iso` (approximately 1 GB)
4. Save ISO file to computer

### Ubuntu Server 22.04 LTS
1. Search: "Ubuntu 22 server ISO"
2. Download: "Ubuntu 22.04 LTS (Jammy Jellyfish) Server install image"
3. Ensure it's the server version, not desktop

## Network Configuration

### Understanding Network Adapters
- **Physical Computer**: Has network adapters (WiFi, Ethernet)
- **Router**: Allocates IP addresses via DHCP
- **Virtual Machine**: Needs virtual network adapter for connectivity

### Bridge Networking Concept
Bridge networking allows VM to connect directly to your physical network:
```
VM Network Adapter → Computer Network Adapter → WiFi Router → Internet
```

### Configuring Bridge Adapter
1. Select VM → Settings → Network
2. **Adapter 1**: Keep as NAT (default)
3. **Adapter 2**: 
   - Enable Network Adapter ✓
   - Attached to: Bridged Adapter
   - Name: Select your computer's active network adapter
     - WiFi: Select wireless adapter
     - Ethernet: Select ethernet adapter

### Finding Your Network Adapter Name
1. Windows: Control Panel → Network and Sharing Center → Change adapter settings
2. Look for active adapter name (e.g., "Intel WiFi", "Ethernet")

### Additional Settings
1. **Settings → System → Motherboard**
2. **Pointing Device**: Select USB Tablet (for better mouse control)

## CentOS Installation Process

### ISO Attachment
1. VM Settings → Storage
2. Click on empty CD icon under Controller: IDE
3. Choose disk file → Select CentOS ISO
4. Check "Live CD/DVD" option

### Installation Steps
1. Start VM
2. Select "Install CentOS Stream 9" using arrow keys
3. **Language Selection**: English → Continue
4. **Installation Destination**: 
   - Select virtual hard disk (20 GB)
   - Automatic partitioning → Done
5. **Network & Host Name**:
   - Configure both network adapters
   - Set hostname: centosvm
   - Apply → Done
6. **Root Password**: 
   - Set strong password
   - Weak passwords require double confirmation
7. **Begin Installation**: Wait 10-15 minutes

### Post-Installation Setup
1. Power off VM (don't use reboot option)
2. Remove ISO from virtual drive
3. Start VM
4. Complete initial setup:
   - Create user account
   - Set password
5. Verify IP address:
   ```bash
   ip addr show
   ```
6. Note the bridged adapter IP (e.g., 192.168.1.x)

## Ubuntu Installation Process

### ISO Attachment
Same process as CentOS, using Ubuntu ISO file

### Installation Steps
1. Start VM
2. **Language**: English → Continue
3. **Keyboard Layout**: Default → Done
4. **Network Configuration**:
   - Verify both adapters are detected
   - Note IP addresses
5. **Storage Configuration**:
   - Use entire disk → Done
   - Confirm partition changes → Continue
6. **User Configuration**:
   - Your name: Full name
   - Server name: ubuntuvm
   - Username: devops (or preferred)
   - Password: Set strong password
7. **SSH Server**:
   - **CRITICAL**: Select "Install OpenSSH Server" using spacebar
   - This enables remote access
8. **Installation**: Wait 10-15 minutes

### Post-Installation Setup
1. Power off VM
2. Remove ISO from virtual drive
3. Start VM
4. Login with created credentials
5. Verify IP address:
   ```bash
   ip addr show
   ```

## SSH Connection Setup

### From Host Computer
1. Open Git Bash or terminal
2. Connect to VM:
   ```bash
   ssh username@vm_ip_address
   ```
3. Accept host key fingerprint (first time only)
4. Enter password

### Verification Commands
Inside VM:
```bash
# Check IP addresses
ip addr show

# Check hostname
hostname

# Exit SSH session
exit
```

## Network Troubleshooting

### Common Issues and Solutions

#### 1. VM Not Getting IP Address
**Problem**: Bridged adapter shows no IP address
**Solution**:
```bash
# Check device status
nmcli device status

# Connect device manually
sudo nmcli device connect enp0s8

# Create connection if needed
sudo nmcli connection add type ethernet ifname enp0s8 con-name bridged-conn
sudo nmcli connection up bridged-conn
```

#### 2. SSH Connection Timeouts
**Problem**: `ssh: connect to host port 22: Operation timed out`

**Troubleshooting Steps**:
1. **Verify IP Address**:
   ```bash
   # On VM
   ip addr show
   # On host
   ping vm_ip_address
   ```

2. **Check SSH Server Status**:
   ```bash
   sudo systemctl status sshd
   sudo systemctl start sshd
   sudo systemctl enable sshd
   ```

3. **Test Port Connectivity**:
   ```bash
   # From host
   nc -zv vm_ip_address 22
   ```

4. **Verify Network Configuration**:
   - Ensure VM and host are on same network
   - Check firewall settings
   - Verify bridge adapter configuration

#### 3. NAT vs Bridged Adapter Issues
**NAT Adapter (10.0.2.x)**:
- VM can access internet
- Host cannot directly SSH to VM

**Bridged Adapter (192.168.1.x)**:
- VM appears as real network device
- Host can SSH directly
- Both can access internet

#### 4. Adapter Configuration Problems
**If Adapter 2 not working**:
1. Disable Adapter 1 (NAT) cable connection
2. Ensure Adapter 2 is enabled and bridged
3. Restart VM
4. Check interface status with `nmcli device status`

## Advanced Configuration

### VirtualBox Network Modes

#### NAT (Default)
- VM gets IP: 10.0.2.x
- Easy internet access
- Limited host connectivity
- Good for basic internet access

#### Bridged Adapter
- VM gets IP from your router (e.g., 192.168.1.x)
- Full network integration
- Direct SSH access from host
- Best for development environments

#### Host-Only Adapter
- Private network between host and VMs
- No internet access
- Secure testing environment

### Multiple Network Adapters
VMs can have up to 4 network adapters:
- **Adapter 1**: Usually NAT for internet
- **Adapter 2**: Bridged for host connectivity
- **Adapter 3-4**: Additional configurations as needed

## Best Practices

### Resource Allocation
- **Minimum RAM**: 2 GB per VM
- **Recommended RAM**: 4 GB for better performance
- **CPU**: At least 2 processors
- **Disk Space**: 20-25 GB dynamically allocated

### Security Considerations
- Use strong passwords for all accounts
- Enable SSH key authentication for production
- Keep systems updated
- Configure firewall rules as needed

### Performance Optimization
- Install Guest Additions after OS installation
- Allocate sufficient resources based on workload
- Use SSD storage for better performance
- Monitor resource usage

## Common Errors and Solutions

### Installation Failures
1. **ISO Corruption**: Re-download ISO files
2. **Insufficient Resources**: Increase RAM/CPU allocation
3. **Virtualization Disabled**: Enable VT in BIOS
4. **Hyper-V Conflicts**: Disable Windows hypervisor features

### Boot Issues
1. **Boot Loop**: Check boot order in VM settings
2. **Graphics Problems**: Change graphics controller to VMSVGA
3. **Kernel Panics**: Use stable LTS releases

### Network Problems
1. **No IP Address**: Check DHCP configuration
2. **Wrong Adapter**: Verify correct adapter selection
3. **Firewall Blocking**: Configure firewall rules

## Unattended Installation (Optional)

### When to Use
- Automated deployments
- Multiple identical VMs
- Testing environments

### Potential Issues
- Installer crashes
- Boot problems
- Login/password issues
- Network configuration problems

### Recommendation for Beginners
Disable unattended installation and perform manual setup for better control and understanding.

## Summary

This manual installation process provides:
- Complete understanding of virtualization concepts
- Hands-on experience with Linux installations
- Network configuration skills
- Troubleshooting capabilities
- Foundation for advanced DevOps topics

The skills learned here are essential for:
- Docker networking concepts
- Kubernetes networking
- Cloud computing environments
- System administration tasks

---

**Next Steps**: After completing manual installations, explore automated VM creation using Vagrant, Ansible, or cloud provider APIs for more efficient deployments.