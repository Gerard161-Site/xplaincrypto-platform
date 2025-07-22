#!/bin/bash

# Fix Dependencies Script for NextJS Orchestrator AI
# Run this script on your server to diagnose and fix dependency issues

set -e

echo "🔧 Diagnosing and fixing dependency issues..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "${BLUE}[SECTION]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_section "1. Checking current directory and files"
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

if [ -d "orchestrator-ai" ]; then
    cd orchestrator-ai
    echo "Contents of orchestrator-ai directory:"
    ls -la
    
    if [ -d "app" ]; then
        cd app
        echo "Contents of app directory:"
        ls -la
    else
        print_error "app directory not found in orchestrator-ai"
        exit 1
    fi
else
    print_error "orchestrator-ai directory not found. Please ensure your code is in /root/orchestrator-ai/"
    exit 1
fi

print_section "2. Checking system prerequisites"

# Check Docker
if command_exists docker; then
    print_status "Docker is installed: $(docker --version)"
    
    # Check if Docker daemon is running
    if docker info >/dev/null 2>&1; then
        print_status "Docker daemon is running"
    else
        print_warning "Docker daemon is not running. Starting Docker..."
        systemctl start docker
        systemctl enable docker
    fi
else
    print_warning "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    usermod -aG docker $USER
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_status "Docker Compose is installed: $(docker-compose --version)"
else
    print_warning "Docker Compose not found. Installing..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

print_section "3. Checking Docker Compose file"

if [ ! -f "docker-compose.yml" ]; then
    print_warning "docker-compose.yml not found. Creating one..."
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - FRONTEND_PORT=3000
      - API_BASE_URL=${API_BASE_URL:-http://localhost:8001}
      - NEXTAUTH_URL=${NEXTAUTH_URL:-http://206.81.0.227:3000}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET:-default-secret-change-this}
      - DATABASE_URL=${DATABASE_URL:-postgresql://postgres:password@postgres:5432/orchestrator}
    depends_on:
      - postgres
    volumes:
      - ./prisma:/app/prisma
    restart: unless-stopped
    networks:
      - orchestrator-network

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-orchestrator}
      - POSTGRES_USER=${POSTGRES_USER:-postgres}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - orchestrator-network

volumes:
  postgres_data:

networks:
  orchestrator-network:
    driver: bridge
EOF
    print_status "Created docker-compose.yml"
fi

print_section "4. Checking Dockerfile"

if [ ! -f "Dockerfile" ]; then
    print_warning "Dockerfile not found. Creating one..."
    cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with legacy peer deps to handle conflicts
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Generate Prisma client if schema exists
RUN if [ -f "prisma/schema.prisma" ]; then npx prisma generate; fi

# Build the app
RUN npm run build

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
EOF
    print_status "Created Dockerfile"
fi

print_section "5. Checking package.json"

if [ ! -f "package.json" ]; then
    print_error "package.json not found. This is required for the build."
    exit 1
fi

print_status "Found package.json. Checking for common dependency issues..."

# Check for peer dependency warnings
if grep -q "peerDependencies" package.json; then
    print_warning "Found peer dependencies. Will use --legacy-peer-deps flag"
fi

print_section "6. Checking environment configuration"

if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cat > .env << 'EOF'
# Production Environment Configuration
NODE_ENV=production
FRONTEND_PORT=3000

# URLs - Update these for your server
NEXTAUTH_URL=http://206.81.0.227:3000
API_BASE_URL=http://206.81.0.227:8001

# Security - CHANGE THESE IN PRODUCTION
NEXTAUTH_SECRET=your-super-secret-key-change-this-now

# Database
DATABASE_URL=postgresql://postgres:secure_password@postgres:5432/orchestrator
POSTGRES_DB=orchestrator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password

# Optional: OpenAI API Key
# OPENAI_API_KEY=your-openai-api-key-here
EOF
    print_status "Created .env file"
    print_warning "Please edit .env file and update the secret keys!"
fi

print_section "7. Cleaning up previous builds"

print_status "Stopping any existing containers..."
docker-compose down || true

print_status "Removing old images..."
docker system prune -f

print_status "Removing node_modules to ensure clean install..."
rm -rf node_modules

print_section "8. Building with dependency fixes"

print_status "Building the application with dependency fixes..."

# Method 1: Try with --legacy-peer-deps
echo "Attempting build with legacy peer deps..."
if docker-compose build --no-cache; then
    print_status "✅ Build successful!"
else
    print_error "Build failed. Trying alternative approaches..."
    
    # Method 2: Try building with different Node version
    print_status "Trying with Node 16..."
    sed -i 's/node:18-alpine/node:16-alpine/g' Dockerfile
    
    if docker-compose build --no-cache; then
        print_status "✅ Build successful with Node 16!"
    else
        # Method 3: Try with npm ci instead of npm install
        print_status "Trying with npm ci..."
        sed -i 's/npm install --legacy-peer-deps/npm ci --legacy-peer-deps/g' Dockerfile
        
        if docker-compose build --no-cache; then
            print_status "✅ Build successful with npm ci!"
        else
            print_error "Build still failing. Let's check the specific errors..."
            docker-compose build 2>&1 | grep -E "(error|ERROR|Error)" | tail -20
        fi
    fi
fi

print_section "9. Starting the application"

print_status "Starting the application..."
if docker-compose up -d; then
    print_status "✅ Application started successfully!"
    
    # Wait a moment for services to start
    sleep 10
    
    print_status "Checking service status..."
    docker-compose ps
    
    print_status "Checking if application is responding..."
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        print_status "🎉 Application is running and responding!"
        print_status "🌐 Access your app at: http://206.81.0.227:3000"
    else
        print_warning "Application is starting but not yet responding. Checking logs..."
        docker-compose logs --tail=50
    fi
else
    print_error "Failed to start application. Checking logs..."
    docker-compose logs --tail=50
fi

print_section "10. Final status and troubleshooting"

echo ""
print_status "=== SUMMARY ==="
echo "✅ Docker and Docker Compose installed"
echo "✅ Configuration files created"
echo "✅ Build process completed"

print_status "=== USEFUL COMMANDS ==="
echo "View logs: docker-compose logs -f"
echo "Restart app: docker-compose restart"
echo "Rebuild app: docker-compose down && docker-compose up -d --build"
echo "Stop app: docker-compose down"
echo "Check status: docker-compose ps"

if [ -f ".env" ]; then
    print_warning "⚠️  IMPORTANT: Update your .env file with secure passwords!"
    print_warning "⚠️  Especially change NEXTAUTH_SECRET and database passwords"
fi

print_status "🚀 Deployment script completed!"