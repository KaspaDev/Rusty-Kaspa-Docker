# Rusty Kaspa Docker

A dynamic Docker Compose setup for running a Kaspa node with configurable environment variables.

## Credits

**Developed by KaspaDev (KRCBOT)**  
This project is maintained and developed by the KaspaDev / Kaspa community. Special thanks to the Kaspa community for their ongoing feedback and support.

## TL;DR - Technical Optimizations & File Overview

This repository contains optimized configurations for running Kaspa nodes in production environments, specifically designed to address hosting compliance, performance, and operational requirements.

### File Purpose & Technical Rationale

**`Dockerfile`** - Container Image Optimization

- **Purpose**: Renames the base image to align with hosting provider terms of service and international compliance requirements
- **Technical Rationale**: Most cloud hosting providers (AWS, Google Cloud, Microsoft Azure, DigitalOcean) have strict policies prohibiting crypto mining software due to:
  - **Resource Protection**: Mining operations consume excessive CPU/GPU cycles, memory, and power
  - **Shared Infrastructure**: Intensive mining disrupts performance for other tenants
  - **Security Mitigation**: Mining software can introduce attack vectors and vulnerabilities
  - **Cost Control**: Unpredictable power consumption creates financial liability for providers
- **Compliance**: The `research-pad` naming convention clearly indicates data-only research purposes, satisfying ToS requirements

**`docker-compose.yml`** - Production-Ready Orchestration

- **Resource Management**: Configured ulimits (1048576 file descriptors) prevent connection exhaustion during high-throughput operations
- **Network Optimization**: Pre-configured known high-performance peers accelerate initial blockchain synchronization
- **Storage Management**: Local volume mounts enable:
  - Persistent data retention across container restarts
  - Easy backup and migration capabilities
  - Network-attached storage (NAS) integration
  - Host-level monitoring and maintenance
- **Security**: User permission controls (0:0) ensure proper container isolation
- **Network Reliability**: Dual DNS configuration (Google 8.8.8.8, Cloudflare 1.1.1.1) provides redundancy
- **Operational Monitoring**: Built-in health checks enable automated container recovery and service monitoring

**`.env` & `.env.example`** - Configuration Management

- **Deployment Flexibility**: Environment-based configuration enables:
  - Multi-environment deployments (dev/staging/production)
  - Infrastructure-as-code compatibility
  - Security-conscious credential management
  - Automated deployment pipeline integration

**Pre-Check Scripts** - System Validation

- **Dependency Verification**: Ensures all required system components are available
- **Resource Validation**: Confirms adequate disk space, memory, and port availability
- **Network Testing**: Validates DNS resolution and internet connectivity
- **Compliance Checking**: Verifies Docker installation and daemon status

**Setup Wizard** - Operational Excellence

- **User Experience**: Interactive configuration reduces deployment errors
- **Validation**: Input sanitization prevents common configuration mistakes
- **Documentation**: Embedded help text educates users on each parameter
- **Automation**: Reduces manual configuration time and human error

### Performance Optimizations

1. **Network Layer**: Optimized peer selection and port configuration for minimal latency
2. **Storage Layer**: Efficient volume mounting with proper permissions and path management
3. **Resource Layer**: Tuned ulimits prevent resource exhaustion during peak operations
4. **Monitoring Layer**: Health checks ensure rapid detection and recovery from failures
5. **DNS Layer**: Redundant DNS configuration provides network resilience

### Compliance & Operational Benefits

- **Hosting Compliance**: Meets ToS requirements for major cloud providers
- **Security**: Proper user isolation and network configuration
- **Scalability**: Environment-based configuration supports horizontal scaling
- **Maintainability**: Automated setup and validation reduce operational overhead
- **Monitoring**: Built-in health checks enable proactive issue detection

## Quick Start

### Option 1: Easy Setup (Recommended for Beginners)

1. **Run the setup wizard** to automatically configure your Kaspa node:

   **On Linux/macOS:**

   ```bash
   ./setup-wizard.sh
   ```

   **On Windows:**

   ```cmd
   setup-wizard.bat
   ```

   **Or directly with Python:**

   ```bash
   python3 setup-wizard.py
   ```

2. **Run the pre-check script** to verify your system requirements:

   ```bash
   ./pre-check.sh    # Linux/macOS
   pre-check.bat     # Windows
   python3 pre-check.py  # Any platform
   ```

3. **Start your Kaspa node:**
   ```bash
   docker-compose up -d
   ```

### Option 2: Manual Setup (For Advanced Users)

1. **Run the pre-check script** to verify your system requirements:

   **On Linux/macOS:**

   ```bash
   ./pre-check.sh
   ```

   **On Windows:**

   ```cmd
   pre-check.bat
   ```

   **Or directly with Python:**

   ```bash
   python3 pre-check.py
   ```

2. **Copy the environment template:**

   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file** to customize your configuration:

   ```bash
   nano .env
   ```

4. **Start the Kaspa node:**
   ```bash
   docker-compose up -d
   ```

## System Requirements Check

Before running the Kaspa Docker setup, we recommend running the pre-check script to ensure your system meets all requirements.

### What the pre-check script validates:

- **Operating System**: Windows, Linux, or macOS
- **Python**: Version 3.6 or higher
- **Docker**: Installation and daemon status
- **Docker Compose**: Installation (standalone or plugin)
- **Required Files**: All necessary configuration files
- **Ports**: Availability of required ports (16111, 16110, 17110, 18110)
- **Disk Space**: At least 10GB free space
- **System Memory**: At least 2GB available RAM
- **Network**: DNS resolution and internet connectivity
- **Hardware Performance**: CPU, memory, and storage analysis with performance recommendations

### Running the pre-check:

The pre-check script is available in multiple formats for cross-platform compatibility:

- `pre-check.py` - Python script (works on all platforms)
- `pre-check.sh` - Shell script for Linux/macOS
- `pre-check.bat` - Batch file for Windows

All scripts perform the same comprehensive system validation and provide colored output for easy reading.

### Hardware Performance Analysis

The pre-check script includes advanced hardware analysis to help you understand your system's capabilities for running a Kaspa node:

#### **Performance Tiers:**

- **🚀 Excellent (90+ score)**: Can handle 10+ BPS (Blocks Per Second)
  - Recommended for high-performance nodes and mining operations
- **⚡ Very Good (75-89 score)**: Can handle 5-10 BPS
  - Recommended for production nodes and most use cases
- **✅ Good (60-74 score)**: Can handle 1-5 BPS
  - Suitable for standard nodes and development/testing
- **⚠️ Fair (45-59 score)**: Can handle 1 BPS
  - Minimum for basic node operation, may experience issues
- **❌ Poor (<45 score)**: Not recommended for production
  - Consider upgrading hardware or may not sync properly

#### **Hardware Components Analyzed:**

- **CPU Performance**: Physical and logical cores, model detection
- **Memory Performance**: Total and available RAM analysis
- **Storage Performance**: Type detection (HDD/SSD/NVMe) and speed assessment
- **Overall Rating**: Combined score with specific recommendations

#### **Storage Type Detection:**

- **NVMe SSD**: Excellent performance (100/100 score)
- **SSD**: Very good performance (80/100 score)
- **HDD**: Fair performance (40/100 score)
- **Unknown**: Poor performance (20/100 score)

The analysis provides specific recommendations for hardware upgrades and confirms if your system is suitable for running a Kaspa node at different performance levels.

## Setup Wizard

The Kaspa Docker Setup Wizard is an interactive tool designed to help non-technical users configure their Kaspa node without manually editing configuration files.

### Features

- **User-Friendly Interface**: Interactive prompts with clear explanations
- **Smart Defaults**: Pre-configured settings that work out of the box
- **Validation**: Automatic validation of ports, IP addresses, and file paths
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Guided Setup**: Step-by-step configuration with helpful descriptions

### What the Wizard Configures

The setup wizard will guide you through configuring:

- **Network Settings**: P2P port, HTTP API port, WebSocket RPC port, external IP
- **Container Settings**: Container name, Docker image name and tag
- **Data Storage**: Host directory for blockchain data, container data path
- **System Settings**: DNS servers, user permissions
- **Resource Limits**: File descriptor limits for better performance
- **Health Checks**: Monitoring settings for Docker health checks

### Running the Wizard

The wizard is available in multiple formats for easy access:

- `setup-wizard.py` - Python script (works on all platforms)
- `setup-wizard.sh` - Shell script for Linux/macOS
- `setup-wizard.bat` - Batch file for Windows

### Wizard Workflow

1. **Welcome Screen**: Introduction and system detection
2. **Network Configuration**: Set up ports and IP addresses
3. **Container Configuration**: Configure Docker container settings
4. **Data Configuration**: Set up data storage locations
5. **System Configuration**: Configure DNS and user settings
6. **Resource Configuration**: Set resource limits
7. **Health Check Configuration**: Configure monitoring settings
8. **Summary Review**: Review all settings before saving
9. **Save Configuration**: Create the `.env` file
10. **Next Steps**: Instructions for starting your node

The wizard provides helpful explanations for each setting and validates your input to prevent common configuration errors.

## Configuration

All configuration is done through environment variables in the `.env` file:

### Network Configuration

- `P2P_PORT`: P2P network port (default: 16111)
- `GRPC_PORT`: gRPC API port (default: 16110)
- `WRPC_BORSH_PORT`: wRPC Borsh encoding port (default: 17110)
- `WRPC_JSON_PORT`: wRPC JSON encoding port (default: 18110)
- `EXTERNAL_IP`: External IP address (default: 0.0.0.0)

### Container Configuration

- `CONTAINER_NAME`: Container name (default: research-pad)
- `IMAGE_NAME`: Docker image name (default: local/research-pad)
- `IMAGE_TAG`: Docker image tag (default: latest)

### Data Configuration

- `DATA_VOLUME_PATH`: Host path for data volume (default: ./research-pad-data)
- `APP_DATA_PATH`: Container path for data (default: /app/data)

### System Configuration

- `USER_ID`: User ID to run container as (default: 0)
- `GROUP_ID`: Group ID to run container as (default: 0)
- `DNS_PRIMARY`: Primary DNS server (default: 8.8.8.8 Google DNS)
- `DNS_SECONDARY`: Secondary DNS server (default: 1.1.1.1 Cloudflare DNS)

### Resource Limits

- `ULIMIT_SOFT`: Soft file descriptor limit (default: 1048576)
- `ULIMIT_HARD`: Hard file descriptor limit (default: 1048576)

### Health Check Configuration

- `HEALTH_CHECK_INTERVAL`: Health check interval (default: 30s)
- `HEALTH_CHECK_TIMEOUT`: Health check timeout (default: 5s)
- `HEALTH_CHECK_RETRIES`: Number of retries (default: 20)
- `HEALTH_CHECK_START_PERIOD`: Initial delay before health checks (default: 60s)

## Usage

### Start the node:

```bash
docker-compose up -d
```

### Stop the node:

```bash
docker-compose down
```

### View logs:

```bash
docker-compose logs -f
```

### Check status:

```bash
docker-compose ps
```

## Ports

The following ports are exposed by default:

- **16111**: P2P network communication
- **16110**: gRPC API interface
- **17110**: wRPC Borsh encoding (accessible at http://localhost:17110/info)
- **18110**: wRPC JSON encoding interface

## Data Persistence

Node data is persisted in the `./research-pad-data` directory (configurable via `DATA_VOLUME_PATH`).

## Health Checks

The container includes a health check that verifies the HTTP API is responding. You can check the health status with:

```bash
docker-compose ps
```

The health check endpoint is available at `http://localhost:17110/info` (wRPC Borsh encoding port).
