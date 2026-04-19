# Docker & Deployment

Guide for containerizing and deploying the Language Learning Framework.

For split-machine inference where TTS runs on a separate device, see [Remote TTS Server](remote-tts-server.md).

## Docker Compose (Quick Start)

### Prerequisites

- Docker
- Docker Compose 1.27+

### Run Everything

```bash
docker-compose up --build
```

This starts:
- **API** - http://localhost:5000
- **UI** - http://localhost:3000
- **Data directories** - Initialized automatically

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f ui
```

### Environment Variables

Set in `.env` or override on command line:

```bash
docker-compose -e LOG_LEVEL=DEBUG up
```

Or in `.env`:
```env
API_PORT=5000
API_DEBUG=False
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

If using a remote TTS server, also set:

```env
TTS_REMOTE_PROVIDER_ID=remote-tts
TTS_REMOTE_BASE_URL=http://INFERENCE_HOST:7001
TTS_REMOTE_SYNTHESIZE_PATH=/synthesize
TTS_REMOTE_HEALTH_PATH=/health
```

See [Remote TTS Server](remote-tts-server.md) for full setup and validation.

## Individual Containers

### API Container

Build:
```bash
docker build -t llf-api ./apps/api
```

Run:
```bash
docker run -p 5000:5000 \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=5000 \
  -v $(pwd)/data:/usr/src/app/data \
  llf-api
```

### UI Container

Build:
```bash
docker build -t llf-ui ./apps/web-ui
```

Run:
```bash
docker run -p 3000:80 \
  -e VITE_API_URL=http://api:5000/api \
  llf-ui
```

## Production Deployment

### Vercel (Frontend)

```bash
cd apps/web-ui
npm run build
# Deploy dist/ directory
```

### Heroku (Backend)

```bash
# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

Set environment variables:
```bash
heroku config:set API_PORT=5000
heroku config:set LOG_LEVEL=INFO
```

### Self-Hosted (AWS/Digital Ocean/etc.)

1. **SSH into server**

```bash
ssh user@your-server.com
```

2. **Install Docker & Docker Compose**

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone repository**

```bash
git clone https://github.com/your-username/LanguageLearningFramework.git
cd LanguageLearningFramework
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env with production settings
nano .env
```

5. **Start services**

```bash
docker-compose up -d
```

6. **Configure reverse proxy (Nginx)**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    # UI
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # API
    location /api {
        proxy_pass http://localhost:5000/api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Enable HTTPS (Let's Encrypt)**

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Kubernetes Deployment

### Create Namespace

```bash
kubectl create namespace llf
```

### Deploy API

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llf-api
  namespace: llf
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llf-api
  template:
    metadata:
      labels:
        app: llf-api
    spec:
      containers:
      - name: api
        image: your-registry/llf-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: API_PORT
          value: "5000"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
```

### Deploy UI

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llf-ui
  namespace: llf
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llf-ui
  template:
    metadata:
      labels:
        app: llf-ui
    spec:
      containers:
      - name: ui
        image: your-registry/llf-ui:latest
        ports:
        - containerPort: 80
        env:
        - name: VITE_API_URL
          value: "https://your-domain.com/api"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### Create Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: llf-api
  namespace: llf
spec:
  selector:
    app: llf-api
  ports:
  - port: 5000
    targetPort: 5000
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: llf-ui
  namespace: llf
spec:
  selector:
    app: llf-ui
  ports:
  - port: 3000
    targetPort: 80
  type: ClusterIP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: llf-ingress
  namespace: llf
spec:
  ingressClassName: nginx
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: llf-ui
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: llf-api
            port:
              number: 5000
```

## Monitoring

### Health Checks

API health endpoint:
```bash
curl http://localhost:5000/health
```

### Logs

View container logs:
```bash
docker-compose logs -f api
docker-compose logs -f ui
```

### Metrics

Consider adding Prometheus + Grafana for production monitoring:
```bash
docker run -p 9090:9090 prom/prometheus
docker run -p 3000:3000 grafana/grafana
```

## Scaling

### Horizontal Scaling

Use load balancer with multiple API instances:
```bash
docker-compose up -d --scale api=3
```

### Data Persistence

Mount volumes for data:
```yaml
volumes:
  - type: bind
    source: ./data
    target: /usr/src/app/data
```

### Caching

Add Redis for future enhancements:
```bash
docker run -p 6379:6379 redis:alpine
```

## Backup & Recovery

### Backup Data

```bash
docker cp llf-api:/usr/src/app/data ./data-backup
tar czf data-backup.tar.gz data-backup/
```

### Restore Data

```bash
tar xzf data-backup.tar.gz
docker cp data-backup/data llf-api:/usr/src/app/
```

## Security Best Practices

1. **Use environment variables** for sensitive data
2. **Enable HTTPS** with Let's Encrypt
3. **Set CORS origins** explicitly
4. **Use secrets manager** for production
5. **Keep images updated** - regularly rebuild with latest deps
6. **Implement rate limiting** at reverse proxy level
7. **Use .env.example** template, never commit .env
8. **Enable container security scanning** (Trivy, Snyk)

## Troubleshooting

### Container won't start

Check logs:
```bash
docker-compose logs api
```

### Port already in use

Change port in docker-compose.yml or `.env`:
```yaml
ports:
  - "5001:5000"  # Use port 5001 instead
```

### Data lost after restart

Ensure volumes are mounted:
```bash
docker inspect llf-api | grep -A 5 Mounts
```

### API can't reach files

Check volume mounts:
```bash
docker-compose exec api ls -la /usr/src/app/data/
```
