# Multi-stage Dockerfile for React.js Vite Frontend
# Stage 1: Build static distribution
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY package*.json ./
RUN npm ci

# Copy application source
COPY . .

# Build production assets
RUN npm run build

# Stage 2: Serve using non-root Nginx for Kubernetes security
FROM nginxinc/nginx-unprivileged:alpine-slim

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose standard unprivileged port
EXPOSE 8080

# Healthcheck for container runtime
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]
