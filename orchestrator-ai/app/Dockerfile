FROM node:18-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache libc6-compat openssl

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Generate Prisma client
RUN npx prisma generate --schema=./prisma/schema.prisma

# Build the application
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
