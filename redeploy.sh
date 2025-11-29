#!/bin/bash

# Redeploy script for Masumi agent
set -e

echo "🔨 Building Docker image..."
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v1 .

echo "📤 Pushing Docker image to registry..."
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v1

echo "🔄 Restarting Kubernetes deployment..."
kubectl rollout restart deployment/python-api

echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/python-api

echo "✅ Deployment complete! Checking pod status..."
kubectl get pods -l app=python-api

echo ""
echo "📋 To view logs, run:"
echo "   kubectl logs -f deployment/python-api"
echo ""
echo "🔍 To test the availability endpoint:"
echo "   curl http://161.156.165.133.nip.io/availability"

# Made with Bob
