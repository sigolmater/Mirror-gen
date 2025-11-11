# Deployment Guide

## Quick Start (Development)

### 1. Start Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on: http://localhost:8000

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:5173

## Production Deployment

### Backend (FastAPI)

#### Option 1: Using Uvicorn with Gunicorn

1. Install production dependencies:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Option 2: Docker Deployment

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t mirror-gen-backend .
docker run -p 8000:8000 mirror-gen-backend
```

### Frontend (React)

#### Build for Production

```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`

#### Option 1: Serve with Nginx

1. Install Nginx
2. Copy built files to web root:
```bash
cp -r dist/* /var/www/html/
```

3. Configure Nginx (`/etc/nginx/sites-available/mirror-gen`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Option 2: Docker Deployment

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Database Migration (SQLite to PostgreSQL)

For production, consider using PostgreSQL:

1. Install PostgreSQL driver:
```bash
pip install asyncpg
```

2. Update `backend/database.py`:
```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/mirror_gen"
```

3. The schema will be automatically created on first run.

### Environment Variables

Create `.env` file in backend directory:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/mirror_gen
CORS_ORIGINS=http://yourdomain.com,https://yourdomain.com
SECRET_KEY=your-secret-key-here
```

Load in `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Docker Compose (Full Stack)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db/mirror_gen
    depends_on:
      - db
    
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mirror_gen
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

## Monitoring and Maintenance

### Health Checks

- Backend: http://localhost:8000/health
- Frontend: Check if page loads

### Logs

#### Backend Logs
```bash
tail -f logs/backend.log
```

#### Nginx Logs
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Database Backup

#### SQLite
```bash
cp mirror_gen.db mirror_gen_backup_$(date +%Y%m%d).db
```

#### PostgreSQL
```bash
pg_dump -U postgres mirror_gen > backup_$(date +%Y%m%d).sql
```

## Security Considerations

1. **Enable HTTPS** using Let's Encrypt or SSL certificates
2. **Add Authentication** to API endpoints
3. **Rate Limiting** to prevent abuse
4. **Input Validation** is already implemented with Pydantic
5. **CORS Configuration** - restrict to your domain only
6. **Environment Variables** - never commit secrets to git

## Performance Optimization

1. **Enable Caching** for static assets
2. **Database Indexing** - already implemented in models
3. **API Response Compression** - enable gzip in Nginx
4. **CDN** for static frontend assets
5. **Database Connection Pooling** - already configured in SQLAlchemy

## Scaling

For high traffic:

1. **Horizontal Scaling**: Deploy multiple backend instances behind a load balancer
2. **Database Scaling**: Use PostgreSQL with read replicas
3. **Caching Layer**: Add Redis for session/data caching
4. **Message Queue**: Add Celery for async tasks

## Troubleshooting

### Backend won't start
- Check Python version (3.8+)
- Verify all dependencies installed
- Check database connectivity

### Frontend won't connect to backend
- Verify CORS settings in backend
- Check API proxy configuration in vite.config.js
- Ensure backend is running

### Database errors
- Check database file permissions
- Verify DATABASE_URL is correct
- Ensure migrations have run

## Support

For issues, check:
1. Application logs
2. Browser console (for frontend issues)
3. API documentation at http://localhost:8000/docs
