# Orchestrator AI - Deployment Guide

This guide will help you deploy the Orchestrator AI NextJS frontend with proper backend connectivity and nginx configuration.

## 🚀 Quick Deployment

### Option 1: Automated Server Deployment (Recommended)

1. **Upload the code to your server:**
   ```bash
   # On your local machine
   scp -r orchestrator-ai root@206.81.0.22:/root/
   
   # Or use rsync
   rsync -avz --exclude 'node_modules' --exclude '.next' orchestrator-ai/ root@206.81.0.22:/root/orchestrator-ai/
   ```

2. **SSH into your server:**
   ```bash
   ssh -i ~/.ssh/id_rsa root@206.81.0.22
   ```

3. **Run the automated deployment script:**
   ```bash
   cd /root/orchestrator-ai
   chmod +x server-deploy.sh
   ./server-deploy.sh
   ```

### Option 2: Manual Deployment

1. **SSH into your server and navigate to the app directory:**
   ```bash
   ssh -i ~/.ssh/id_rsa root@206.81.0.22
   cd /root/orchestrator-ai/app
   ```

2. **Run the local deployment script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 📋 Prerequisites

- Ubuntu/Debian server (tested on Ubuntu 20.04+)
- Root access or sudo privileges
- At least 2GB RAM and 10GB disk space
- Ports 22, 80, 443, 3000, 8001 available

## 🔧 Configuration

### Environment Variables

Edit the `.env` file in the `orchestrator-ai/app/` directory:

```bash
# Required - Add your OpenAI API key
OPENAI_API_KEY=your-openai-api-key-here

# Optional - Customize other settings
NEXTAUTH_URL=http://206.81.0.22:3000
API_BASE_URL=http://backend:8001
POSTGRES_PASSWORD=your-secure-password
```

### Key Configuration Files

- **`docker-compose.yml`** - Multi-service orchestration
- **`nginx.conf`** - Reverse proxy and load balancing
- **`Dockerfile`** - Optimized NextJS container
- **`package.json`** - Dependencies with conflict resolution
- **`next.config.js`** - NextJS optimization settings

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│                Nginx                    │
│            (Port 80/443)               │
└─────────────┬───────────────────────────┘
              │
    ┌─────────▼─────────┐    ┌─────────────┐
    │   NextJS App      │    │   Backend   │
    │   (Port 3000)     │◄──►│ (Port 8001) │
    └─────────┬─────────┘    └─────────────┘
              │
    ┌─────────▼─────────┐    ┌─────────────┐
    │   PostgreSQL      │    │   Redis     │
    │   (Port 5432)     │    │ (Port 6380) │
    └───────────────────┘    └─────────────┘
```

## 🔍 Troubleshooting

### Common Issues

#### 1. **Dependency Conflicts**
```bash
# Solution: Clean installation
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

#### 2. **Port Already in Use**
```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :80

# Kill the process or change port in docker-compose.yml
sudo kill -9 <PID>
```

#### 3. **Docker Build Fails**
```bash
# Clear Docker cache and rebuild
docker system prune -f
docker-compose build --no-cache

# Check Docker logs
docker-compose logs frontend
```

#### 4. **Backend Connection Issues**
```bash
# Check if backend is running
docker ps | grep backend

# Test backend connectivity
curl http://localhost:8001/health

# Check network connectivity
docker network ls
docker network inspect orchestrator-ai_orchestrator-network
```

#### 5. **Database Connection Problems**
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Test database connection
docker exec orchestrator-postgres pg_isready -U orchestrator

# Reset database
docker-compose down
docker volume rm orchestrator-ai_postgres_data
docker-compose up -d
```

### Health Check Endpoints

- **Frontend Health:** `http://206.81.0.22:3000/api/health`
- **Backend Health:** `http://206.81.0.22:8001/health`
- **Main App:** `http://206.81.0.22:80`

### Log Analysis

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs frontend
docker-compose logs backend
docker-compose logs postgres
docker-compose logs nginx

# Check container status
docker ps -a

# Check resource usage
docker stats
```

### Performance Optimization

#### 1. **Memory Issues**
```bash
# Check memory usage
free -h
docker stats

# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
```

#### 2. **Build Performance**
```bash
# Enable Docker BuildKit
export DOCKER_BUILDKIT=1

# Use multi-core builds
docker-compose build --parallel
```

#### 3. **Application Performance**
- Enable Redis caching: `docker-compose --profile cache up -d`
- Use nginx compression (already configured)
- Monitor with health checks

## 🔐 Security

### Firewall Configuration
```bash
# Check firewall status
sudo ufw status

# Allow required ports
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSL Configuration (Optional)
```bash
# Install certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Update nginx.conf to enable HTTPS section
```

### Security Best Practices
- Change default passwords in `.env`
- Use strong `NEXTAUTH_SECRET`
- Regularly update dependencies
- Monitor logs for suspicious activity

## 📊 Monitoring

### Container Monitoring
```bash
# Check container health
docker ps
docker-compose ps

# View resource usage
docker stats

# Check container logs
docker-compose logs -f --tail=100
```

### Application Monitoring
```bash
# Check application health
curl http://206.81.0.22:3000/api/health

# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s http://206.81.0.22:3000/
```

### Database Monitoring
```bash
# Check database connections
docker exec orchestrator-postgres psql -U orchestrator -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
docker exec orchestrator-postgres psql -U orchestrator -c "SELECT pg_size_pretty(pg_database_size('orchestrator_db'));"
```

## 🔄 Maintenance

### Updates
```bash
# Update application
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# Update system packages
sudo apt update && sudo apt upgrade
```

### Backups
```bash
# Backup database
docker exec orchestrator-postgres pg_dump -U orchestrator orchestrator_db > backup.sql

# Backup volumes
docker run --rm -v orchestrator-ai_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres-backup.tar.gz /data
```

### Cleanup
```bash
# Remove unused Docker resources
docker system prune -f

# Clean up logs
sudo journalctl --vacuum-time=7d
```

## 📞 Support

If you encounter issues:

1. **Check the logs first:** `docker-compose logs -f`
2. **Verify prerequisites:** Ensure Docker and Docker Compose are installed
3. **Check ports:** Make sure required ports are available
4. **Review configuration:** Verify `.env` file settings
5. **Test connectivity:** Use health check endpoints

### Quick Debugging Commands
```bash
# Service status
systemctl status orchestrator-ai

# Container status
docker ps -a

# Network connectivity
docker network ls
docker network inspect orchestrator-ai_orchestrator-network

# Resource usage
df -h
free -h
docker stats --no-stream
```

## 🎯 Success Indicators

After successful deployment, you should see:

- ✅ All containers running: `docker ps`
- ✅ Health check passes: `curl http://206.81.0.22:3000/api/health`
- ✅ Application accessible: `http://206.81.0.22:80`
- ✅ No errors in logs: `docker-compose logs`

---

**🚀 Your Orchestrator AI application should now be running successfully!**

Access it at: `http://206.81.0.22:80` or `http://206.81.0.22:3000`