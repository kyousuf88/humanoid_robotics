# Deployment Guide for RAG Chatbot

This guide provides instructions for deploying the RAG Chatbot application in a production environment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Compose Deployment](#docker-compose-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Environment Configuration](#environment-configuration)
5. [SSL Configuration](#ssl-configuration)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Scaling and Performance](#scaling-and-performance)

## Prerequisites

Before deploying the application, ensure you have:

- Docker and Docker Compose installed (for Docker deployment)
- Kubernetes cluster (for Kubernetes deployment)
- API keys for:
  - Cohere
  - OpenAI
  - Qdrant Cloud
- Database connection string for Neon Serverless Postgres
- SSL certificates (for HTTPS)

## Docker Compose Deployment

### 1. Prepare Environment File

Copy the production environment template and fill in your values:

```bash
cp backend/.env.prod .env
# Edit .env file with your actual values
```

### 2. Create SSL Directory

```bash
mkdir -p ssl
# Place your SSL certificate files in the ssl directory:
# - cert.pem (your certificate)
# - key.pem (your private key)
```

### 3. Create Nginx Directory

```bash
mkdir -p nginx/conf.d
```

### 4. Deploy with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Verify Deployment

```bash
# Check if all services are running
docker-compose -f docker-compose.prod.yml ps

# Check application logs
docker-compose -f docker-compose.prod.yml logs backend
```

## Kubernetes Deployment

### 1. Prepare Kubernetes Secrets

Encode your sensitive information in base64:

```bash
# Example for encoding a secret
echo -n 'your-secret-value' | base64
```

Update the `k8s/secrets.yaml` file with your base64-encoded values.

### 2. Apply Kubernetes Configurations

```bash
# Create namespace (optional)
kubectl create namespace rag-chatbot

# Apply secrets
kubectl apply -f k8s/secrets.yaml

# Apply deployment
kubectl apply -f k8s/deployment.yaml
```

### 3. Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress
```

## Environment Configuration

The following environment variables are available for configuration:

### API and Service Configuration
- `COHERE_API_KEY`: Your Cohere API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_URL`: URL for Qdrant Cloud instance
- `NEON_DATABASE_URL`: Connection string for Neon Serverless Postgres

### Application Settings
- `SECRET_KEY`: Secret key for cryptographic operations
- `DEBUG`: Set to "false" for production
- `LOG_LEVEL`: Log level (INFO, WARNING, ERROR)

### Rate Limiting
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per window (default: 100)
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 3600)

### Model Configuration
- `COHERE_MODEL`: Cohere model to use (default: embed-multilingual-v3.0)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4)

### Performance and Caching
- `CACHE_ENABLED`: Enable/disable caching (default: true)
- `CACHE_SIZE`: Maximum number of cached items (default: 2000)
- `CACHE_DEFAULT_TTL`: Default TTL for cached items in seconds (default: 7200)

## SSL Configuration

For HTTPS support, you need to provide SSL certificates:

1. Place your certificate file as `ssl/cert.pem`
2. Place your private key as `ssl/key.pem`
3. Update the nginx configuration if using different paths

## Monitoring and Logging

The application includes built-in monitoring capabilities:

### Metrics Endpoint
- Access metrics at: `https://your-domain.com/v1/metrics`
- Access alerts at: `https://your-domain.com/v1/alerts`

### Health Check
- Health endpoint: `https://your-domain.com/v1/health`

## Scaling and Performance

### Backend Scaling
- The backend is configured to run with 4 workers by default
- Adjust the number of workers in the Dockerfile if needed
- For Kubernetes, adjust the replica count in deployment.yaml

### Cache Configuration
- Default cache size is 2000 items
- TTL is set to 2 hours (7200 seconds) by default
- Adjust CACHE_SIZE and CACHE_DEFAULT_TTL based on your needs

### Rate Limiting
- Default is 100 requests per hour per session
- Adjust RATE_LIMIT_REQUESTS and RATE_LIMIT_WINDOW as needed

## Security Considerations

1. **Secrets Management**: Never commit API keys to version control
2. **SSL/TLS**: Always use HTTPS in production
3. **Rate Limiting**: The application includes rate limiting to prevent abuse
4. **Data Retention**: User data is automatically deleted after 30 days
5. **Non-root User**: The application runs as a non-root user in containers

## Troubleshooting

### Common Issues

1. **Connection Timeouts**: Verify that all service URLs are accessible
2. **API Key Errors**: Check that all API keys are correctly configured
3. **Database Connection**: Ensure the database URL is properly formatted
4. **SSL Issues**: Verify certificate files are in the correct location and format

### Logs
- Docker: `docker-compose -f docker-compose.prod.yml logs -f backend`
- Kubernetes: `kubectl logs -l app=rag-chatbot -f`

## Maintenance

### Cache Management
- Clear cache: `POST /v1/cache/clear`
- Invalidate specific question: `POST /v1/cache/question/invalidate`

### Health Checks
Regularly monitor the health endpoint to ensure all services are operational.