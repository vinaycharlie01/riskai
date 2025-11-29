#!/bin/bash

# RiskLens AI - Quick Deployment Script
# This script rebuilds and redeploys the agent to Kubernetes

set -e

echo "🛡️  RiskLens AI - Quick Deployment"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="ghcr.io/vinaycharlie01/local-llama-agent-python:v1"
DEPLOYMENT_NAME="python-api"

echo -e "${BLUE}Step 1: Building Docker image...${NC}"
docker build -t $IMAGE_NAME .

echo ""
echo -e "${BLUE}Step 2: Pushing to registry...${NC}"
docker push $IMAGE_NAME

echo ""
echo -e "${BLUE}Step 3: Restarting Kubernetes deployment...${NC}"
kubectl rollout restart deployment/$DEPLOYMENT_NAME

echo ""
echo -e "${BLUE}Step 4: Waiting for rollout to complete...${NC}"
kubectl rollout status deployment/$DEPLOYMENT_NAME --timeout=300s

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""

# Get pod status
echo -e "${BLUE}Current pod status:${NC}"
kubectl get pods -l app=$DEPLOYMENT_NAME

echo ""
echo -e "${BLUE}Recent logs:${NC}"
kubectl logs deployment/$DEPLOYMENT_NAME --tail=20

echo ""
echo "=================================="
echo -e "${GREEN}🎉 RiskLens AI is now deployed!${NC}"
echo "=================================="
echo ""
echo "📋 Next steps:"
echo "  1. Test availability: curl http://161.156.165.133.nip.io/availability"
echo "  2. View logs: kubectl logs -f deployment/$DEPLOYMENT_NAME"
echo "  3. Check Masumi dashboard for your agent"
echo ""
echo "🔍 Useful commands:"
echo "  - View logs: kubectl logs -f deployment/$DEPLOYMENT_NAME"
echo "  - Check status: kubectl get pods -l app=$DEPLOYMENT_NAME"
echo "  - Describe pod: kubectl describe pod -l app=$DEPLOYMENT_NAME"
echo ""

# Made with Bob
