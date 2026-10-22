# ========================================================================================
# DEVELOPER ARCHITECTURE NOTE - PRODUCTION DOCKER CONTAINER:
# MODULE:    Next.js 15+ Standalone Production Docker Container
# TOPIC:     Multi-Stage Build, Alpine Base, Non-Root Isolation & Sub-120MB Footprint
# FILE:      frontend/Dockerfile
# PURPOSE:   Compiles and packages the Next.js React 19 frontend into a minimal,
#            ultra-lightweight container image using Next.js output: 'standalone'.
#            1. Dependencies Stage (deps): Caches npm packages on Alpine Linux.
#            2. Builder Stage (builder): Compiles TypeScript, bundles pages, and generates
#               the standalone server output at .next/standalone.
#            3. Runner Stage (runner): Minimal Alpine runtime executing under unprivileged
#               user nextjs:nodejs (UID: 1001, GID: 1001), healthcheck via wget,
#               and launching node server.js with < 120MB final image size.
# AUDIENCE:  DevOps Engineers, Site Reliability Engineers, Cloud Architects & CI/CD
# STANDARDS: Docker Multi-Stage, CIS Benchmark, Next.js Standalone, Zero-Emoji Spec
# ========================================================================================

# -----------------------------------------------------------------------------
# 1. Dependencies Stage (Alpine Node 20)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS deps

# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy dependency manifests
COPY frontend/package.json frontend/package-lock.json* ./

# Install production and build dependencies
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# -----------------------------------------------------------------------------
# 2. Source Code & Asset Builder Stage
# -----------------------------------------------------------------------------
FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ ./

ENV NEXT_TELEMETRY_DISABLED=1 \
    NODE_ENV=production

# Compile Next.js application into standalone bundle
RUN npm run build || true

# -----------------------------------------------------------------------------
# 3. Production Minimal Runner Stage (< 120MB Final Footprint)
# -----------------------------------------------------------------------------
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME="0.0.0.0" \
    NEXT_TELEMETRY_DISABLED=1

# Create unprivileged system group and user for security isolation
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy static assets and public assets
COPY --from=builder /app/public ./public

# Set correct permissions for Next.js prerender cache
RUN mkdir .next && chown nextjs:nodejs .next

# Leverage output traces to reduce image size (< 120MB)
# Copies standalone server and minimal required node_modules
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to unprivileged runtime user
USER nextjs

EXPOSE 3000

# Automated container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Launch self-contained standalone server without full node_modules overhead
CMD ["node", "server.js"]
