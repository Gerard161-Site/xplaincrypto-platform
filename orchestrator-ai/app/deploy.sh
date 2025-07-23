#!/bin/bash

# Orchestrator AI Frontend Deployment Script
# This script deploys the NextJS frontend with Docker Compose

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_PORT=${FRONTEND_PORT:-3000}
API_BASE_URL=${API_BASE_URL:-http://localhost:8001}
DEPLOY_HOST=${DEPLOY_HOST:-206.81.0.22}

echo -e "${BLUE}🚀 Starting Orchestrator AI Frontend Deployment${NC}"
echo "=================================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_warning "docker-compose not found, checking for 'docker compose'..."
        if ! docker compose version >/dev/null 2>&1; then
            print_error "Docker Compose is not available. Please install Docker Compose."
            exit 1
        else
            DOCKER_COMPOSE_CMD="docker compose"
        fi
    else
        DOCKER_COMPOSE_CMD="docker-compose"
    fi
    
    print_status "Prerequisites check passed"
}

# Setup environment
setup_environment() {
    print_info "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "Please edit .env file with your configuration"
        else
            print_error ".env.example not found. Creating basic .env file..."
            cat > .env << EOF
NODE_ENV=production
NEXTAUTH_URL=http://${DEPLOY_HOST}:${FRONTEND_PORT}
NEXTAUTH_SECRET=$(openssl rand -base64 32)
API_BASE_URL=http://backend:8001
DATABASE_URL=postgresql://orchestrator:orchestrator_password@postgres:5432/orchestrator_db
POSTGRES_DB=orchestrator_db
POSTGRES_USER=orchestrator
POSTGRES_PASSWORD=orchestrator_password
REDIS_CACHE_PASSWORD=redis_cache_123
OPENAI_API_KEY=your-openai-api-key-here
EOF
        fi
    fi
    
    # Validate environment
    if ! grep -q "NEXTAUTH_SECRET" .env || grep -q "your-super-secret" .env; then
        print_warning "Generating new NEXTAUTH_SECRET..."
        if command_exists openssl; then
            NEW_SECRET=$(openssl rand -base64 32)
            sed -i "s/NEXTAUTH_SECRET=.*/NEXTAUTH_SECRET=${NEW_SECRET}/" .env
        fi
    fi
    
    print_status "Environment setup completed"
}

# Clean up previous deployment
cleanup_previous() {
    print_info "Cleaning up previous deployment..."
    
    # Stop and remove containers
    $DOCKER_COMPOSE_CMD down --remove-orphans 2>/dev/null || true
    
    # Remove unused images and volumes
    docker system prune -f >/dev/null 2>&1 || true
    
    # Clean build cache
    rm -rf .next 2>/dev/null || true
    rm -rf node_modules/.cache 2>/dev/null || true
    
    print_status "Cleanup completed"
}

# Build and start services
deploy_services() {
    print_info "Building and starting services..."
    
    # Build images
    print_info "Building Docker images..."
    $DOCKER_COMPOSE_CMD build --no-cache frontend
    
    if [ $? -ne 0 ]; then
        print_error "Failed to build frontend image"
        exit 1
    fi
    
    # Start services
    print_info "Starting services..."
    $DOCKER_COMPOSE_CMD up -d
    
    if [ $? -ne 0 ]; then
        print_error "Failed to start services"
        exit 1
    fi
    
    print_status "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_info "Waiting for services to be ready..."
    
    # Wait for database
    print_info "Waiting for database..."
    timeout=60
    while ! docker exec orchestrator-postgres pg_isready -U orchestrator >/dev/null 2>&1; do
        sleep 2
        timeout=$((timeout - 2))
        if [ $timeout -le 0 ]; then
            print_error "Database failed to start within timeout"
            exit 1
        fi
    done
    print_status "Database is ready"
    
    # Wait for frontend
    print_info "Waiting for frontend..."
    timeout=120
    while ! curl -f http://localhost:${FRONTEND_PORT}/api/health >/dev/null 2>&1; do
        sleep 5
        timeout=$((timeout - 5))
        if [ $timeout -le 0 ]; then
            print_warning "Frontend health check timeout, but continuing..."
            break
        fi
    done
    
    if curl -f http://localhost:${FRONTEND_PORT} >/dev/null 2>&1; then
        print_status "Frontend is ready"
    else
        print_warning "Frontend may not be fully ready yet"
    fi
}

# Run database migrations
run_migrations() {
    print_info "Running database migrations..."
    
    # Check if Prisma schema exists
    if [ -f "prisma/schema.prisma" ]; then
        # Generate Prisma client
        docker exec orchestrator-frontend npx prisma generate 2>/dev/null || true
        
        # Run migrations
        docker exec orchestrator-frontend npx prisma db push 2>/dev/null || true
        
        print_status "Database migrations completed"
    else
        print_warning "No Prisma schema found, skipping migrations"
    fi
}

# Check deployment health
check_deployment_health() {
    print_info "Checking deployment health..."
    
    # Check Docker containers
    if ! docker ps | grep -q orchestrator-frontend; then
        print_error "Frontend container is not running"
        return 1
    fi
    
    if ! docker ps | grep -q orchestrator-nginx; then
        print_warning "Nginx container is not running"
    fi
    
    # Check frontend health
    if curl -f http://localhost:${FRONTEND_PORT} >/dev/null 2>&1; then
        print_status "Frontend is accessible at http://localhost:${FRONTEND_PORT}"
    else
        print_warning "Frontend is not accessible"
    fi
    
    # Check nginx
    if curl -f http://localhost:80 >/dev/null 2>&1; then
        print_status "Nginx proxy is accessible at http://localhost:80"
    else
        print_warning "Nginx proxy is not accessible"
    fi
    
    print_status "Health check completed"
}

# Show deployment status
show_deployment_status() {
    echo ""
    echo "=============================================="
    print_status "Deployment completed successfully! 🎉"
    echo "=============================================="
    echo ""
    echo -e "${BLUE}📱 Application URLs:${NC}"
    echo "   • Frontend (Direct): http://${DEPLOY_HOST}:${FRONTEND_PORT}"
    echo "   • Frontend (Nginx):  http://${DEPLOY_HOST}:80"
    echo ""
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "   • View logs:     $DOCKER_COMPOSE_CMD logs -f"
    echo "   • Stop services: $DOCKER_COMPOSE_CMD down"
    echo "   • Restart:       $DOCKER_COMPOSE_CMD restart"
    echo ""
    echo -e "${BLUE}📊 Container Status:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep orchestrator
    echo ""
}

# Error handling
handle_error() {
    print_error "Deployment failed! 💥"
    echo ""
    print_info "Troubleshooting steps:"
    echo "1. Check logs: $DOCKER_COMPOSE_CMD logs"
    echo "2. Check container status: docker ps -a"
    echo "3. Check environment variables in .env file"
    echo "4. Ensure ports ${FRONTEND_PORT} and 80 are available"
    echo ""
    print_info "For more help, check the logs above or contact support."
    exit 1
}

# Set error trap
trap 'handle_error' ERR

# Main deployment flow
main() {
    check_prerequisites
    setup_environment
    cleanup_previous
    deploy_services
    wait_for_services
    run_migrations
    check_deployment_health
    show_deployment_status
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            print_info "Clean deployment requested"
            cleanup_previous
            shift
            ;;
        --no-cache)
            print_info "No cache build requested"
            DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD --no-cache"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --clean      Clean up before deployment"
            echo "  --no-cache   Build without cache"
            echo "  --help       Show this help message"
            echo ""
            exit 0
            ;;
        *)
            print_warning "Unknown option: $1"
            shift
            ;;
    esac
done

# Run main deployment
main

print_status "🎯 All done! Your Orchestrator AI frontend is now running!"