import { NextRequest, NextResponse } from 'next/server';

// Health check endpoint
export async function GET(request: NextRequest) {
  try {
    // Basic health check
    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'orchestrator-ai-frontend',
      version: process.env.npm_package_version || '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      uptime: process.uptime(),
      memory: {
        used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
        rss: Math.round(process.memoryUsage().rss / 1024 / 1024),
      },
      checks: {
        database: await checkDatabase(),
        api: await checkBackendAPI(),
        redis: await checkRedis(),
      }
    };

    // Determine overall health
    const allChecksHealthy = Object.values(healthData.checks).every(check => check.status === 'healthy');
    
    return NextResponse.json({
      ...healthData,
      status: allChecksHealthy ? 'healthy' : 'degraded'
    }, {
      status: allChecksHealthy ? 200 : 503,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });

  } catch (error) {
    console.error('Health check failed:', error);
    
    return NextResponse.json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      service: 'orchestrator-ai-frontend',
      error: error instanceof Error ? error.message : 'Unknown error',
      checks: {
        database: { status: 'unknown', error: 'Health check failed' },
        api: { status: 'unknown', error: 'Health check failed' },
        redis: { status: 'unknown', error: 'Health check failed' }
      }
    }, { 
      status: 503,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });
  }
}

// Check database connectivity
async function checkDatabase() {
  try {
    // Try to import and use Prisma client if available
    if (process.env.DATABASE_URL) {
      try {
        const { PrismaClient } = await import('@prisma/client');
        const prisma = new PrismaClient();
        await prisma.$queryRaw`SELECT 1`;
        await prisma.$disconnect();
        return { status: 'healthy', message: 'Database connection successful' };
      } catch (error) {
        return { 
          status: 'unhealthy', 
          error: error instanceof Error ? error.message : 'Database connection failed' 
        };
      }
    }
    return { status: 'healthy', message: 'No database configured' };
  } catch (error) {
    return { 
      status: 'unhealthy', 
      error: error instanceof Error ? error.message : 'Database check failed' 
    };
  }
}

// Check backend API connectivity
async function checkBackendAPI() {
  try {
    const apiBaseUrl = process.env.API_BASE_URL || 'http://backend:8001';
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${apiBaseUrl}/health`, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      return { status: 'healthy', message: 'Backend API accessible' };
    } else {
      return { 
        status: 'unhealthy', 
        error: `Backend API returned ${response.status}` 
      };
    }
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      return { status: 'unhealthy', error: 'Backend API timeout' };
    }
    return { 
      status: 'unhealthy', 
      error: error instanceof Error ? error.message : 'Backend API check failed' 
    };
  }
}

// Check Redis connectivity
async function checkRedis() {
  try {
    // Basic Redis check - in a real app you'd use a Redis client
    // For now, we'll just check if Redis URL is configured
    if (process.env.REDIS_URL) {
      return { status: 'healthy', message: 'Redis URL configured' };
    }
    return { status: 'healthy', message: 'No Redis configured' };
  } catch (error) {
    return { 
      status: 'unhealthy', 
      error: error instanceof Error ? error.message : 'Redis check failed' 
    };
  }
}

// Support HEAD requests for load balancer health checks
export async function HEAD(request: NextRequest) {
  try {
    return new NextResponse(null, { status: 200 });
  } catch (error) {
    return new NextResponse(null, { status: 503 });
  }
}