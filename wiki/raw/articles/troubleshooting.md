# Troubleshooting - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/troubleshooting  
**Category:** troubleshooting  
**Scraped:** 2025-06-09 06:37:21

---

## Original Content

## 

​

Common installation issues

### 

​

Linux permission issues

When installing Claude Code with npm, you may encounter permission errors if your npm global prefix is not user writable (eg. `/usr`, or `/usr/local`).

#### 

​

Recommended solution: Create a user-writable npm prefix

The safest approach is to configure npm to use a directory within your home folder:
    
    # First, save a list of your existing global packages for later migration
    npm list -g --depth=0 > ~/npm-global-packages.txt
    
    # Create a directory for your global packages
    mkdir -p ~/.npm-global
    
    # Configure npm to use the new directory path
    npm config set prefix ~/.npm-global
    
    # Note: Replace ~/.bashrc with ~/.zshrc, ~/.profile, or other appropriate file for your shell
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
    
    # Apply the new PATH setting
    source ~/.bashrc
    
    # Now reinstall Claude Code in the new location
    npm install -g @anthropic-ai/claude-code
    
    # Optional: Reinstall your previous global packages in the new location
    # Look at ~/npm-global-packages.txt and install packages you want to keep
    
This solution is recommended because it:

  * Avoids modifying system directory permissions
  * Creates a clean, dedicated location for your global npm packages
  * Follows security best practices

#### 

​

System Recovery: If you have run commands that change ownership and permissions of system files or similar

If you’ve already run a command that changed system directory permissions (such as `sudo chown -R $USER:$(id -gn) /usr && sudo chmod -R u+w /usr`) and your system is now broken (for example, if you see `sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`), you’ll need to perform recovery steps.

##### Ubuntu/Debian Recovery Method:

  1. While rebooting, hold **SHIFT** to access the GRUB menu

  2. Select “Advanced options for Ubuntu/Debian”

  3. Choose the recovery mode option

  4. Select “Drop to root shell prompt”

  5. Remount the filesystem as writable:
    
        mount -o remount,rw /
    
  6. Fix permissions:
    
        # Restore root ownership
    chown -R root:root /usr
    chmod -R 755 /usr
    
    # Ensure /usr/local is owned by your user for npm packages
    chown -R YOUR_USERNAME:YOUR_USERNAME /usr/local
    
    # Set setuid bit for critical binaries
    chmod u+s /usr/bin/sudo
    chmod 4755 /usr/bin/sudo
    chmod u+s /usr/bin/su
    chmod u+s /usr/bin/passwd
    chmod u+s /usr/bin/newgrp
    chmod u+s /usr/bin/gpasswd
    chmod u+s /usr/bin/chsh
    chmod u+s /usr/bin/chfn
    
    # Fix sudo configuration
    chown root:root /usr/libexec/sudo/sudoers.so
    chmod 4755 /usr/libexec/sudo/sudoers.so
    chown root:root /etc/sudo.conf
    chmod 644 /etc/sudo.conf
    
  7. Reinstall affected packages (optional but recommended):
    
        # Save list of installed packages
    dpkg --get-selections > /tmp/installed_packages.txt
    
    # Reinstall them
    awk '{print $1}' /tmp/installed_packages.txt | xargs -r apt-get install --reinstall -y
    
  8. Reboot:
    
        reboot
    
##### Alternative Live USB Recovery Method:

If the recovery mode doesn’t work, you can use a live USB:

  1. Boot from a live USB (Ubuntu, Debian, or any Linux distribution)

  2. Find your system partition:
    
        lsblk
    
  3. Mount your system partition:
    
        sudo mount /dev/sdXY /mnt  # replace sdXY with your actual system partition
    
  4. If you have a separate boot partition, mount it too:
    
        sudo mount /dev/sdXZ /mnt/boot  # if needed
    
  5. Chroot into your system:
    
        # For Ubuntu/Debian:
    sudo chroot /mnt
    
    # For Arch-based systems:
    sudo arch-chroot /mnt
    
  6. Follow steps 6-8 from the Ubuntu/Debian recovery method above

After restoring your system, follow the recommended solution above to set up a user-writable npm prefix.

## 

​

Auto-updater issues

If Claude Code can’t update automatically, it may be due to permission issues with your npm global prefix directory. Follow the [recommended solution](/_sites/docs.anthropic.com/en/docs/claude-code/troubleshooting#recommended-solution-create-a-user-writable-npm-prefix) above to fix this.

If you prefer to disable the auto-updater instead, you can use: If you prefer to disable the auto-updater instead , you can set the `DISABLE_AUTOUPDATER` [environment variable](settings#environment-variables) to `1`

## 

​

Permissions and authentication

### 

​

Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools to run without approval using the `/permissions` command. See [Permissions docs](settings#permissions).

### 

​

Authentication issues

If you’re experiencing authentication problems:

  1. Run `/logout` to sign out completely
  2. Close Claude Code
  3. Restart with `claude` and complete the authentication process again

If problems persist, try:
    
    rm -rf ~/.config/claude-code/auth.json
    claude
    
This removes your stored authentication information and forces a clean login.

## 

​

Performance and stability

### 

​

High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you’re experiencing performance issues:

  1. Use `/compact` regularly to reduce context size
  2. Close and restart Claude Code between major tasks
  3. Consider adding large build directories to your `.gitignore` file

### 

​

Command hangs or freezes

If Claude Code seems unresponsive:

  1. Press Ctrl+C to attempt to cancel the current operation
  2. If unresponsive, you may need to close the terminal and restart

### 

​

ESC key not working in JetBrains (IntelliJ, PyCharm, etc.) terminals

If you’re using Claude Code in JetBrains terminals and the ESC key doesn’t interrupt the agent as expected, this is likely due to a keybinding clash with JetBrains’ default shortcuts.

To fix this issue:

  1. Go to Settings → Tools → Terminal
  2. Click the “Configure terminal keybindings” hyperlink next to “Override IDE Shortcuts”
  3. Within the terminal keybindings, scroll down to “Switch focus to Editor” and delete that shortcut

This will allow the ESC key to properly function for canceling Claude Code operations instead of being captured by PyCharm’s “Switch focus to Editor” action.

## 

​

Getting more help

If you’re experiencing issues not covered here:

  1. Use the `/bug` command within Claude Code to report problems directly to Anthropic
  2. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues
  3. Run `/doctor` to check the health of your Claude Code installation

Was this page helpful?

YesNo

[Tutorials](/en/docs/claude-code/tutorials)[Overview](/en/docs/claude-code/third-party-integrations)


---

## AI Analysis

## Analysis of Claude Code Troubleshooting Documentation

### 1. Concise Summary

This documentation provides comprehensive troubleshooting steps for common issues encountered while using Claude Code, particularly focusing on installation, auto-updater, permissions, authentication, and performance. It offers detailed solutions for Linux permission errors, including a recommended user-writable npm prefix setup and critical system recovery steps for damaged installations. Additionally, it addresses specific problems like repeated permission prompts, authentication failures, high resource usage, command freezes, and JetBrains terminal keybinding conflicts.

### 2. Key Topics Covered

*   **Installation Issues:** Specifically Linux permission errors with npm.
*   **System Recovery:** Detailed steps for recovering a broken Linux system due to incorrect permission changes.
*   **Auto-updater Issues:** Troubleshooting and disabling the auto-updater.
*   **Permissions and Authentication:** Managing repeated prompts and resolving login problems.
*   **Performance and Stability:** Addressing high CPU/memory usage, command hangs, and specific IDE keybinding conflicts.
*   **Getting More Help:** Resources for reporting bugs and checking installation health.

### 3. Important Technical Details

*   **NPM Global Prefix:** The core recommendation for installation issues is to configure npm to use a user-writable directory (`~/.npm-global`) instead of system-wide locations like `/usr` or `/usr/local`. This involves setting `npm config set prefix ~/.npm-global` and updating the `PATH` environment variable.
*   **Linux System Recovery:**
    *   **Symptoms:** `sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`, `chown -R $USER:$(id -gn) /usr && sudo chmod -R u+w /usr` causing system breakage.
    *   **Methods:**
        *   **Recovery Mode (Ubuntu/Debian):** Accessing GRUB, dropping to root shell, remounting filesystem (`mount -o remount,rw /`), restoring root ownership and permissions for `/usr`, `/usr/bin/sudo`, `/usr/bin/su`, etc., and optionally reinstalling packages.
        *   **Live USB Recovery:** Booting from a live USB, identifying and mounting the system partition, `chroot`ing into the system, and then following the recovery mode steps.
*   **Authentication:** Removing `~/.config/claude-code/auth.json` for a clean login.
*   **Performance:** Using `/compact` command, restarting Claude Code, and adding large build directories to `.gitignore`.
*   **JetBrains ESC Key Fix:** Modifying JetBrains IDE settings (Settings → Tools → Terminal → Configure terminal keybindings) to remove the "Switch focus to Editor" shortcut.
*   **Internal Commands:** `/permissions`, `/logout`, `/compact`, `/bug`, `/doctor`.
*   **Environment Variable:** `DISABLE_AUTOUPDATER` to disable auto-updates.

### 4. Code Examples

```bash
# Recommended solution: Create a user-writable npm prefix
npm list -g --depth=0 > ~/npm-global-packages.txt
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc # or ~/.zshrc, ~/.profile
source ~/.bashrc
npm install -g @anthropic-ai/claude-code

# System Recovery: Remount filesystem
mount -o remount,rw /

# System Recovery: Fix permissions
chown -R root:root /usr
chmod -R 755 /usr
chown -R YOUR_USERNAME:YOUR_USERNAME /usr/local
chmod u+s /usr/bin/sudo
chmod 4755 /usr/bin/sudo
chmod u+s /usr/bin/su
# ... (other chmod u+s commands for critical binaries)
chown root:root /usr/libexec/sudo/sudoers.so
chmod 4755 /usr/libexec/sudo/sudoers.so
chown root:root /etc/sudo.conf
chmod 644 /etc/sudo.conf

# System Recovery: Reinstall affected packages
dpkg --get-selections > /tmp/installed_packages.txt
awk '{print $1}' /tmp/installed_packages.txt | xargs -r apt-get install --reinstall -y

# System Recovery: Reboot
reboot

# Live USB Recovery: Mount partition
sudo mount /dev/sdXY /mnt
sudo mount /dev/sdXZ /mnt/boot # if needed

# Live USB Recovery: Chroot
sudo chroot /mnt # For Ubuntu/Debian
sudo arch-chroot /mnt # For Arch-based systems

# Authentication issues
rm -rf ~/.config/claude-code/auth.json
claude
```

### 5. Related Concepts or Prerequisites

*   **Linux Command Line Basics:** Familiarity with `npm`, `mkdir`, `echo`, `export`, `source`, `chown`, `chmod`, `mount`, `reboot`, `lsblk`, `sudo`, `dpkg`, `apt-get`, `awk`, `xargs`, `chroot`.
*   **NPM Package Management:** Understanding of global npm packages and prefixes.
*   **Linux File System Permissions:** Knowledge of `root` ownership, `setuid` bit, and standard file permissions (e.g., 755, 644).
*   **Linux Boot Process:** Basic understanding of GRUB menu and recovery mode.
*   **Environment Variables:** How to set and use them (e.g., `PATH`, `DISABLE_AUTOUPDATER`).
*   **JetBrains IDEs:** Familiarity with their settings and keybinding configurations.
*   **Claude Code Specifics:** Knowledge of its internal commands (`/permissions`, `/logout`, `/compact`, `/bug`, `/doctor`).
