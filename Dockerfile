# Multi-stage build for Food Rescue MAS

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend_react/package*.json ./
RUN npm ci --prefer-offline --no-audit
COPY frontend_react/ ./
RUN npm run build

# Stage 2: Backend
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python files
COPY *.py ./

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist /app/static

# Expose ports
EXPOSE 8000

# Set environment
ENV PYTHONUNBUFFERED=1

# Run backend
CMD ["python", "api.py"]
