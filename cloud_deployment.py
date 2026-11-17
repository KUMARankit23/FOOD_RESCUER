"""
Cloud Deployment Configuration
Docker containerization and cloud platform configs (AWS, GCP, Azure)
CI/CD pipeline setup
"""

import json
from typing import Dict, List, Any, Literal, Optional
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Cloud platforms"""
    DOCKER = "docker"
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class DeploymentConfig:
    """Base deployment configuration"""
    
    def __init__(self, platform: Platform):
        self.platform = platform
        self.created_at = datetime.now().isoformat()
        self.config: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "platform": self.platform.value,
            "created_at": self.created_at,
            "config": self.config
        }


class DockerDeploymentConfig(DeploymentConfig):
    """Docker containerization configuration"""
    
    def __init__(self):
        super().__init__(Platform.DOCKER)
        self._generate_dockerfile()
        self._generate_docker_compose()
    
    def _generate_dockerfile(self):
        """Generate Dockerfile"""
        dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV STREAMLIT_SERVER_PORT=8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "api.py"]
"""
        self.config["dockerfile"] = dockerfile
    
    def _generate_docker_compose(self):
        """Generate docker-compose.yml"""
        compose = {
            "version": "3.8",
            "services": {
                "api": {
                    "build": ".",
                    "ports": ["8000:8000"],
                    "environment": {
                        "API_HOST": "0.0.0.0",
                        "API_PORT": "8000"
                    },
                    "networks": ["food_rescue"],
                    "restart_policy": {
                        "condition": "on-failure",
                        "delay": "5s",
                        "max_attempts": 5
                    }
                },
                "dashboard": {
                    "build": ".",
                    "command": "streamlit run streamlit_dashboard.py",
                    "ports": ["8501:8501"],
                    "networks": ["food_rescue"],
                    "depends_on": ["api"]
                }
            },
            "networks": {
                "food_rescue": {
                    "driver": "bridge"
                }
            }
        }
        self.config["docker_compose"] = compose
    
    def get_dockerfile(self) -> str:
        """Get Dockerfile content"""
        return self.config.get("dockerfile", "")
    
    def get_docker_compose_yaml(self) -> str:
        """Get docker-compose content"""
        import yaml
        try:
            return yaml.dump(self.config.get("docker_compose", {}))
        except:
            return json.dumps(self.config.get("docker_compose", {}), indent=2)


class AWSDeploymentConfig(DeploymentConfig):
    """AWS deployment configuration"""
    
    def __init__(self, region: str = "us-east-1"):
        super().__init__(Platform.AWS)
        self.region = region
        self._generate_configs()
    
    def _generate_configs(self):
        """Generate AWS deployment configs"""
        
        # ECR configuration
        self.config["ecr"] = {
            "repository_name": "food-rescue-mas",
            "region": self.region,
            "image_tag": "latest"
        }
        
        # ECS Task Definition
        self.config["ecs_task_definition"] = {
            "family": "food-rescue-task",
            "networkMode": "awsvpc",
            "requiresCompatibilities": ["FARGATE"],
            "cpu": "256",
            "memory": "512",
            "containerDefinitions": [
                {
                    "name": "food-rescue-api",
                    "image": f"ACCOUNT_ID.dkr.ecr.{self.region}.amazonaws.com/food-rescue-mas:latest",
                    "portMappings": [
                        {
                            "containerPort": 8000,
                            "protocol": "tcp"
                        }
                    ],
                    "environment": [
                        {"name": "API_HOST", "value": "0.0.0.0"},
                        {"name": "API_PORT", "value": "8000"}
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "/ecs/food-rescue",
                            "awslogs-region": self.region,
                            "awslogs-stream-prefix": "ecs"
                        }
                    }
                }
            ]
        }
        
        # ECS Service
        self.config["ecs_service"] = {
            "serviceName": "food-rescue-service",
            "cluster": "food-rescue-cluster",
            "taskDefinition": "food-rescue-task",
            "desiredCount": 1,
            "launchType": "FARGATE",
            "loadBalancers": [
                {
                    "targetGroupArn": "arn:aws:elasticloadbalancing:REGION:ACCOUNT:targetgroup/food-rescue/...",
                    "containerName": "food-rescue-api",
                    "containerPort": 8000
                }
            ]
        }
        
        # ALB Configuration
        self.config["alb"] = {
            "name": "food-rescue-alb",
            "type": "application",
            "scheme": "internet-facing",
            "listeners": [
                {
                    "protocol": "HTTP",
                    "port": 80,
                    "defaultActions": [
                        {
                            "type": "forward",
                            "targetGroupArn": "..."
                        }
                    ]
                }
            ]
        }
        
        # Auto Scaling
        self.config["autoscaling"] = {
            "min_capacity": 1,
            "max_capacity": 5,
            "target_cpu_utilization": 70,
            "target_memory_utilization": 80
        }
    
    def get_deployment_commands(self) -> List[str]:
        """Get AWS deployment commands"""
        return [
            "# 1. Build and push Docker image to ECR",
            f"aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.{self.region}.amazonaws.com",
            "docker build -t food-rescue-mas:latest .",
            f"docker tag food-rescue-mas:latest ACCOUNT_ID.dkr.ecr.{self.region}.amazonaws.com/food-rescue-mas:latest",
            f"docker push ACCOUNT_ID.dkr.ecr.{self.region}.amazonaws.com/food-rescue-mas:latest",
            "",
            "# 2. Create ECS Cluster",
            "aws ecs create-cluster --cluster-name food-rescue-cluster --region " + self.region,
            "",
            "# 3. Register Task Definition",
            "aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json --region " + self.region,
            "",
            "# 4. Create ECS Service",
            "aws ecs create-service --cli-input-json file://ecs-service.json --region " + self.region
        ]


class GCPDeploymentConfig(DeploymentConfig):
    """Google Cloud Platform deployment configuration"""
    
    def __init__(self, project_id: str, region: str = "us-central1"):
        super().__init__(Platform.GCP)
        self.project_id = project_id
        self.region = region
        self._generate_configs()
    
    def _generate_configs(self):
        """Generate GCP deployment configs"""
        
        # Cloud Run Configuration
        self.config["cloud_run"] = {
            "serviceName": "food-rescue-service",
            "image": f"gcr.io/{self.project_id}/food-rescue-mas:latest",
            "region": self.region,
            "platform": "managed",
            "memory": "512Mi",
            "cpu": "1",
            "timeout": "3600s",
            "environment_variables": {
                "API_HOST": "0.0.0.0",
                "API_PORT": "8080"
            }
        }
        
        # Cloud Build Configuration
        self.config["cloud_build"] = {
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/docker",
                    "args": ["build", "-t", f"gcr.io/{self.project_id}/food-rescue-mas:latest", "."]
                },
                {
                    "name": "gcr.io/cloud-builders/docker",
                    "args": ["push", f"gcr.io/{self.project_id}/food-rescue-mas:latest"]
                },
                {
                    "name": "gcr.io/cloud-builders/gke-deploy",
                    "args": [
                        "run",
                        "--filename=k8s/",
                        "--image=gcr.io/" + self.project_id + "/food-rescue-mas:latest",
                        "--location=" + self.region
                    ]
                }
            ],
            "images": [f"gcr.io/{self.project_id}/food-rescue-mas:latest"]
        }
        
        # GKE Deployment
        self.config["gke_deployment"] = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "food-rescue",
                "namespace": "default"
            },
            "spec": {
                "replicas": 3,
                "selector": {
                    "matchLabels": {
                        "app": "food-rescue"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "food-rescue"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "food-rescue",
                                "image": f"gcr.io/{self.project_id}/food-rescue-mas:latest",
                                "ports": [
                                    {
                                        "containerPort": 8000
                                    }
                                ],
                                "resources": {
                                    "requests": {
                                        "cpu": "100m",
                                        "memory": "128Mi"
                                    },
                                    "limits": {
                                        "cpu": "500m",
                                        "memory": "512Mi"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    
    def get_deployment_commands(self) -> List[str]:
        """Get GCP deployment commands"""
        return [
            f"# Set GCP project",
            f"gcloud config set project {self.project_id}",
            "",
            f"# Build and push Docker image",
            f"gcloud builds submit --tag gcr.io/{self.project_id}/food-rescue-mas:latest",
            "",
            f"# Deploy to Cloud Run",
            f"gcloud run deploy food-rescue-service \\",
            f"  --image gcr.io/{self.project_id}/food-rescue-mas:latest \\",
            f"  --region {self.region} \\",
            f"  --platform managed \\",
            f"  --memory 512Mi \\",
            f"  --allow-unauthenticated",
            "",
            f"# Or deploy to GKE",
            f"gcloud container clusters create food-rescue-cluster --region {self.region}",
            f"kubectl apply -f k8s/deployment.yaml"
        ]


class AzureDeploymentConfig(DeploymentConfig):
    """Microsoft Azure deployment configuration"""
    
    def __init__(self, resource_group: str, region: str = "eastus"):
        super().__init__(Platform.AZURE)
        self.resource_group = resource_group
        self.region = region
        self._generate_configs()
    
    def _generate_configs(self):
        """Generate Azure deployment configs"""
        
        # Container Instances
        self.config["container_instances"] = {
            "name": "food-rescue-container",
            "resourceGroup": self.resource_group,
            "image": f"foodrescuemasregistry.azurecr.io/food-rescue-mas:latest",
            "cpu": 1,
            "memory": 1,
            "ports": [
                {
                    "port": 8000,
                    "protocol": "TCP"
                }
            ]
        }
        
        # App Service
        self.config["app_service"] = {
            "resourceGroup": self.resource_group,
            "name": "food-rescue-app",
            "kind": "Linux",
            "sku": {
                "name": "B2",
                "tier": "Basic"
            }
        }
        
        # Application Insights
        self.config["app_insights"] = {
            "resourceGroup": self.resource_group,
            "name": "food-rescue-insights",
            "applicationType": "web",
            "kind": "python"
        }
    
    def get_deployment_commands(self) -> List[str]:
        """Get Azure deployment commands"""
        return [
            f"# Login to Azure",
            f"az login",
            "",
            f"# Create resource group",
            f"az group create --name {self.resource_group} --location {self.region}",
            "",
            f"# Create container registry",
            f"az acr create --resource-group {self.resource_group} --name foodrescuemasregistry --sku Basic",
            "",
            f"# Build and push image",
            f"az acr build --registry foodrescuemasregistry --image food-rescue-mas:latest .",
            "",
            f"# Deploy to Container Instances",
            f"az container create \\",
            f"  --resource-group {self.resource_group} \\",
            f"  --name food-rescue-container \\",
            f"  --image foodrescuemasregistry.azurecr.io/food-rescue-mas:latest \\",
            f"  --cpu 1 --memory 1",
            "",
            f"# Or deploy to App Service",
            f"az appservice plan create --name food-rescue-plan --resource-group {self.resource_group}",
            f"az webapp create --resource-group {self.resource_group} --plan food-rescue-plan --name food-rescue-app"
        ]


class DeploymentManager:
    """Manages deployment configurations for all platforms"""
    
    def __init__(self):
        self.deployments: Dict[Platform, DeploymentConfig] = {}
    
    def create_docker_deployment(self) -> DockerDeploymentConfig:
        """Create Docker deployment config"""
        config = DockerDeploymentConfig()
        self.deployments[Platform.DOCKER] = config
        print("✓ Created Docker deployment config")
        return config
    
    def create_aws_deployment(self, region: str = "us-east-1") -> AWSDeploymentConfig:
        """Create AWS deployment config"""
        config = AWSDeploymentConfig(region)
        self.deployments[Platform.AWS] = config
        print(f"✓ Created AWS deployment config (region: {region})")
        return config
    
    def create_gcp_deployment(self, project_id: str, region: str = "us-central1") -> GCPDeploymentConfig:
        """Create GCP deployment config"""
        config = GCPDeploymentConfig(project_id, region)
        self.deployments[Platform.GCP] = config
        print(f"✓ Created GCP deployment config (project: {project_id})")
        return config
    
    def create_azure_deployment(self, resource_group: str, region: str = "eastus") -> AzureDeploymentConfig:
        """Create Azure deployment config"""
        config = AzureDeploymentConfig(resource_group, region)
        self.deployments[Platform.AZURE] = config
        print(f"✓ Created Azure deployment config (resource group: {resource_group})")
        return config
    
    def get_deployment(self, platform: Platform) -> Optional[DeploymentConfig]:
        """Get deployment config for a platform"""
        return self.deployments.get(platform)
    
    def print_all_deployment_commands(self):
        """Print deployment commands for all platforms"""
        print("\n" + "=" * 70)
        print("DEPLOYMENT COMMANDS FOR ALL PLATFORMS")
        print("=" * 70)
        
        for platform, config in self.deployments.items():
            print(f"\n{platform.value.upper()} DEPLOYMENT")
            print("-" * 70)
            
            if hasattr(config, 'get_deployment_commands'):
                commands = config.get_deployment_commands()
                for cmd in commands:
                    print(cmd)


# Global deployment manager
deployment_manager = DeploymentManager()


def generate_all_deployment_configs():
    """Generate deployment configs for all platforms"""
    print("=" * 70)
    print("GENERATING DEPLOYMENT CONFIGURATIONS")
    print("=" * 70)
    
    # Docker
    deployment_manager.create_docker_deployment()
    
    # AWS
    deployment_manager.create_aws_deployment(region="us-east-1")
    
    # GCP
    deployment_manager.create_gcp_deployment(project_id="food-rescue-mas", region="us-central1")
    
    # Azure
    deployment_manager.create_azure_deployment(resource_group="food-rescue-rg", region="eastus")
    
    print("\n✓ All deployment configurations generated")


if __name__ == "__main__":
    # Generate configurations
    generate_all_deployment_configs()
    
    # Print Docker config
    print("\n" + "=" * 70)
    print("DOCKER CONFIGURATION")
    print("=" * 70)
    docker_config = deployment_manager.get_deployment(Platform.DOCKER)
    if docker_config:
        print(docker_config.get_dockerfile()[:500] + "...")
    
    # Print all commands
    deployment_manager.print_all_deployment_commands()
    
    print("\n✓ Deployment configuration complete")
