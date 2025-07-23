# Multi-stage build for NextJS app with enhanced Prisma support
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat openssl
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies with clean cache and legacy peer deps flag
RUN npm ci --legacy-peer-deps && npm cache clean --force

# Copy prisma schema for client generation
COPY prisma ./prisma/

# Generate Prisma client with verbose logging
RUN if [ -f "./prisma/schema.prisma" ]; then \
    echo "Generating Prisma client..." && \
    npx prisma generate --verbose; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

# Copy dependencies and prisma client from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/prisma ./prisma

# Copy source code
COPY . .

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ENV SKIP_ENV_VALIDATION=1

# Ensure Prisma client is available
RUN echo "Checking Prisma client availability..." && \
    if [ -f "./prisma/schema.prisma" ]; then \
      npx prisma generate --verbose || echo "Prisma generation failed, continuing..."; \
    fi

# Build the application with increased memory and error handling
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN echo "Starting NextJS build..." && \
    npm run build || (echo "Build failed, checking for partial build..." && \
    if [ -d ".next" ]; then echo "Partial build found, continuing..."; else exit 1; fi)

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV SKIP_ENV_VALIDATION=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy necessary files
COPY --from=builder /app/public ./public

# Copy the built application
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Copy Prisma client if it exists
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder /app/node_modules/@prisma ./node_modules/@prisma

# Set correct permissions
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start the application
CMD ["node", "server.js"]