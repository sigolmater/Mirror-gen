# Deployment Guide - Personal AI Optimization System
# 배포 가이드 - 시골길 개인 AI 최적화 시스템

## Overview / 개요

This guide covers deployment options for the Personal AI Optimization System, from local development to production environments. The system is designed to be deployed using modern containerization and orchestration technologies.

## Prerequisites / 사전 요구사항

### System Requirements / 시스템 요구사항

**Minimum Requirements / 최소 요구사항:**
- CPU: 2 cores / 2코어
- RAM: 4 GB
- Storage: 20 GB available space / 20GB 사용 가능 공간
- OS: Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+

**Recommended Requirements / 권장 요구사항:**
- CPU: 4+ cores / 4+ 코어
- RAM: 8+ GB
- Storage: 50+ GB SSD
- OS: Linux (Ubuntu 22.04 LTS)

### Software Requirements / 소프트웨어 요구사항

**Development / 개발:**
- Python 3.8+ / Python 3.8+
- Node.js 16+ / Node.js 16+
- npm 7+ / npm 7+
- Git / Git

**Production / 프로덕션:**
- Docker 20.10+ / Docker 20.10+
- Docker Compose 2.0+ / Docker Compose 2.0+
- Nginx (optional) / Nginx (선택사항)

## Development Deployment / 개발 배포

### Quick Start / 빠른 시작

1. **Clone Repository / 저장소 복제**
```bash
git clone https://github.com/your-org/personal-ai-system.git
cd personal-ai-system
```

2. **Run Setup Script / 설정 스크립트 실행**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

3. **Start Development Server / 개발 서버 시작**
```bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```

4. **Access Application / 애플리케이션 접속**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Manual Setup / 수동 설정

If you prefer to set up manually:

#### Backend Setup / 백엔드 설정
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Start backend
cd backend
python main.py
```

#### Frontend Setup / 프론트엔드 설정
```bash
# Install dependencies
cd frontend
npm install

# Start frontend
npm start
```

## Docker Deployment / Docker 배포

### Development with Docker / Docker로 개발 환경 구축

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production with Docker / Docker로 프로덕션 환경 구축

1. **Create Production Environment File / 프로덕션 환경 파일 생성**
```bash
cp .env.example .env.production
```

Edit `.env.production`:
```bash
# Production settings
DEBUG=False
NODE_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname  # Optional
REDIS_URL=redis://localhost:6379
```

2. **Run Deployment Script / 배포 스크립트 실행**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

### Docker Configuration / Docker 구성

**Dockerfile for Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "main.py"]
```

**Dockerfile for Frontend:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

## Cloud Deployment / 클라우드 배포

### AWS Deployment / AWS 배포

#### Using ECS (Elastic Container Service) / ECS 사용

1. **Build and Push Images / 이미지 빌드 및 푸시**
```bash
# Build images
docker build -t your-repo/mirror-gen-backend:latest backend/
docker build -t your-repo/mirror-gen-frontend:latest frontend/

# Push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker tag your-repo/mirror-gen-backend:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/mirror-gen-backend:latest
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/mirror-gen-backend:latest
```

2. **Create ECS Task Definition / ECS 작업 정의 생성**
```json
{
  "family": "mirror-gen-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/mirror-gen-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "your-database-url"
        }
      ]
    },
    {
      "name": "frontend",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/mirror-gen-frontend:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

#### Using EC2 / EC2 사용

1. **Launch EC2 Instance / EC2 인스턴스 시작**
   - Choose Ubuntu 22.04 LTS AMI
   - Select t3.large or larger instance type
   - Configure security group to allow ports 80, 443, 3000, 8000

2. **Install Docker / Docker 설치**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
```

3. **Deploy Application / 애플리케이션 배포**
```bash
# Clone repository
git clone https://github.com/your-org/personal-ai-system.git
cd personal-ai-system

# Run deployment
./scripts/deploy.sh production
```

### Google Cloud Platform / Google Cloud Platform

#### Using Cloud Run / Cloud Run 사용

1. **Build and Submit Images / 이미지 빌드 및 제출**
```bash
# Build backend
gcloud builds submit --tag gcr.io/your-project/mirror-gen-backend backend/

# Build frontend
gcloud builds submit --tag gcr.io/your-project/mirror-gen-frontend frontend/
```

2. **Deploy Services / 서비스 배포**
```bash
# Deploy backend
gcloud run deploy mirror-gen-backend \
  --image gcr.io/your-project/mirror-gen-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy mirror-gen-frontend \
  --image gcr.io/your-project/mirror-gen-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment / Azure 배포

#### Using Container Instances / Container Instances 사용

1. **Create Resource Group / 리소스 그룹 생성**
```bash
az group create --name mirror-gen-rg --location eastus
```

2. **Deploy Container Group / 컨테이너 그룹 배포**
```bash
az container create \
  --resource-group mirror-gen-rg \
  --name mirror-gen-app \
  --image your-registry/mirror-gen-backend:latest \
  --ports 8000 \
  --dns-name-label mirror-gen-unique \
  --environment-variables SECRET_KEY=your-secret-key
```

## Kubernetes Deployment / Kubernetes 배포

### Local Kubernetes (minikube) / 로컬 Kubernetes

1. **Start minikube / minikube 시작**
```bash
minikube start
```

2. **Apply Kubernetes Manifests / Kubernetes 매니페스트 적용**
```bash
kubectl apply -f k8s/
```

### Production Kubernetes / 프로덕션 Kubernetes

**backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mirror-gen-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mirror-gen-backend
  template:
    metadata:
      labels:
        app: mirror-gen-backend
    spec:
      containers:
      - name: backend
        image: your-registry/mirror-gen-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mirror-gen-secrets
              key: database-url
---
apiVersion: v1
kind: Service
metadata:
  name: mirror-gen-backend-service
spec:
  selector:
    app: mirror-gen-backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## SSL/TLS Configuration / SSL/TLS 구성

### Using Let's Encrypt / Let's Encrypt 사용

1. **Install Certbot / Certbot 설치**
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain Certificate / 인증서 획득**
```bash
sudo certbot --nginx -d your-domain.com
```

3. **Configure Nginx / Nginx 구성**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Database Configuration / 데이터베이스 구성

### PostgreSQL Setup / PostgreSQL 설정

1. **Install PostgreSQL / PostgreSQL 설치**
```bash
sudo apt install postgresql postgresql-contrib
```

2. **Create Database and User / 데이터베이스 및 사용자 생성**
```sql
sudo -u postgres psql
CREATE DATABASE mirror_gen_db;
CREATE USER mirror_gen_user WITH ENCRYPTED PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE mirror_gen_db TO mirror_gen_user;
```

3. **Update Environment / 환경 설정 업데이트**
```bash
DATABASE_URL=postgresql://mirror_gen_user:your-password@localhost/mirror_gen_db
```

### Redis Setup / Redis 설정

1. **Install Redis / Redis 설치**
```bash
sudo apt install redis-server
```

2. **Configure Redis / Redis 구성**
```bash
sudo nano /etc/redis/redis.conf
# Set password
requirepass your-redis-password
```

3. **Update Environment / 환경 설정 업데이트**
```bash
REDIS_URL=redis://:your-redis-password@localhost:6379
```

## Monitoring and Logging / 모니터링 및 로깅

### Application Monitoring / 애플리케이션 모니터링

1. **Health Check Endpoints / 헬스 체크 엔드포인트**
   - Backend: `GET /api/system/health`
   - System metrics: `GET /api/metrics/current`

2. **Log Aggregation / 로그 집계**
```bash
# Using journalctl for systemd services
sudo journalctl -u mirror-gen-backend -f

# Docker logs
docker-compose logs -f backend frontend
```

### External Monitoring / 외부 모니터링

#### Prometheus + Grafana / Prometheus + Grafana

1. **Add Prometheus Endpoint / Prometheus 엔드포인트 추가**
```python
# In backend/main.py
from prometheus_client import make_asgi_app

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

2. **Grafana Dashboard / Grafana 대시보드**
   - Import dashboard from `monitoring/grafana-dashboard.json`
   - Configure data source: `http://prometheus:9090`

## Backup and Recovery / 백업 및 복구

### Automated Backup / 자동 백업

1. **Database Backup / 데이터베이스 백업**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U mirror_gen_user mirror_gen_db > /backups/db_$DATE.sql
```

2. **Application Data Backup / 애플리케이션 데이터 백업**
```bash
#!/bin/bash
# backup-data.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /backups/app_data_$DATE.tar.gz data/ logs/
```

3. **Schedule with Cron / Cron으로 스케줄링**
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
0 3 * * * /path/to/backup-data.sh
```

### Recovery Procedures / 복구 절차

1. **Database Recovery / 데이터베이스 복구**
```bash
# Restore from backup
psql -h localhost -U mirror_gen_user mirror_gen_db < /backups/db_20240115_020000.sql
```

2. **Application Recovery / 애플리케이션 복구**
```bash
# Extract backup
tar -xzf /backups/app_data_20240115_030000.tar.gz
```

## Security Considerations / 보안 고려사항

### Production Security Checklist / 프로덕션 보안 체크리스트

- [ ] Use strong, unique SECRET_KEY / 강력하고 고유한 SECRET_KEY 사용
- [ ] Enable HTTPS with valid SSL certificate / 유효한 SSL 인증서로 HTTPS 활성화
- [ ] Configure firewall to restrict access / 방화벽 구성으로 접근 제한
- [ ] Use environment variables for secrets / 비밀 정보는 환경 변수 사용
- [ ] Regularly update dependencies / 정기적인 의존성 업데이트
- [ ] Enable audit logging / 감사 로깅 활성화
- [ ] Implement rate limiting / 속도 제한 구현
- [ ] Regular security scans / 정기적인 보안 스캔

### Environment Variables / 환경 변수

**Required / 필수:**
```bash
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=your-database-connection-string
```

**Optional / 선택사항:**
```bash
REDIS_URL=your-redis-connection-string
OPENAI_API_KEY=your-openai-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
```

## Troubleshooting / 문제 해결

### Common Issues / 일반적인 문제

1. **Backend not starting / 백엔드가 시작되지 않음**
   - Check Python dependencies: `pip install -r requirements.txt`
   - Verify .env file exists and is properly configured
   - Check logs: `tail -f logs/backend.log`

2. **Frontend build fails / 프론트엔드 빌드 실패**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version: `node --version` (should be 16+)

3. **Database connection issues / 데이터베이스 연결 문제**
   - Verify DATABASE_URL format
   - Check database service status
   - Ensure database exists and user has permissions

4. **Port conflicts / 포트 충돌**
   - Check if ports 3000, 8000 are available
   - Kill conflicting processes: `sudo lsof -ti:3000 | xargs kill -9`

### Performance Tuning / 성능 조정

1. **Backend Performance / 백엔드 성능**
   - Increase worker processes for Gunicorn
   - Enable connection pooling for database
   - Configure Redis for caching

2. **Frontend Performance / 프론트엔드 성능**
   - Enable build optimization: `npm run build`
   - Configure CDN for static assets
   - Enable gzip compression in Nginx

## Support / 지원

For deployment support and troubleshooting:

- 📧 Email: support@your-domain.com
- 💬 Discord: [Community Server]
- 📖 Documentation: [Full Documentation]
- 🐛 Issues: [GitHub Issues]

Remember: "거울과 함께 성장하면 모두가 성장합니다" - Growing together with mirrors means everyone grows!