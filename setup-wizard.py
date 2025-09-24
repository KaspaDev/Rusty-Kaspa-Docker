#!/usr/bin/env python3
"""
Kaspa Docker Setup Wizard
Developed by KaspaDev (KRCBOT)

Interactive wizard to help non-technical users configure their .env file
for running Kaspa Docker. Works on Windows, Linux, and macOS.
"""

import os
import sys
import platform
import socket
import json
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the wizard header"""
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("        🚀 Kaspa Docker Setup Wizard 🚀")
    print("        Developed by KaspaDev (KRCBOT)")
    print("=" * 70)
    print(f"{Colors.END}")
    print(f"{Colors.YELLOW}Welcome! This wizard will help you configure your Kaspa node.{Colors.END}")
    print(f"{Colors.YELLOW}Press Enter to use default values (recommended for beginners).{Colors.END}")
    print()

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{Colors.UNDERLINE}{title}{Colors.END}")
    print("-" * len(title))

def get_input(prompt, default=None, validator=None):
    """Get user input with optional default and validation"""
    while True:
        if default:
            full_prompt = f"{prompt} [{default}]: "
        else:
            full_prompt = f"{prompt}: "
        
        user_input = input(full_prompt).strip()
        
        # Use default if no input provided
        if not user_input and default:
            return default
        
        # Validate input if validator provided
        if validator:
            try:
                return validator(user_input)
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
                continue
        
        return user_input

def validate_port(port_str):
    """Validate port number"""
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return str(port)
        else:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError:
        raise ValueError("Please enter a valid port number")

def validate_ip(ip_str):
    """Validate IP address"""
    try:
        socket.inet_aton(ip_str)
        return ip_str
    except socket.error:
        raise ValueError("Please enter a valid IP address")

def validate_path(path_str):
    """Validate directory path"""
    if not path_str:
        raise ValueError("Path cannot be empty")
    
    # Convert to Path object for cross-platform compatibility
    path = Path(path_str)
    
    # Check if parent directory exists
    if not path.parent.exists():
        raise ValueError(f"Parent directory does not exist: {path.parent}")
    
    return str(path)

def check_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.bind(('127.0.0.1', int(port)))
            return True
    except OSError:
        return False

def get_system_info():
    """Get system information for recommendations"""
    system = platform.system()
    
    # Default data directory based on OS
    if system == 'Windows':
        default_data_dir = r".\kaspa-data"
    else:
        default_data_dir = "./kaspa-data"
    
    # Get local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "0.0.0.0"
    
    return {
        'os': system,
        'default_data_dir': default_data_dir,
        'local_ip': local_ip
    }

def network_configuration():
    """Configure network settings"""
    print_section("🌐 Network Configuration")
    
    print(f"{Colors.YELLOW}Network settings control how your Kaspa node communicates.{Colors.END}")
    print(f"{Colors.YELLOW}The default ports are standard for Kaspa nodes.{Colors.END}")
    
    system_info = get_system_info()
    
    # P2P Port
    print(f"\n{Colors.CYAN}P2P Port{Colors.END}")
    print("This port is used for peer-to-peer communication with other Kaspa nodes.")
    p2p_port = get_input("Enter P2P port", "16111", validate_port)
    
    # gRPC Port
    print(f"\n{Colors.CYAN}gRPC Port{Colors.END}")
    print("This port provides gRPC API access to your node (Mainnet: 16110).")
    grpc_port = get_input("Enter gRPC port", "16110", validate_port)
    
    # wRPC Borsh Port
    print(f"\n{Colors.CYAN}wRPC Borsh Encoding Port{Colors.END}")
    print("This port provides wRPC with Borsh encoding (Mainnet: 17110).")
    wrpc_borsh_port = get_input("Enter wRPC Borsh port", "17110", validate_port)
    
    # wRPC JSON Port
    print(f"\n{Colors.CYAN}wRPC JSON Encoding Port{Colors.END}")
    print("This port provides wRPC with JSON encoding (Mainnet: 18110).")
    wrpc_json_port = get_input("Enter wRPC JSON port", "18110", validate_port)
    
    # External IP
    print(f"\n{Colors.CYAN}External IP Address{Colors.END}")
    print(f"Your detected local IP is: {system_info['local_ip']}")
    print("Use 0.0.0.0 to accept connections from any IP, or specify your local IP.")
    external_ip = get_input("Enter external IP", "0.0.0.0", validate_ip)
    
    # Check port availability
    print(f"\n{Colors.YELLOW}Checking port availability...{Colors.END}")
    ports = [p2p_port, grpc_port, wrpc_borsh_port, wrpc_json_port]
    unavailable_ports = []
    
    for port in ports:
        if not check_port_available(port):
            unavailable_ports.append(port)
    
    if unavailable_ports:
        print(f"{Colors.RED}Warning: The following ports are already in use: {', '.join(unavailable_ports)}{Colors.END}")
        print(f"{Colors.YELLOW}You may need to change these ports or stop other services using them.{Colors.END}")
        response = get_input("Continue anyway? (y/N)", "N")
        if response.lower() != 'y':
            return network_configuration()
    
    return {
        'P2P_PORT': p2p_port,
        'GRPC_PORT': grpc_port,
        'WRPC_BORSH_PORT': wrpc_borsh_port,
        'WRPC_JSON_PORT': wrpc_json_port,
        'EXTERNAL_IP': external_ip
    }

def container_configuration():
    """Configure container settings"""
    print_section("🐳 Container Configuration")
    
    print(f"{Colors.YELLOW}Container settings control how your Docker container runs.{Colors.END}")
    
    # Container Name
    print(f"\n{Colors.CYAN}Container Name{Colors.END}")
    print("This is the name of your Docker container (must be unique).")
    container_name = get_input("Enter container name", "kaspa-node")
    
    # Image Name
    print(f"\n{Colors.CYAN}Docker Image Name{Colors.END}")
    print("This is the name of the Docker image (usually don't change this).")
    image_name = get_input("Enter image name", "local/research-pad")
    
    # Image Tag
    print(f"\n{Colors.CYAN}Docker Image Tag{Colors.END}")
    print("This is the version tag of the Docker image.")
    image_tag = get_input("Enter image tag", "latest")
    
    return {
        'CONTAINER_NAME': container_name,
        'IMAGE_NAME': image_name,
        'IMAGE_TAG': image_tag
    }

def data_configuration():
    """Configure data storage settings"""
    print_section("💾 Data Storage Configuration")
    
    print(f"{Colors.YELLOW}Data settings control where your Kaspa node stores its data.{Colors.END}")
    
    system_info = get_system_info()
    
    # Data Volume Path
    print(f"\n{Colors.CYAN}Data Directory{Colors.END}")
    print("This is where your Kaspa node will store its blockchain data.")
    print(f"Recommended: {system_info['default_data_dir']}")
    data_volume_path = get_input("Enter data directory path", system_info['default_data_dir'])
    
    # App Data Path
    print(f"\n{Colors.CYAN}Container Data Path{Colors.END}")
    print("This is the path inside the container where data is stored (usually don't change).")
    app_data_path = get_input("Enter container data path", "/app/data")
    
    return {
        'DATA_VOLUME_PATH': data_volume_path,
        'APP_DATA_PATH': app_data_path
    }

def system_configuration():
    """Configure system settings"""
    print_section("⚙️ System Configuration")
    
    print(f"{Colors.YELLOW}System settings control resource usage and user permissions.{Colors.END}")
    
    # DNS Servers
    print(f"\n{Colors.CYAN}DNS Servers{Colors.END}")
    print("These DNS servers will be used by your Kaspa node for network lookups.")
    dns_primary = get_input("Enter primary DNS server", "8.8.8.8")
    dns_secondary = get_input("Enter secondary DNS server", "1.1.1.1")
    
    # User Configuration
    print(f"\n{Colors.CYAN}User Configuration{Colors.END}")
    print("User ID and Group ID for running the container (0 = root, usually don't change).")
    user_id = get_input("Enter user ID", "0")
    group_id = get_input("Enter group ID", "0")
    
    return {
        'DNS_PRIMARY': dns_primary,
        'DNS_SECONDARY': dns_secondary,
        'USER_ID': user_id,
        'GROUP_ID': group_id
    }

def resource_configuration():
    """Configure resource limits"""
    print_section("🔧 Resource Limits")
    
    print(f"{Colors.YELLOW}Resource limits control how much system resources your node can use.{Colors.END}")
    
    # File Descriptor Limits
    print(f"\n{Colors.CYAN}File Descriptor Limits{Colors.END}")
    print("These control how many files your node can have open simultaneously.")
    print("Higher values allow more connections but use more resources.")
    
    ulimit_soft = get_input("Enter soft file descriptor limit", "1048576")
    ulimit_hard = get_input("Enter hard file descriptor limit", "1048576")
    
    return {
        'ULIMIT_SOFT': ulimit_soft,
        'ULIMIT_HARD': ulimit_hard
    }

def health_check_configuration():
    """Configure health check settings"""
    print_section("❤️ Health Check Configuration")
    
    print(f"{Colors.YELLOW}Health check settings control how Docker monitors your node's health.{Colors.END}")
    
    # Health Check Settings
    print(f"\n{Colors.CYAN}Health Check Timing{Colors.END}")
    print("These settings control how often Docker checks if your node is healthy.")
    
    health_interval = get_input("Enter health check interval (e.g., 30s)", "30s")
    health_timeout = get_input("Enter health check timeout (e.g., 5s)", "5s")
    health_retries = get_input("Enter number of retries before marking unhealthy", "20")
    health_start_period = get_input("Enter start period before health checks begin (e.g., 60s)", "60s")
    
    return {
        'HEALTH_CHECK_INTERVAL': health_interval,
        'HEALTH_CHECK_TIMEOUT': health_timeout,
        'HEALTH_CHECK_RETRIES': health_retries,
        'HEALTH_CHECK_START_PERIOD': health_start_period
    }

def save_env_file(config):
    """Save configuration to .env file"""
    print_section("💾 Saving Configuration")
    
    env_content = """# Kaspa Node Configuration
# Generated by Kaspa Docker Setup Wizard
# Developed by KaspaDev (KRCBOT)

# Service Configuration
SERVICE_NAME=research-pad
CONTAINER_NAME={CONTAINER_NAME}
IMAGE_NAME={IMAGE_NAME}
IMAGE_TAG={IMAGE_TAG}

# Network Configuration
P2P_PORT={P2P_PORT}
GRPC_PORT={GRPC_PORT}
WRPC_BORSH_PORT={WRPC_BORSH_PORT}
WRPC_JSON_PORT={WRPC_JSON_PORT}
EXTERNAL_IP={EXTERNAL_IP}

# Data Configuration
DATA_VOLUME_PATH={DATA_VOLUME_PATH}
APP_DATA_PATH={APP_DATA_PATH}

# DNS Configuration
DNS_PRIMARY={DNS_PRIMARY}
DNS_SECONDARY={DNS_SECONDARY}

# User Configuration
USER_ID={USER_ID}
GROUP_ID={GROUP_ID}

# Resource Limits
ULIMIT_SOFT={ULIMIT_SOFT}
ULIMIT_HARD={ULIMIT_HARD}

# Health Check Configuration
HEALTH_CHECK_INTERVAL={HEALTH_CHECK_INTERVAL}
HEALTH_CHECK_TIMEOUT={HEALTH_CHECK_TIMEOUT}
HEALTH_CHECK_RETRIES={HEALTH_CHECK_RETRIES}
HEALTH_CHECK_START_PERIOD={HEALTH_CHECK_START_PERIOD}

# Peer Configuration (comma-separated list)
PEERS=51.79.24.82:16111,162.55.100.124:16111
""".format(**config)
    
    # Check if .env already exists
    if Path('.env').exists():
        response = get_input("A .env file already exists. Overwrite it? (y/N)", "N")
        if response.lower() != 'y':
            print(f"{Colors.YELLOW}Configuration not saved.{Colors.END}")
            return False
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"{Colors.GREEN}✓ Configuration saved to .env file!{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}Error saving configuration: {e}{Colors.END}")
        return False

def show_summary(config):
    """Show configuration summary"""
    print_section("📋 Configuration Summary")
    
    print(f"{Colors.CYAN}Your Kaspa node will be configured with:{Colors.END}")
    print()
    
    print(f"{Colors.YELLOW}Network Settings:{Colors.END}")
    print(f"  • P2P Port: {config['P2P_PORT']}")
    print(f"  • gRPC Port: {config['GRPC_PORT']}")
    print(f"  • wRPC Borsh Port: {config['WRPC_BORSH_PORT']}")
    print(f"  • wRPC JSON Port: {config['WRPC_JSON_PORT']}")
    print(f"  • External IP: {config['EXTERNAL_IP']}")
    print()
    
    print(f"{Colors.YELLOW}Container Settings:{Colors.END}")
    print(f"  • Container Name: {config['CONTAINER_NAME']}")
    print(f"  • Image: {config['IMAGE_NAME']}:{config['IMAGE_TAG']}")
    print()
    
    print(f"{Colors.YELLOW}Data Storage:{Colors.END}")
    print(f"  • Host Directory: {config['DATA_VOLUME_PATH']}")
    print(f"  • Container Path: {config['APP_DATA_PATH']}")
    print()
    
    print(f"{Colors.YELLOW}System Settings:{Colors.END}")
    print(f"  • DNS: {config['DNS_PRIMARY']}, {config['DNS_SECONDARY']}")
    print(f"  • User: {config['USER_ID']}:{config['GROUP_ID']}")
    print()

def show_next_steps():
    """Show next steps after configuration"""
    print_section("🚀 Next Steps")
    
    print(f"{Colors.GREEN}Great! Your Kaspa node is now configured.{Colors.END}")
    print()
    print(f"{Colors.YELLOW}To start your Kaspa node:{Colors.END}")
    print(f"  1. Run: {Colors.CYAN}docker-compose up -d{Colors.END}")
    print()
    print(f"{Colors.YELLOW}To check your node status:{Colors.END}")
    print(f"  1. Run: {Colors.CYAN}docker-compose ps{Colors.END}")
    print(f"  2. Run: {Colors.CYAN}docker-compose logs -f{Colors.END}")
    print()
    print(f"{Colors.YELLOW}To stop your node:{Colors.END}")
    print(f"  1. Run: {Colors.CYAN}docker-compose down{Colors.END}")
    print()
    print(f"{Colors.YELLOW}Your node will be accessible at:{Colors.END}")
    print(f"  • gRPC API: {Colors.CYAN}localhost:16110{Colors.END}")
    print(f"  • wRPC Borsh: {Colors.CYAN}ws://localhost:17110{Colors.END}")
    print(f"  • wRPC JSON: {Colors.CYAN}ws://localhost:18110{Colors.END}")
    print()
    print(f"{Colors.BLUE}For more help, visit: https://github.com/KaspaDev/Rusty-Kaspa-Docker{Colors.END}")
    print(f"{Colors.BLUE}Developed by KaspaDev (KRCBOT){Colors.END}")

def main():
    """Main wizard function"""
    try:
        print_header()
        
        # Check if we're in the right directory
        if not Path('docker-compose.yml').exists():
            print(f"{Colors.RED}Error: docker-compose.yml not found!{Colors.END}")
            print(f"{Colors.YELLOW}Please run this wizard from the Kaspa Docker directory.{Colors.END}")
            input("Press Enter to exit...")
            return 1
        
        # Run configuration sections
        config = {}
        
        # Network configuration
        config.update(network_configuration())
        
        # Container configuration
        config.update(container_configuration())
        
        # Data configuration
        config.update(data_configuration())
        
        # System configuration
        config.update(system_configuration())
        
        # Resource configuration
        config.update(resource_configuration())
        
        # Health check configuration
        config.update(health_check_configuration())
        
        # Show summary
        show_summary(config)
        
        # Confirm and save
        response = get_input("Save this configuration? (Y/n)", "Y")
        if response.lower() != 'n':
            if save_env_file(config):
                show_next_steps()
            else:
                print(f"{Colors.RED}Failed to save configuration.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}Configuration cancelled.{Colors.END}")
        
        input("\nPress Enter to exit...")
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
        return 1
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.END}")
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
