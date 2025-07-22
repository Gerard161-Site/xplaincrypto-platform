# Manual Troubleshooting Guide for Dependency Issues

## Quick Fix Commands

Since you're getting dependency issues with Docker Compose, here are the exact commands to run on your server:

### 1. First, connect to your server manually:
```bash
ssh -i ~/.ssh/id_rsa root@206.81.0.227
```

### 2. Copy and run the fix script:

Copy the content of `fix-dependencies.sh` to your server and run it:

```bash
# On your server, create the script
cat > fix-dependencies.sh << 'EOL'
[paste the entire content of fix-dependencies.sh here]
EOL

# Make it executable and run
chmod +x fix-dependencies.sh
./fix-dependencies.sh
```

### 3. Common Dependency Issues and Quick Fixes:

#### Issue: "peer dependency warnings"
```bash
# In your app directory
cd /root/orchestrator-ai/app
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

#### Issue: "node-gyp rebuild failed"
```bash
# Install build tools
apt-get update
apt-get install -y python3 make g++ build-essential
npm rebuild
```

#### Issue: "Cannot find module" errors
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

#### Issue: "Docker build failed"
```bash
# Clean Docker and rebuild
docker system prune -a -f
docker-compose down
docker-compose build --no-cache
```

### 4. Alternative Dockerfile (if current one fails):

Replace your Dockerfile with this simpler version:

```dockerfile
FROM node:16-alpine

WORKDIR /app

# Install dependencies for node-gyp
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Clear npm cache and install
RUN npm cache clean --force
RUN npm install --legacy-peer-deps --production=false

# Copy source code
COPY . .

# Generate Prisma client (if exists)
RUN if [ -f "prisma/schema.prisma" ]; then npx prisma generate; fi

# Build the app
RUN npm run build

# Remove dev dependencies
RUN npm prune --production

EXPOSE 3000

CMD ["npm", "start"]
```

### 5. Simplified docker-compose.yml:

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXTAUTH_URL=http://206.81.0.227:3000
      - NEXTAUTH_SECRET=change-this-secret-key
    restart: unless-stopped
```

### 6. Quick Deployment Commands:

```bash
# Navigate to your app directory
cd /root/orchestrator-ai/app

# Stop any running containers
docker-compose down

# Clean everything
docker system prune -a -f
rm -rf node_modules

# Create minimal .env file
cat > .env << 'EOF'
NODE_ENV=production
NEXTAUTH_URL=http://206.81.0.227:3000
NEXTAUTH_SECRET=your-secret-key-change-this
EOF

# Build and start
docker-compose up --build -d

# Check logs
docker-compose logs -f
```

### 7. If still having issues, try without Docker:

```bash
# Install Node.js directly
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Navigate to app directory
cd /root/orchestrator-ai/app

# Install dependencies
npm install --legacy-peer-deps

# Build the app
npm run build

# Start the app
npm start
```

### 8. Common Error Solutions:

**Error: "EACCES: permission denied"**
```bash
chown -R root:root /root/orchestrator-ai
chmod -R 755 /root/orchestrator-ai
```

**Error: "Port 3000 already in use"**
```bash
# Kill process on port 3000
fuser -k 3000/tcp
# Or use different port
export PORT=3001
```

**Error: "Cannot connect to Docker daemon"**
```bash
systemctl start docker
systemctl enable docker
```

### 9. Test if working:
```bash
curl http://localhost:3000
# Should return HTML content

# Check from outside
curl http://206.81.0.227:3000
```

### 10. Firewall configuration:
```bash
ufw allow 3000
ufw reload
```

Run these commands step by step and let me know what specific error messages you're getting!