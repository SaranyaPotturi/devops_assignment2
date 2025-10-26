# Ticket Booking Application - Complete DevOps Project

## Project Overview
A full-stack ticket booking web application demonstrating complete DevOps workflow including Git version control, Docker containerization, Jenkins CI/CD pipeline, and Kubernetes orchestration.

## Technology Stack

### Frontend
- HTML5
- CSS3 (Tailwind CSS via CDN)
- Vanilla JavaScript

### Backend
- Python 3.11
- Flask
- Flask-CORS

### DevOps Tools
- **Version Control**: Git, GitHub
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins
- **Container Registry**: Docker Hub
- **Orchestration**: Kubernetes (Minikube)

## Project Structure
```
ticket-booking-app/
├── frontend/
│   └── index.html              # Frontend application
├── backend/
│   ├── app.py                  # Flask backend API
│   └── requirements.txt        # Python dependencies
├── kubernetes/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
├── Dockerfile.backend          # Backend containerization
├── Dockerfile.frontend         # Frontend containerization
├── docker-compose.yml          # Local development setup
├── Jenkinsfile                 # CI/CD pipeline definition
├── .gitignore
└── README.md
```

## Prerequisites

- Docker Desktop installed and running
- Git installed and configured
- Jenkins running (port 8081)
- Minikube installed (for Kubernetes)
- Docker Hub account
- GitHub account

## Setup Instructions

### 1. Git Version Control Setup

#### Initialize Repository
```bash
cd ticket-booking-app
git init
git add .
git commit -m "Initial commit: Ticket booking application"
```

#### Implement GitFlow Branching Strategy
```bash
# Create develop branch
git checkout -b develop

# Create feature branch
git checkout -b feature/booking-system
git add .
git commit -m "Add booking system feature"

# Merge to develop
git checkout develop
git merge feature/booking-system

# Create release branch
git checkout -b release/v1.0
git commit -m "Prepare release v1.0" --allow-empty

# Merge to main
git checkout -b main
git merge release/v1.0
git tag -a v1.0 -m "Version 1.0"

# Merge back to develop
git checkout develop
git merge release/v1.0
```

#### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/ticket-booking-app.git
git push -u origin main
git push -u origin develop
git push --tags
```

### 2. Docker Containerization

#### Build Docker Images
```bash
# Build backend image
docker build -f Dockerfile.backend -t YOUR_DOCKERHUB_USERNAME/tickethub-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t YOUR_DOCKERHUB_USERNAME/tickethub-frontend:latest .
```

#### Verify Images
```bash
docker images | findstr tickethub
```

#### Test Locally with Docker Compose
```bash
# Start containers
docker-compose up -d

# Verify containers are running
docker ps

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000/api/health

# Stop containers
docker-compose down
```

#### Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Push images
docker push YOUR_DOCKERHUB_USERNAME/tickethub-backend:latest
docker push YOUR_DOCKERHUB_USERNAME/tickethub-frontend:latest
```

### 3. Jenkins CI/CD Pipeline Setup

#### Start Jenkins
```bash
docker run -d --name jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

#### Get Initial Admin Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### Access Jenkins
- URL: http://localhost:8081
- Enter admin password
- Install suggested plugins
- Create admin user

#### Install Required Plugins
Navigate to: Manage Jenkins → Plugins → Available
- Docker Pipeline
- Docker plugin
- Kubernetes plugin
- Git plugin

#### Add Docker Hub Credentials
1. Go to: Manage Jenkins → Credentials → System → Global
2. Click "Add Credentials"
3. Select "Username with password"
4. Username: YOUR_DOCKERHUB_USERNAME
5. Password: YOUR_DOCKERHUB_PASSWORD
6. ID: `dockerhub-credentials`
7. Click OK

#### Create Pipeline Job
1. New Item → Name: `tickethub-pipeline` → Pipeline → OK
2. Configure:
   - Build Triggers: ✓ Poll SCM
   - Schedule: `H/5 * * * *`
   - Pipeline Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/YOUR_USERNAME/ticket-booking-app.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. Save

#### Trigger Build
- Click "Build Now"
- Monitor console output

### 4. Kubernetes Deployment

#### Start Minikube
```bash
minikube start --driver=docker
```

#### Verify Kubernetes
```bash
kubectl version --client
kubectl get nodes
minikube status
```

#### Deploy Application
```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml
```

#### Verify Deployment
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

#### Access Application
```bash
# Get service URLs
minikube service frontend-service --url
minikube service backend-service --url
```

#### Scale Application
```bash
# Scale to 5 replicas
kubectl scale deployment backend-deployment --replicas=5
kubectl scale deployment frontend-deployment --replicas=5

# Verify scaling
kubectl get pods
```

## API Endpoints

### Backend API (Port 5000)
- `GET /api/health` - Health check endpoint
- `GET /api/events` - Get all events
- `GET /api/events/<id>` - Get specific event
- `POST /api/bookings` - Create new booking
- `GET /api/bookings` - Get all bookings
- `GET /api/bookings/<id>` - Get specific booking
- `DELETE /api/bookings/<id>` - Cancel booking

### Example API Call
```bash
# Health check
curl http://localhost:5000/api/health

# Get all events
curl http://localhost:5000/api/events

# Create booking
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "venue_id": 1,
    "time": "5:00 PM",
    "seats": 2
  }'
```

## CI/CD Pipeline Stages

The Jenkins pipeline consists of the following stages:

1. **Checkout**: Clone code from GitHub
2. **Build Backend**: Build backend Docker image
3. **Build Frontend**: Build frontend Docker image
4. **Test**: Run health check tests on backend
5. **Push to Docker Hub**: Push images to Docker registry
6. **Deploy to Kubernetes**: Deploy to Kubernetes cluster

### Pipeline Workflow
```
Git Push → Jenkins Trigger → Build Images → Run Tests → Push to Docker Hub → Deploy to K8s
```

## Testing the Complete Workflow

### 1. Make Code Change
Edit `backend/app.py`:
```python
"status": "healthy - v2.0"  # Change version
```

### 2. Commit and Push
```bash
git add .
git commit -m "Update health check to v2.0"
git push origin main
```

### 3. Watch Pipeline Execute
- Jenkins automatically triggers build (within 5 minutes)
- All stages execute automatically
- Application updates in Kubernetes

### 4. Verify Deployment
```bash
kubectl get pods
curl http://$(minikube ip):30001/api/health
# Should show v2.0
```
## Commands Reference

### Docker Commands
```bash
# Build image
docker build -f Dockerfile.backend -t image-name .

# Run container
docker run -d -p 5000:5000 image-name

# View running containers
docker ps

# View logs
docker logs container-name

# Stop container
docker stop container-name

# Remove container
docker rm container-name

# Remove image
docker rmi image-name

# Clean up
docker system prune -a
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# View branches
git branch -a

# View log
git log --oneline --graph --all
```

### Kubernetes Commands
```bash
# Get resources
kubectl get all
kubectl get pods
kubectl get deployments
kubectl get services

# Describe resource
kubectl describe pod pod-name

# View logs
kubectl logs pod-name

# Scale deployment
kubectl scale deployment name --replicas=5

# Delete resource
kubectl delete -f file.yaml

# Apply changes
kubectl apply -f file.yaml

# Rollout status
kubectl rollout status deployment/name
```
