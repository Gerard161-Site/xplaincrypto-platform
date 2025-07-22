# NextJS Orchestrator AI - Deployment Guide

## Quick Deployment to Server (206.81.0.227)

### Prerequisites
- SSH key access to your server (`~/.ssh/id_rsa`)
- Server with Ubuntu/Debian OS
- Root access to the server

### 1. Automated Deployment (Recommended)

Run the automated deployment script:

```bash
./deploy-to-server.sh
```

This script will:
- Test SSH connection
- Install Docker and Docker Compose on the server
- Copy your application files
- Set up environment configuration
- Build and start the application

### 2. Manual Deployment (Alternative)

If you prefer manual deployment:

#### Step 1: Connect to your server
```bash
ssh -i ~/.ssh/id_rsa root@206.81.0.227
```

#### Step 2: Install prerequisites
```bash
# Update system
apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

#### Step 3: Copy your application
```bash
# From your local machine
scp -i ~/.ssh/id_rsa -r orchestrator-ai/ root@206.81.0.227:/root/
```

#### Step 4: Configure environment
```bash
# On the server
cd /root/orchestrator-ai/app
cp .env.production .env

# Edit the .env file with your actual values
nano .env
```

#### Step 5: Start the application
```bash
docker-compose up -d --build
```

### 3. Environment Configuration

Update these important variables in your `.env` file:

```env
# Change these for security
NEXTAUTH_SECRET=your-super-secret-key-here
POSTGRES_PASSWORD=your-secure-database-password
REDIS_PASSWORD=your-secure-redis-password

# Add your OpenAI API key if using AI features
OPENAI_API_KEY=your-openai-api-key

# Server URLs (already configured for your server)
NEXTAUTH_URL=http://206.81.0.227:3000
API_BASE_URL=http://206.81.0.227:8001
```

### 4. Firewall Configuration

Make sure your server firewall allows the necessary ports:

```bash
# On your server
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 3000  # NextJS app
ufw allow 8001  # API (if needed)
ufw enable
```

### 5. Verify Deployment

Check if your application is running:

```bash
# Check Docker containers
docker-compose ps

# Check application health
curl http://localhost:3000

# View logs
docker-compose logs -f
```

### 6. Access Your Application

Once deployed, you can access your application at:
- **Frontend**: http://206.81.0.227:3000
- **API** (if running): http://206.81.0.227:8001

### 7. Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart application
docker-compose restart

# Stop application
docker-compose down

# Update application (after code changes)
docker-compose down
docker-compose up -d --build

# Access database
docker-compose exec postgres psql -U postgres -d orchestrator
```

### 8. Troubleshooting

#### Application won't start:
```bash
# Check logs
docker-compose logs

# Check if ports are available
netstat -tlnp | grep :3000

# Restart Docker daemon
systemctl restart docker
```

#### Database connection issues:
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Reset database
docker-compose down
docker volume rm app_postgres_data
docker-compose up -d
```

#### Permission issues:
```bash
# Fix file permissions
chown -R root:root /root/orchestrator-ai
chmod -R 755 /root/orchestrator-ai
```

### 9. SSL/HTTPS Setup (Optional)

To enable HTTPS with Let's Encrypt:

```bash
# Install certbot
apt-get install certbot

# Get SSL certificate
certbot certonly --standalone -d yourdomain.com

# Update nginx configuration to use SSL
# Enable nginx profile in docker-compose.yml
docker-compose --profile nginx up -d
```

### 10. Monitoring and Maintenance

```bash
# Set up log rotation
echo '/var/lib/docker/containers/*/*-json.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}' > /etc/logrotate.d/docker

# Set up automatic updates (optional)
echo '0 2 * * 0 cd /root/orchestrator-ai/app && docker-compose pull && docker-compose up -d' | crontab -
```

## Support

If you encounter any issues:
1. Check the application logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Check system resources: `htop` or `docker stats`
4. Review the environment configuration in `.env`

Happy deploying! 🚀