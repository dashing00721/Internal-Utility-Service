# Internal Utility Service

A production-grade Flask API deployed on AWS EC2 with Docker,
Nginx, HTTPS and automated CI/CD using GitHub Actions.

## Architecture
- GitHub — source of truth
- GitHub Actions — CI/CD pipeline
- Docker Hub — image registry
- AWS EC2 — cloud server
- Nginx — reverse proxy
- Let's Encrypt — SSL certificates
- AWS Secrets Manager — runtime secrets

## Dockerfile Structure
The Dockerfile uses a single stage build that installs all
dependencies and runs the Flask app as a non-root user for
security. A HEALTHCHECK is included to monitor the app.

## CI/CD Pipeline
1. Run tests with pytest
2. Lint code with flake8
3. Build Docker image
4. Push to Docker Hub
5. Deploy to EC2 automatically

## Tagging Strategy
- latest — most recent build
- v1.0.0 — stable release
- commit SHA — exact version tracking

## Secret Injection
- GitHub Secrets — used during CI/CD pipeline
- AWS Secrets Manager — used at runtime on EC2
- No secrets in source code or Docker images

## HTTPS Setup
- Nginx configured as reverse proxy
- Certbot installed on EC2
- Let's Encrypt SSL certificate obtained
- HTTP automatically redirects to HTTPS
- Certificate auto-renews every 90 days

## Update Strategy
Rolling update — new container replaces old one:
1. Pull new image from Docker Hub
2. Stop old container
3. Start new container
4. Zero downtime deployment

## Rollback Method
To rollback to previous version:
docker stop myapp
docker rm myapp
docker run -d --restart always --name myapp \
dashing007/internal-utility:v1.0.0 -p 5000:5000

## Reflection Questions

### 1. Why did you structure the Dockerfile the way you did?
I structured the Dockerfile to be simple and secure. The app runs
as a non-root user to prevent security vulnerabilities. A
HEALTHCHECK is included so Docker knows when the app is unhealthy
and can restart it automatically.

### 2. Why multi-stage build?
Multi-stage builds keep the final image small by separating the
build environment from the production environment. This reduces
the attack surface and makes deployments faster.

### 3. Why that tagging strategy?
Using latest, semantic versioning and commit SHA gives full
traceability. Latest is for quick deployments, v1.0.0 is for
stable releases and SHA tags let you trace exactly which code
is running in production.

### 4. Why GitHub Secrets and AWS Secrets Manager split?
GitHub Secrets handle CI/CD credentials safely during the pipeline.
AWS Secrets Manager handles runtime secrets on the server. This
separation means secrets are never exposed in logs or source code.

### 5. How does deployment avoid downtime?
The pipeline stops the old container and starts the new one
immediately. The process takes only a few seconds so users
experience minimal interruption.

### 6. How would you scale to multiple EC2 instances?
Use a load balancer in front of multiple EC2 instances. Push
the same Docker image to all instances and use a shared database.
AWS Auto Scaling can add more instances when traffic increases.

### 7. What security risks still exist?
Debug mode is still on in Flask which should be turned off in
production. The database credentials are still in config.py and
should be moved to AWS Secrets Manager completely.

### 8. How would you evolve this into Kubernetes?
Replace Docker run commands with Kubernetes deployment files.
Use Kubernetes services for load balancing and secrets for
credential management. This allows automatic scaling and
self-healing of containers.
