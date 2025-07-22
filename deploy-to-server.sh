#!/bin/bash

# Deployment script for NextJS Orchestrator AI application
# Usage: ./deploy-to-server.sh

set -e

echo "🚀 Starting deployment to server..."

# Configuration
SERVER_IP="206.81.0.227"
SERVER_USER="root"
SSH_KEY="~/.ssh/id_rsa"
APP_DIR="/root/orchestrator-ai"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa ]; then
    print_error "SSH key not found at ~/.ssh/id_rsa"
    exit 1
fi

print_status "Testing SSH connection..."
if ! ssh -i "$SSH_KEY" -o ConnectTimeout=10 "$SERVER_USER@$SERVER_IP" "echo 'SSH connection successful'"; then
    print_error "Failed to connect to server. Please check your SSH key and server access."
    exit 1
fi

print_status "SSH connection successful!"

# Function to run commands on remote server
run_remote() {
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "$1"
}

# Function to copy files to remote server
copy_to_remote() {
    scp -i "$SSH_KEY" -r "$1" "$SERVER_USER@$SERVER_IP:$2"
}

print_status "Installing prerequisites on server..."
run_remote "
    # Update system
    apt-get update

    # Install Docker if not installed
    if ! command -v docker &> /dev/null; then
        echo 'Installing Docker...'
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl start docker
        systemctl enable docker
    fi

    # Install Docker Compose if not installed
    if ! command -v docker-compose &> /dev/null; then
        echo 'Installing Docker Compose...'
        curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi

    # Install Node.js and npm if not installed
    if ! command -v node &> /dev/null; then
        echo 'Installing Node.js...'
        curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
        apt-get install -y nodejs
    fi

    echo 'Prerequisites installed successfully!'
"

print_status "Creating application directory on server..."
run_remote "mkdir -p $APP_DIR"

print_status "Copying application files to server..."
copy_to_remote "orchestrator-ai/" "/root/"

print_status "Setting up environment configuration..."
run_remote "
    cd $APP_DIR/app
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        cp env.example .env
        echo 'Created .env file from env.example'
        echo 'Please update the environment variables in .env file'
    fi
"

print_status "Building and starting the application..."
run_remote "
    cd $APP_DIR/app
    
    # Stop any existing containers
    docker-compose down || true
    
    # Build and start the application
    docker-compose up -d --build
    
    # Wait for services to be ready
    echo 'Waiting for services to start...'
    sleep 30
    
    # Check if services are running
    docker-compose ps
"

print_status "Checking application health..."
if run_remote "curl -f http://localhost:3000 > /dev/null 2>&1"; then
    print_status "✅ Application is running successfully!"
    print_status "🌐 Access your application at: http://$SERVER_IP:3000"
else
    print_warning "Application might still be starting. Check logs with:"
    echo "ssh -i $SSH_KEY $SERVER_USER@$SERVER_IP 'cd $APP_DIR/app && docker-compose logs'"
fi

print_status "Deployment completed!"
print_status "Useful commands:"
echo "  - Check logs: ssh -i $SSH_KEY $SERVER_USER@$SERVER_IP 'cd $APP_DIR/app && docker-compose logs'"
echo "  - Restart app: ssh -i $SSH_KEY $SERVER_USER@$SERVER_IP 'cd $APP_DIR/app && docker-compose restart'"
echo "  - Stop app: ssh -i $SSH_KEY $SERVER_USER@$SERVER_IP 'cd $APP_DIR/app && docker-compose down'"
echo "  - Update app: ./deploy-to-server.sh"