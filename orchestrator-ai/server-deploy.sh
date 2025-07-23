#!/bin/bash

# Orchestrator AI Server Deployment Script
# Run this on your server at 206.81.0.22

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SERVER_IP="206.81.0.22"
PROJECT_DIR="/root/orchestrator-ai"
APP_DIR="${PROJECT_DIR}/app"

echo -e "${BLUE}🚀 Orchestrator AI Server Deployment${NC}"
echo "========================================"

print_status() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }

# Check if we're running as root
check_permissions() {
    if [ "$EUID" -ne 0 ]; then
        print_error "Please run as root or with sudo"
        exit 1
    fi
    print_status "Running with proper permissions"
}

# Install Docker if not present
install_docker() {
    if ! command -v docker &> /dev/null; then
        print_info "Installing Docker..."
        
        # Update packages
        apt-get update
        apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
        
        # Add Docker's official GPG key
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        
        # Set up stable repository
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        # Install Docker
        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        
        # Start and enable Docker
        systemctl start docker
        systemctl enable docker
        
        print_status "Docker installed successfully"
    else
        print_status "Docker is already installed"
    fi
}

# Install Docker Compose if not present
install_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_info "Installing Docker Compose..."
        
        # Install docker-compose
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        
        print_status "Docker Compose installed successfully"
    else
        print_status "Docker Compose is already available"
    fi
}

# Install required packages
install_dependencies() {
    print_info "Installing system dependencies..."
    
    apt-get update
    apt-get install -y \
        curl \
        wget \
        git \
        unzip \
        nginx \
        openssl \
        postgresql-client \
        redis-tools
    
    print_status "Dependencies installed"
}

# Setup project directory
setup_project() {
    print_info "Setting up project directory..."
    
    # Create project directory if it doesn't exist
    mkdir -p $PROJECT_DIR
    cd $PROJECT_DIR
    
    # If orchestrator-ai directory doesn't exist, we need the code
    if [ ! -d "orchestrator-ai" ]; then
        print_error "orchestrator-ai directory not found in $PROJECT_DIR"
        print_info "Please ensure the code is uploaded to $PROJECT_DIR/orchestrator-ai"
        exit 1
    fi
    
    cd $APP_DIR
    print_status "Project directory ready"
}

# Create environment file
create_environment() {
    print_info "Creating environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        
        # Generate secure secrets
        NEXTAUTH_SECRET=$(openssl rand -base64 32)
        POSTGRES_PASSWORD=$(openssl rand -base64 16)
        REDIS_PASSWORD=$(openssl rand -base64 16)
        API_KEY=$(openssl rand -base64 24)
        
        # Update environment file
        sed -i "s|NEXTAUTH_URL=.*|NEXTAUTH_URL=http://${SERVER_IP}:3000|g" .env
        sed -i "s|NEXTAUTH_SECRET=.*|NEXTAUTH_SECRET=${NEXTAUTH_SECRET}|g" .env
        sed -i "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=${POSTGRES_PASSWORD}|g" .env
        sed -i "s|REDIS_CACHE_PASSWORD=.*|REDIS_CACHE_PASSWORD=${REDIS_PASSWORD}|g" .env
        sed -i "s|API_KEY=.*|API_KEY=${API_KEY}|g" .env
        sed -i "s|DEPLOY_HOST=.*|DEPLOY_HOST=${SERVER_IP}|g" .env
        
        print_status "Environment file created with secure secrets"
        print_warning "Please edit .env file and add your OPENAI_API_KEY"
    else
        print_status "Environment file already exists"
    fi
}

# Build backend image (if orchestrator backend exists)
build_backend() {
    print_info "Checking for backend..."
    
    if [ -d "../orchestrator" ]; then
        print_info "Building backend image..."
        cd ../orchestrator
        
        # Create Dockerfile for backend if it doesn't exist
        if [ ! -f "Dockerfile" ]; then
            cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Start the application
CMD ["python", "orchestrator.py"]
EOF
        fi
        
        docker build -t orchestrator-backend:latest .
        cd $APP_DIR
        print_status "Backend image built"
    else
        print_warning "Backend directory not found, skipping backend build"
    fi
}

# Setup firewall
setup_firewall() {
    print_info "Configuring firewall..."
    
    # Install ufw if not present
    if ! command -v ufw &> /dev/null; then
        apt-get install -y ufw
    fi
    
    # Configure firewall rules
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    
    # SSH
    ufw allow 22/tcp
    
    # HTTP and HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Application ports
    ufw allow 3000/tcp
    ufw allow 8001/tcp
    
    # Enable firewall
    ufw --force enable
    
    print_status "Firewall configured"
}

# Deploy application
deploy_application() {
    print_info "Deploying application..."
    
    # Make deploy script executable
    chmod +x deploy.sh
    
    # Run deployment
    ./deploy.sh --clean
    
    print_status "Application deployed"
}

# Setup systemd service for auto-restart
setup_systemd() {
    print_info "Setting up systemd service..."
    
    cat > /etc/systemd/system/orchestrator-ai.service << EOF
[Unit]
Description=Orchestrator AI Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=${APP_DIR}
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable orchestrator-ai.service
    
    print_status "Systemd service configured"
}

# Setup log rotation
setup_logging() {
    print_info "Setting up log rotation..."
    
    cat > /etc/logrotate.d/orchestrator-ai << EOF
/var/lib/docker/containers/*/*-json.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
    postrotate
        /bin/kill -USR1 \$(cat /var/run/docker.pid 2>/dev/null) 2>/dev/null || true
    endscript
}
EOF

    print_status "Log rotation configured"
}

# Health check
final_health_check() {
    print_info "Performing final health check..."
    
    sleep 30  # Wait for services to start
    
    # Check if containers are running
    if docker ps | grep -q orchestrator-frontend; then
        print_status "Frontend container is running"
    else
        print_error "Frontend container is not running"
    fi
    
    # Check if application is accessible
    if curl -f http://localhost:3000/api/health >/dev/null 2>&1; then
        print_status "Application health check passed"
    else
        print_warning "Application health check failed, but deployment completed"
    fi
    
    # Check if nginx is running
    if docker ps | grep -q orchestrator-nginx; then
        print_status "Nginx proxy is running"
    else
        print_warning "Nginx proxy is not running"
    fi
}

# Show final status
show_final_status() {
    echo ""
    echo "=============================================="
    print_status "🎉 Deployment Completed Successfully!"
    echo "=============================================="
    echo ""
    echo -e "${BLUE}📱 Access your application:${NC}"
    echo "   • Frontend: http://${SERVER_IP}:3000"
    echo "   • Proxy:    http://${SERVER_IP}:80"
    echo "   • Health:   http://${SERVER_IP}:3000/api/health"
    echo ""
    echo -e "${BLUE}🔧 Management commands:${NC}"
    echo "   • Check status:   docker ps"
    echo "   • View logs:      docker-compose logs -f"
    echo "   • Restart:        systemctl restart orchestrator-ai"
    echo "   • Stop:           systemctl stop orchestrator-ai"
    echo ""
    echo -e "${BLUE}📂 Important files:${NC}"
    echo "   • Project:        ${PROJECT_DIR}"
    echo "   • App:            ${APP_DIR}"
    echo "   • Environment:    ${APP_DIR}/.env"
    echo "   • Logs:           docker-compose logs"
    echo ""
    print_warning "Don't forget to:"
    echo "   1. Add your OPENAI_API_KEY to .env file"
    echo "   2. Configure SSL certificates if needed"
    echo "   3. Set up domain name if applicable"
    echo ""
}

# Error handling
handle_error() {
    print_error "Deployment failed!"
    echo ""
    print_info "Troubleshooting:"
    echo "1. Check Docker status: systemctl status docker"
    echo "2. Check logs: docker-compose logs"
    echo "3. Check disk space: df -h"
    echo "4. Check memory: free -h"
    echo ""
    exit 1
}

# Set error trap
trap 'handle_error' ERR

# Main deployment process
main() {
    check_permissions
    install_dependencies
    install_docker
    install_docker_compose
    setup_project
    create_environment
    build_backend
    setup_firewall
    deploy_application
    setup_systemd
    setup_logging
    final_health_check
    show_final_status
}

# Run deployment
main

print_status "🎯 Server deployment completed! Your Orchestrator AI is now running!"