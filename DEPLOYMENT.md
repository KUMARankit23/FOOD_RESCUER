# Production Deployment Guide

## Local Docker Deployment

```bash
docker-compose up -d
# App runs at http://localhost:8000
```

## Render.com Deployment

1. Fork repo to GitHub
2. Set environment variables in Render dashboard:
   - DATABASE_URL
   - GOOGLE_API_KEY
   - LLM_PROVIDER
3. Create new Web Service
4. Build command: (auto-detected)
5. Start command: `python api.py`
6. Deploy

## Environment Variables

```bash
export LLM_PROVIDER=google_gemini
export GOOGLE_API_KEY=your_key
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
```

## Database Migration

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

## Health Check

```bash
curl http://localhost:8000/health
```

## Production Checklist

- [ ] Set all environment variables
- [ ] Configure PostgreSQL
- [ ] Configure Redis
- [ ] Set ALLOWED_ORIGINS
- [ ] Enable SSL/TLS
- [ ] Set DEBUG=false
- [ ] Configure backup strategy
- [ ] Set up monitoring
- [ ] Configure error logging
- [ ] Test disaster recovery
