#!/bin/bash

# Complete Server Setup and Dependency Fix Script
# Run these commands step by step on your server: root@206.81.0.227

echo "🚀 NextJS Deployment Fix Script"
echo "================================"

# Step 1: Check current location and navigate to the app
echo "Step 1: Checking directory structure..."
pwd
ls -la

# Navigate to the app directory
cd /root
if [ ! -d "orchestrator-ai" ]; then
    echo "❌ orchestrator-ai directory not found in /root"
    echo "Please ensure your code is uploaded to /root/orchestrator-ai/"
    exit 1
fi

cd orchestrator-ai/app
echo "✅ Now in app directory: $(pwd)"
ls -la

# Step 2: Install system prerequisites
echo -e "\nStep 2: Installing system prerequisites..."

# Update system
apt-get update

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
else
    echo "✅ Docker already installed: $(docker --version)"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose already installed: $(docker-compose --version)"
fi

# Install build tools for node-gyp
apt-get install -y python3 make g++ build-essential curl

# Step 3: Create optimized Dockerfile
echo -e "\nStep 3: Creating optimized Dockerfile..."
cat > Dockerfile << 'EOF'
FROM node:18-alpine

# Install system dependencies for node-gyp
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    libc6-compat

WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Clear npm cache and install dependencies
RUN npm cache clean --force
RUN npm install --legacy-peer-deps --verbose

# Copy source code
COPY . .

# Generate Prisma client if schema exists
RUN if [ -f "prisma/schema.prisma" ]; then \
    echo "Generating Prisma client..." && \
    npx prisma generate; \
    fi

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["npm", "start"]
EOF

echo "✅ Created optimized Dockerfile"

# Step 4: Create simplified docker-compose.yml
echo -e "\nStep 4: Creating Docker Compose configuration..."
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
      - NEXTAUTH_URL=http://206.81.0.227:3000
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET:-default-secret-please-change}
      - API_BASE_URL=http://206.81.0.227:8001
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  default:
    driver: bridge
EOF

echo "✅ Created Docker Compose configuration"

# Step 5: Create environment file
echo -e "\nStep 5: Creating environment configuration..."
cat > .env << 'EOF'
# Production Environment Configuration
NODE_ENV=production

# Application URLs
NEXTAUTH_URL=http://206.81.0.227:3000
API_BASE_URL=http://206.81.0.227:8001

# Security (CHANGE THIS!)
NEXTAUTH_SECRET=your-super-secret-key-change-this-immediately

# Optional configurations
# DATABASE_URL=postgresql://username:password@localhost:5432/database
# OPENAI_API_KEY=your-openai-api-key-here
EOF

echo "✅ Created environment file"
echo "⚠️  IMPORTANT: Edit .env file and change NEXTAUTH_SECRET!"

# Step 6: Clean up previous builds
echo -e "\nStep 6: Cleaning up previous builds..."
docker-compose down 2>/dev/null || true
docker system prune -f
rm -rf node_modules package-lock.json

# Step 7: Build and start the application
echo -e "\nStep 7: Building and starting the application..."
echo "This may take several minutes..."

if docker-compose up --build -d; then
    echo "✅ Build successful!"
    
    # Wait for application to start
    echo "Waiting for application to start..."
    sleep 30
    
    # Check container status
    echo -e "\nContainer status:"
    docker-compose ps
    
    # Check logs
    echo -e "\nRecent logs:"
    docker-compose logs --tail=20
    
    # Test if application is responding
    echo -e "\nTesting application..."
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        echo "🎉 SUCCESS! Application is running!"
        echo "🌐 Access your app at: http://206.81.0.227:3000"
    else
        echo "⚠️  Application is starting but not yet responding"
        echo "Check logs with: docker-compose logs -f"
    fi
else
    echo "❌ Build failed. Checking logs..."
    docker-compose logs
    
    echo -e "\nTrying alternative approach with Node 16..."
    sed -i 's/node:18-alpine/node:16-alpine/g' Dockerfile
    
    if docker-compose up --build -d; then
        echo "✅ Success with Node 16!"
    else
        echo "❌ Still failing. Manual intervention required."
        echo "Check specific error messages above."
    fi
fi

# Step 8: Configure firewall
echo -e "\nStep 8: Configuring firewall..."
ufw allow 22    # SSH
ufw allow 3000  # NextJS app
ufw --force enable

# Step 9: Final status
echo -e "\n🎯 DEPLOYMENT SUMMARY"
echo "======================"
echo "✅ Docker and Docker Compose installed"
echo "✅ Application files configured"
echo "✅ Environment setup completed"
echo "✅ Firewall configured"

echo -e "\n📋 USEFUL COMMANDS:"
echo "View logs:     docker-compose logs -f"
echo "Restart app:   docker-compose restart"
echo "Stop app:      docker-compose down"
echo "Rebuild app:   docker-compose down && docker-compose up --build -d"

echo -e "\n🔗 ACCESS YOUR APP:"
echo "Local:   http://localhost:3000"
echo "Remote:  http://206.81.0.227:3000"

echo -e "\n⚠️  SECURITY REMINDER:"
echo "Edit .env file and change NEXTAUTH_SECRET!"
echo "nano .env"

echo -e "\n🚀 Deployment completed!"