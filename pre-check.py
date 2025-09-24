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

# Try to import psutil, install if not available
try:
    import psutil
except ImportError:
    print("Installing required dependency: psutil")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "psutil"])
    import psutil

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

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{Colors.UNDERLINE}{title}{Colors.END}")
    print("-" * len(title))

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
    required_ports = [16111, 17110, 18110]
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

def get_cpu_info():
    """Get CPU information"""
    try:
        cpu_count = psutil.cpu_count(logical=False)  # Physical cores
        cpu_count_logical = psutil.cpu_count(logical=True)  # Logical cores
        
        # Try to get CPU model
        cpu_model = "Unknown"
        if platform.system() == 'Linux':
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if line.startswith('model name'):
                            cpu_model = line.split(':')[1].strip()
                            break
            except:
                pass
        elif platform.system() == 'Darwin':
            try:
                result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    cpu_model = result.stdout.strip()
            except:
                pass
        elif platform.system() == 'Windows':
            try:
                result = subprocess.run(['wmic', 'cpu', 'get', 'name', '/value'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.startswith('Name='):
                            cpu_model = line.split('=', 1)[1].strip()
                            break
            except:
                pass
        
        return {
            'physical_cores': cpu_count,
            'logical_cores': cpu_count_logical,
            'model': cpu_model
        }
    except Exception as e:
        return {
            'physical_cores': 1,
            'logical_cores': 1,
            'model': 'Unknown'
        }

def get_storage_info():
    """Get storage information and detect type"""
    try:
        # Get disk usage for current directory
        disk_usage = psutil.disk_usage('.')
        total_gb = disk_usage.total / (1024**3)
        free_gb = disk_usage.free / (1024**3)
        
        # Try to detect storage type
        storage_type = "Unknown"
        storage_speed = "Unknown"
        
        if platform.system() == 'Linux':
            try:
                # Check if it's an SSD by looking at /sys/block
                result = subprocess.run(['lsblk', '-d', '-o', 'name,rota'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n')[1:]:  # Skip header
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                device = parts[0]
                                rota = parts[1]
                                if rota == '0':  # SSD
                                    storage_type = "SSD"
                                    storage_speed = "Fast"
                                else:  # HDD
                                    storage_type = "HDD"
                                    storage_speed = "Slow"
                                break
                
                # Check for NVMe
                if os.path.exists('/dev/nvme0n1'):
                    storage_type = "NVMe SSD"
                    storage_speed = "Very Fast"
            except:
                pass
        elif platform.system() == 'Darwin':
            try:
                result = subprocess.run(['system_profiler', 'SPStorageDataType'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    if 'Solid State' in result.stdout:
                        storage_type = "SSD"
                        storage_speed = "Fast"
                    elif 'NVMe' in result.stdout:
                        storage_type = "NVMe SSD"
                        storage_speed = "Very Fast"
                    else:
                        storage_type = "HDD"
                        storage_speed = "Slow"
            except:
                pass
        elif platform.system() == 'Windows':
            try:
                result = subprocess.run(['wmic', 'diskdrive', 'get', 'model,mediatype', '/value'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    if 'SSD' in result.stdout or 'Solid State' in result.stdout:
                        storage_type = "SSD"
                        storage_speed = "Fast"
                    elif 'NVMe' in result.stdout:
                        storage_type = "NVMe SSD"
                        storage_speed = "Very Fast"
                    else:
                        storage_type = "HDD"
                        storage_speed = "Slow"
            except:
                pass
        
        return {
            'total_gb': total_gb,
            'free_gb': free_gb,
            'type': storage_type,
            'speed': storage_speed
        }
    except Exception as e:
        return {
            'total_gb': 100,
            'free_gb': 50,
            'type': 'Unknown',
            'speed': 'Unknown'
        }

def get_memory_info():
    """Get detailed memory information"""
    try:
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        
        return {
            'total_gb': total_gb,
            'available_gb': available_gb,
            'used_percent': memory.percent
        }
    except Exception as e:
        return {
            'total_gb': 4,
            'available_gb': 2,
            'used_percent': 50
        }

def rank_hardware_performance(cpu_info, memory_info, storage_info):
    """Rank hardware performance and provide recommendations"""
    print_section("🔧 Hardware Performance Analysis")
    
    # CPU Ranking
    cpu_cores = cpu_info['physical_cores']
    cpu_score = 0
    cpu_rating = "Poor"
    
    if cpu_cores >= 16:
        cpu_score = 100
        cpu_rating = "Excellent"
    elif cpu_cores >= 8:
        cpu_score = 80
        cpu_rating = "Very Good"
    elif cpu_cores >= 4:
        cpu_score = 60
        cpu_rating = "Good"
    elif cpu_cores >= 2:
        cpu_score = 40
        cpu_rating = "Fair"
    else:
        cpu_score = 20
        cpu_rating = "Poor"
    
    print(f"{Colors.CYAN}CPU Performance:{Colors.END}")
    print(f"  • Cores: {cpu_cores} physical, {cpu_info['logical_cores']} logical")
    print(f"  • Model: {cpu_info['model']}")
    print(f"  • Rating: {cpu_rating} ({cpu_score}/100)")
    print()
    
    # Memory Ranking
    total_memory = memory_info['total_gb']
    memory_score = 0
    memory_rating = "Poor"
    
    if total_memory >= 64:
        memory_score = 100
        memory_rating = "Excellent"
    elif total_memory >= 32:
        memory_score = 90
        memory_rating = "Very Good"
    elif total_memory >= 16:
        memory_score = 70
        memory_rating = "Good"
    elif total_memory >= 8:
        memory_score = 50
        memory_rating = "Fair"
    elif total_memory >= 4:
        memory_score = 30
        memory_rating = "Poor"
    else:
        memory_score = 10
        memory_rating = "Very Poor"
    
    print(f"{Colors.CYAN}Memory Performance:{Colors.END}")
    print(f"  • Total: {total_memory:.1f}GB")
    print(f"  • Available: {memory_info['available_gb']:.1f}GB")
    print(f"  • Rating: {memory_rating} ({memory_score}/100)")
    print()
    
    # Storage Ranking
    storage_type = storage_info['type']
    storage_score = 0
    storage_rating = "Poor"
    
    if storage_type == "NVMe SSD":
        storage_score = 100
        storage_rating = "Excellent"
    elif storage_type == "SSD":
        storage_score = 80
        storage_rating = "Very Good"
    elif storage_type == "HDD":
        storage_score = 40
        storage_rating = "Fair"
    else:
        storage_score = 20
        storage_rating = "Poor"
    
    print(f"{Colors.CYAN}Storage Performance:{Colors.END}")
    print(f"  • Type: {storage_type}")
    print(f"  • Speed: {storage_info['speed']}")
    print(f"  • Free Space: {storage_info['free_gb']:.1f}GB")
    print(f"  • Rating: {storage_rating} ({storage_score}/100)")
    print()
    
    # Overall Performance Score
    overall_score = (cpu_score + memory_score + storage_score) / 3
    overall_rating = "Poor"
    
    if overall_score >= 90:
        overall_rating = "Excellent"
    elif overall_score >= 75:
        overall_rating = "Very Good"
    elif overall_score >= 60:
        overall_rating = "Good"
    elif overall_score >= 45:
        overall_rating = "Fair"
    else:
        overall_rating = "Poor"
    
    print(f"{Colors.PURPLE}{Colors.BOLD}Overall Hardware Rating: {overall_rating} ({overall_score:.0f}/100){Colors.END}")
    print()
    
    # Performance Tier Recommendations
    print(f"{Colors.YELLOW}Performance Tier Recommendations:{Colors.END}")
    
    if overall_score >= 90:
        print(f"  {Colors.GREEN}🚀 Excellent: Can handle 10+ BPS (Blocks Per Second){Colors.END}")
        print(f"     • Recommended for high-performance nodes")
        print(f"     • Suitable for mining and high-throughput operations")
    elif overall_score >= 75:
        print(f"  {Colors.GREEN}⚡ Very Good: Can handle 5-10 BPS{Colors.END}")
        print(f"     • Recommended for production nodes")
        print(f"     • Good for most use cases")
    elif overall_score >= 60:
        print(f"  {Colors.YELLOW}✅ Good: Can handle 1-5 BPS{Colors.END}")
        print(f"     • Suitable for standard nodes")
        print(f"     • Good for development and testing")
    elif overall_score >= 45:
        print(f"  {Colors.YELLOW}⚠️  Fair: Can handle 1 BPS{Colors.END}")
        print(f"     • Minimum for basic node operation")
        print(f"     • May experience performance issues")
    else:
        print(f"  {Colors.RED}❌ Poor: Not recommended for production{Colors.END}")
        print(f"     • Consider upgrading hardware")
        print(f"     • May not sync properly")
    
    print()
    
    # Specific Recommendations
    print(f"{Colors.CYAN}Hardware Recommendations:{Colors.END}")
    
    if cpu_cores < 4:
        print(f"  • {Colors.RED}Consider upgrading to 4+ CPU cores{Colors.END}")
    if total_memory < 8:
        print(f"  • {Colors.RED}Consider upgrading to 8GB+ RAM{Colors.END}")
    if storage_type == "HDD":
        print(f"  • {Colors.RED}Consider upgrading to SSD or NVMe for better performance{Colors.END}")
    if storage_info['free_gb'] < 50:
        print(f"  • {Colors.RED}Consider freeing up disk space (need 50GB+){Colors.END}")
    
    if overall_score >= 60:
        print(f"  • {Colors.GREEN}Your hardware is suitable for running a Kaspa node{Colors.END}")
    
    print()
    
    return overall_score >= 45  # Return True if hardware is adequate

def check_memory():
    """Check available system memory"""
    try:
        memory_info = get_memory_info()
        
        # Require at least 2GB available memory
        required_gb = 2
        if memory_info['available_gb'] >= required_gb:
            print_check("System Memory", True, f"{memory_info['available_gb']:.1f}GB available (>= {required_gb}GB required)")
            return True
        else:
            print_check("System Memory", False, f"{memory_info['available_gb']:.1f}GB available (requires >= {required_gb}GB)")
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
    
    # Get hardware information
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    storage_info = get_storage_info()
    
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
    
    # Run hardware performance analysis
    hardware_adequate = rank_hardware_performance(cpu_info, memory_info, storage_info)
    results['Hardware'] = hardware_adequate
    
    # Generate report
    success = generate_report(results)
    
    print(f"\n{Colors.BLUE}For more information, visit: https://github.com/KaspaDev/Rusty-Kaspa-Docker{Colors.END}")
    print(f"{Colors.BLUE}Developed by KaspaDev (KRCBOT){Colors.END}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
