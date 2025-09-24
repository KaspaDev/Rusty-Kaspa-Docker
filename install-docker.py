#!/usr/bin/env python3
"""
Docker & Docker Compose Installation Script
Developed by KaspaDev (KRCBOT)

Cross-platform script to install Docker and Docker Compose on:
- Linux (Ubuntu, Debian, CentOS, RHEL, Fedora, Arch)
- macOS
- Windows (with WSL2 support)

This script is part of the Kaspa Docker setup toolkit.
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import urllib.request
import tempfile
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header():
    """Print the script header"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("    🐳 Docker & Docker Compose Installation Script")
    print("    Developed by KaspaDev (KRCBOT)")
    print("=" * 70)
    print(f"{Colors.END}")
    print(f"{Colors.YELLOW}This script will install Docker and Docker Compose on your system.{Colors.END}")
    print()

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{Colors.UNDERLINE}{title}{Colors.END}")
    print("-" * len(title))

def print_step(step, message):
    """Print a step with colored output"""
    print(f"{Colors.CYAN}[{step}] {message}{Colors.END}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def run_command(command, description="", check=True, shell=False):
    """Run a command with error handling"""
    try:
        print_step("RUN", description or command)
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Command completed successfully")
            return True, result.stdout
        else:
            print_error(f"Command failed: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with return code {e.returncode}: {e.stderr}")
        return False, str(e)
    except Exception as e:
        print_error(f"Error running command: {str(e)}")
        return False, str(e)

def check_command_exists(command):
    """Check if a command exists in PATH"""
    return shutil.which(command) is not None

def get_linux_distro():
    """Detect Linux distribution"""
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('ID='):
                    return line.split('=')[1].strip().strip('"')
    except:
        pass
    
    # Fallback methods
    if os.path.exists('/etc/debian_version'):
        return 'debian'
    elif os.path.exists('/etc/redhat-release'):
        return 'rhel'
    elif os.path.exists('/etc/arch-release'):
        return 'arch'
    
    return 'unknown'

def install_docker_linux():
    """Install Docker on Linux"""
    distro = get_linux_distro()
    print_section(f"Installing Docker on {distro.title()}")
    
    if distro in ['ubuntu', 'debian']:
        return install_docker_ubuntu_debian()
    elif distro in ['centos', 'rhel', 'fedora']:
        return install_docker_centos_rhel_fedora()
    elif distro == 'arch':
        return install_docker_arch()
    else:
        print_error(f"Unsupported Linux distribution: {distro}")
        print_warning("Please install Docker manually from https://docs.docker.com/engine/install/")
        return False

def install_docker_ubuntu_debian():
    """Install Docker on Ubuntu/Debian"""
    print_step("1", "Updating package index")
    success, _ = run_command("sudo apt-get update")
    if not success:
        return False
    
    print_step("2", "Installing required packages")
    success, _ = run_command("sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release")
    if not success:
        return False
    
    print_step("3", "Adding Docker's official GPG key")
    # Try the modern approach first, fallback to older method
    try:
        # Download the key first, then process it
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # Download the GPG key
        success, _ = run_command(f"curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o {tmp_path}")
        if success:
            # Process with gpg --dearmor
            success, _ = run_command(f"sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg {tmp_path}")
            if success:
                os.unlink(tmp_path)  # Clean up temp file
            else:
                print_step("3b", "Trying alternative GPG key method")
                # Fallback to apt-key method
                success, _ = run_command(f"sudo apt-key add {tmp_path}")
                os.unlink(tmp_path)  # Clean up temp file
        else:
            print_step("3b", "Trying alternative GPG key method")
            # Direct apt-key method - download to temp file first
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_path = tmp_file.name
            success, _ = run_command(f"curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o {tmp_path}")
            if success:
                success, _ = run_command(f"sudo apt-key add {tmp_path}")
                os.unlink(tmp_path)  # Clean up temp file
        
        if not success:
            return False
    except Exception as e:
        print_error(f"Error setting up GPG key: {e}")
        return False
    
    print_step("4", "Setting up Docker repository")
    distro_codename = subprocess.run(['lsb_release', '-cs'], capture_output=True, text=True).stdout.strip()
    arch = platform.machine()
    if arch == 'x86_64':
        arch = 'amd64'
    elif arch == 'aarch64':
        arch = 'arm64'
    
    # Check if we used the modern keyring method or the older apt-key method
    if os.path.exists('/usr/share/keyrings/docker-archive-keyring.gpg'):
        repo_cmd = f"echo \"deb [arch={arch} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu {distro_codename} stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
    else:
        repo_cmd = f"echo \"deb [arch={arch}] https://download.docker.com/linux/ubuntu {distro_codename} stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
    
    success, _ = run_command(repo_cmd, shell=True)
    if not success:
        return False
    
    print_step("5", "Installing Docker Engine")
    success, _ = run_command("sudo apt-get update")
    if not success:
        return False
    
    success, _ = run_command("sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin")
    if not success:
        return False
    
    print_step("6", "Adding user to docker group")
    success, _ = run_command(f"sudo usermod -aG docker {os.getenv('USER', 'root')}")
    if not success:
        return False
    
    print_success("Docker installed successfully on Ubuntu/Debian")
    return True

def install_docker_centos_rhel_fedora():
    """Install Docker on CentOS/RHEL/Fedora"""
    print_step("1", "Installing required packages")
    success, _ = run_command("sudo yum install -y yum-utils")
    if not success:
        return False
    
    print_step("2", "Adding Docker repository")
    success, _ = run_command("sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")
    if not success:
        return False
    
    print_step("3", "Installing Docker Engine")
    success, _ = run_command("sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin")
    if not success:
        return False
    
    print_step("4", "Starting and enabling Docker service")
    success, _ = run_command("sudo systemctl start docker")
    if not success:
        return False
    
    success, _ = run_command("sudo systemctl enable docker")
    if not success:
        return False
    
    print_step("5", "Adding user to docker group")
    success, _ = run_command(f"sudo usermod -aG docker {os.getenv('USER', 'root')}")
    if not success:
        return False
    
    print_success("Docker installed successfully on CentOS/RHEL/Fedora")
    return True

def install_docker_arch():
    """Install Docker on Arch Linux"""
    print_step("1", "Installing Docker from official repositories")
    success, _ = run_command("sudo pacman -S --noconfirm docker docker-compose")
    if not success:
        return False
    
    print_step("2", "Starting and enabling Docker service")
    success, _ = run_command("sudo systemctl start docker")
    if not success:
        return False
    
    success, _ = run_command("sudo systemctl enable docker")
    if not success:
        return False
    
    print_step("3", "Adding user to docker group")
    success, _ = run_command(f"sudo usermod -aG docker {os.getenv('USER', 'root')}")
    if not success:
        return False
    
    print_success("Docker installed successfully on Arch Linux")
    return True

def install_docker_macos():
    """Install Docker on macOS"""
    print_section("Installing Docker on macOS")
    
    # Check if Homebrew is installed
    if not check_command_exists('brew'):
        print_step("1", "Installing Homebrew")
        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        success, _ = run_command(install_cmd, shell=True)
        if not success:
            print_error("Failed to install Homebrew. Please install it manually from https://brew.sh/")
            return False
    else:
        print_success("Homebrew is already installed")
    
    print_step("2", "Installing Docker Desktop")
    success, _ = run_command("brew install --cask docker")
    if not success:
        return False
    
    print_success("Docker Desktop installed successfully on macOS")
    print_warning("Please start Docker Desktop from Applications folder")
    return True

def install_docker_windows():
    """Install Docker on Windows"""
    print_section("Installing Docker on Windows")
    
    print_warning("Windows installation requires manual steps:")
    print("1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/")
    print("2. Run the installer as Administrator")
    print("3. Enable WSL2 integration during installation")
    print("4. Restart your computer after installation")
    print("5. Start Docker Desktop")
    
    # Check if Docker is already installed
    if check_command_exists('docker'):
        print_success("Docker appears to be already installed")
        return True
    
    print_error("Please install Docker Desktop manually and run this script again")
    return False

def install_docker_compose_standalone():
    """Install standalone Docker Compose"""
    print_section("Installing Docker Compose (standalone)")
    
    # Get latest version
    try:
        with urllib.request.urlopen('https://api.github.com/repos/docker/compose/releases/latest') as response:
            data = json.loads(response.read())
            version = data['tag_name']
    except:
        version = 'v2.24.0'  # Fallback version
    
    print_step("1", f"Downloading Docker Compose {version}")
    
    # Determine architecture
    arch = platform.machine()
    if arch == 'x86_64':
        arch = 'x86_64'
    elif arch == 'aarch64' or arch == 'arm64':
        arch = 'aarch64'
    else:
        print_error(f"Unsupported architecture: {arch}")
        return False
    
    # Download URL
    url = f"https://github.com/docker/compose/releases/download/{version}/docker-compose-linux-{arch}"
    
    try:
        with urllib.request.urlopen(url) as response:
            compose_data = response.read()
    except:
        print_error("Failed to download Docker Compose")
        return False
    
    print_step("2", "Installing Docker Compose")
    compose_path = '/usr/local/bin/docker-compose'
    
    try:
        with open(compose_path, 'wb') as f:
            f.write(compose_data)
        
        # Make executable
        os.chmod(compose_path, 0o755)
        
        print_success("Docker Compose installed successfully")
        return True
    except PermissionError:
        print_error("Permission denied. Please run with sudo or install manually")
        return False

def check_docker_installation():
    """Check if Docker is properly installed"""
    print_section("Verifying Docker Installation")
    
    # Check Docker command
    if not check_command_exists('docker'):
        print_error("Docker command not found")
        return False
    
    print_success("Docker command found")
    
    # Check Docker daemon
    success, output = run_command("docker --version", "Checking Docker version")
    if success:
        print_success(f"Docker version: {output.strip()}")
    else:
        print_error("Docker version check failed")
        return False
    
    # Check Docker daemon status
    success, output = run_command("docker info", "Checking Docker daemon status")
    if success:
        print_success("Docker daemon is running")
    else:
        print_warning("Docker daemon is not running. Please start it manually")
        return False
    
    return True

def check_docker_compose_installation():
    """Check if Docker Compose is properly installed"""
    print_section("Verifying Docker Compose Installation")
    
    # Check for docker compose plugin first
    success, output = run_command("docker compose version", "Checking Docker Compose plugin")
    if success:
        print_success(f"Docker Compose plugin: {output.strip()}")
        return True
    
    # Check for standalone docker-compose
    if check_command_exists('docker-compose'):
        success, output = run_command("docker-compose --version", "Checking standalone Docker Compose")
        if success:
            print_success(f"Docker Compose standalone: {output.strip()}")
            return True
    
    print_error("Docker Compose not found")
    return False

def main():
    """Main function"""
    print_header()
    
    # Detect operating system
    system = platform.system().lower()
    print_section(f"Detected Operating System: {platform.system()} {platform.release()}")
    
    # Check if already installed
    docker_installed = check_command_exists('docker')
    compose_installed = check_command_exists('docker-compose') or check_command_exists('docker compose')
    
    if docker_installed and compose_installed:
        print_success("Docker and Docker Compose are already installed!")
        if check_docker_installation() and check_docker_compose_installation():
            print_success("Everything is working correctly!")
            return 0
        else:
            print_warning("Docker is installed but may need to be started")
            return 1
    
    # Install based on operating system
    if system == 'linux':
        if not install_docker_linux():
            return 1
        
        # Install standalone Docker Compose if plugin not available
        if not check_docker_compose_installation():
            if not install_docker_compose_standalone():
                return 1
    
    elif system == 'darwin':  # macOS
        if not install_docker_macos():
            return 1
    
    elif system == 'windows':
        if not install_docker_windows():
            return 1
    
    else:
        print_error(f"Unsupported operating system: {system}")
        return 1
    
    # Final verification
    print_section("Final Verification")
    if check_docker_installation() and check_docker_compose_installation():
        print_success("Docker and Docker Compose are ready to use!")
        print(f"\n{Colors.GREEN}You can now run the Kaspa Docker setup:{Colors.END}")
        print(f"  {Colors.CYAN}./pre-check.sh{Colors.END}  # Check system requirements")
        print(f"  {Colors.CYAN}./setup-wizard.sh{Colors.END}  # Configure your node")
        print(f"  {Colors.CYAN}docker compose up -d --build{Colors.END}  # Start your node")
        return 0
    else:
        print_error("Installation verification failed")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Installation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)
