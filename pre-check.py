#!/usr/bin/env python3
"""
Kaspa Docker Pre-Check Script
Developed by KaspaDev (KRCBOT)

This script validates system requirements for running the Kaspa Docker setup.
Supports Windows, Linux, and macOS.
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import socket
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Print the script header"""
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("    Kaspa Docker Pre-Check Script")
    print("    Developed by KaspaDev (KRCBOT)")
    print("=" * 60)
    print(f"{Colors.END}")
    print()

def print_check(check_name, status, message=""):
    """Print check result with colored output"""
    if status:
        status_text = f"{Colors.GREEN}✓ PASS{Colors.END}"
    else:
        status_text = f"{Colors.RED}✗ FAIL{Colors.END}"
    
    print(f"{check_name:<30} {status_text}")
    if message:
        print(f"{'':32}{Colors.YELLOW}{message}{Colors.END}")

def check_os():
    """Check operating system compatibility"""
    system = platform.system().lower()
    if system in ['windows', 'linux', 'darwin']:
        print_check("Operating System", True, f"Detected: {platform.system()} {platform.release()}")
        return True
    else:
        print_check("Operating System", False, f"Unsupported OS: {platform.system()}")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print_check("Python Version", True, f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_check("Python Version", False, f"Python {version.major}.{version.minor} (requires 3.6+)")
        return False

def check_docker():
    """Check Docker installation and version"""
    try:
        # Check if docker command exists
        docker_path = shutil.which('docker')
        if not docker_path:
            print_check("Docker Installation", False, "Docker not found in PATH")
            return False
        
        # Check Docker version
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_check("Docker Installation", True, version)
            
            # Check if Docker daemon is running
            try:
                subprocess.run(['docker', 'info'], 
                             capture_output=True, text=True, timeout=10)
                print_check("Docker Daemon", True, "Docker daemon is running")
                return True
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                print_check("Docker Daemon", False, "Docker daemon is not running")
                return False
        else:
            print_check("Docker Installation", False, "Docker command failed")
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_check("Docker Installation", False, "Docker not found or not accessible")
        return False

def check_docker_compose():
    """Check Docker Compose installation"""
    try:
        # Check for docker-compose command
        compose_path = shutil.which('docker-compose')
        if compose_path:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                print_check("Docker Compose", True, version)
                return True
        
        # Check for docker compose plugin (newer versions)
        result = subprocess.run(['docker', 'compose', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_check("Docker Compose", True, f"Plugin: {version}")
            return True
        
        print_check("Docker Compose", False, "Neither docker-compose nor docker compose plugin found")
        return False
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_check("Docker Compose", False, "Docker Compose not found")
        return False

def check_ports():
    """Check if required ports are available"""
    required_ports = [16111, 16110, 17110, 18110]
    all_available = True
    
    for port in required_ports:
        try:
            # Try to bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.bind(('127.0.0.1', port))
                print_check(f"Port {port}", True, "Available")
        except OSError:
            print_check(f"Port {port}", False, "Port is already in use")
            all_available = False
    
    return all_available

def check_disk_space():
    """Check available disk space"""
    try:
        # Check current directory disk space
        statvfs = os.statvfs('.')
        free_space_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
        
        # Require at least 10GB free space
        required_gb = 10
        if free_space_gb >= required_gb:
            print_check("Disk Space", True, f"{free_space_gb:.1f}GB available (>= {required_gb}GB required)")
            return True
        else:
            print_check("Disk Space", False, f"{free_space_gb:.1f}GB available (requires >= {required_gb}GB)")
            return False
            
    except (OSError, AttributeError):
        # Windows doesn't have statvfs, try alternative method
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            free_gb = free / (1024**3)
            required_gb = 10
            
            if free_gb >= required_gb:
                print_check("Disk Space", True, f"{free_gb:.1f}GB available (>= {required_gb}GB required)")
                return True
            else:
                print_check("Disk Space", False, f"{free_gb:.1f}GB available (requires >= {required_gb}GB)")
                return False
        except:
            print_check("Disk Space", False, "Could not determine disk space")
            return False

def check_memory():
    """Check available system memory"""
    try:
        if platform.system() == 'Linux':
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                for line in meminfo.split('\n'):
                    if 'MemAvailable' in line:
                        available_kb = int(line.split()[1])
                        available_gb = available_kb / (1024**2)
                        break
        elif platform.system() == 'Darwin':  # macOS
            result = subprocess.run(['vm_stat'], capture_output=True, text=True)
            if result.returncode == 0:
                # Parse vm_stat output (simplified)
                available_gb = 4  # Default assumption for macOS
        else:  # Windows
            import psutil
            available_gb = psutil.virtual_memory().available / (1024**3)
        
        # Require at least 2GB available memory
        required_gb = 2
        if available_gb >= required_gb:
            print_check("System Memory", True, f"{available_gb:.1f}GB available (>= {required_gb}GB required)")
            return True
        else:
            print_check("System Memory", False, f"{available_gb:.1f}GB available (requires >= {required_gb}GB)")
            return False
            
    except Exception as e:
        print_check("System Memory", False, f"Could not determine memory: {str(e)}")
        return False

def check_required_files():
    """Check if required files exist"""
    required_files = [
        'docker-compose.yml',
        'Dockerfile',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print_check(f"File: {file}", True)
        else:
            print_check(f"File: {file}", False, "Required file missing")
            all_exist = False
    
    return all_exist

def check_network():
    """Check network connectivity"""
    try:
        # Test DNS resolution
        import socket
        socket.gethostbyname('docker.io')
        print_check("Network Connectivity", True, "DNS resolution working")
        
        # Test internet connectivity (optional)
        try:
            import urllib.request
            urllib.request.urlopen('https://docker.io', timeout=5)
            print_check("Internet Access", True, "Can reach Docker Hub")
        except:
            print_check("Internet Access", False, "Cannot reach Docker Hub (may affect image pulls)")
        
        return True
        
    except socket.gaierror:
        print_check("Network Connectivity", False, "DNS resolution failed")
        return False
    except Exception as e:
        print_check("Network Connectivity", False, f"Network error: {str(e)}")
        return False

def generate_report(results):
    """Generate a summary report"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}System Requirements Summary{Colors.END}")
    print("-" * 40)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed! Your system is ready for Kaspa Docker.{Colors.END}")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please address the issues above.{Colors.END}")
        return False

def main():
    """Main function"""
    print_header()
    
    # Run all checks
    results = {
        'OS': check_os(),
        'Python': check_python(),
        'Docker': check_docker(),
        'Docker Compose': check_docker_compose(),
        'Required Files': check_required_files(),
        'Ports': check_ports(),
        'Disk Space': check_disk_space(),
        'Memory': check_memory(),
        'Network': check_network()
    }
    
    # Generate report
    success = generate_report(results)
    
    print(f"\n{Colors.BLUE}For more information, visit: https://github.com/kaspanet/rusty-kaspad{Colors.END}")
    print(f"{Colors.BLUE}Developed by KaspaDev (KRCBOT){Colors.END}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
