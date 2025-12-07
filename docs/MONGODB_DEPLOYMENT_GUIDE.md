# MongoDB-Based High Availability Deployment Guide

This guide explains how to deploy RiskLens AI with MongoDB for distributed job storage, enabling multiple replicas for high availability with disk-based persistent storage.

## Why MongoDB Instead of Redis?

### Redis (RAM-based)
- ❌ Stores data in RAM (expensive, limited)
- ❌ Requires AOF/RDB for persistence (slower)
- ❌ Not ideal for large datasets
- ✅ Very fast for small data

### MongoDB (Disk-based)
- ✅ Stores data on disk (uses your 1TB efficiently)
- ✅ Native persistence (no extra configuration)
- ✅ Better for large datasets
- ✅ Indexed queries for fast lookups
- ✅ Lower memory footprint

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Sokosumi                             │
│                    (Payment Gateway)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    NGINX Ingress                             │
│              (Load Balancer + TLS)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Python API Service                          │
│                   (ClusterIP)                                │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌─────────────────┐            ┌─────────────────┐
│  Python API     │            │  Python API     │
│  Pod 1          │◄──────────►│  Pod 2          │
│  (Replica 1)    │  MongoDB   │  (Replica 2)    │
└────────┬────────┘            └────────┬────────┘
         │                               │
         └───────────────┬───────────────┘
                         ▼
                 ┌───────────────┐
                 │  MongoDB Pod  │
                 │  (Disk-based  │
                 │   Storage)    │
                 └───────┬───────┘
                         │
                         ▼
         ┌───────────────────────────────┐
         │  Your 1TB Disk (vdd)          │
         │  /mnt/instana/stanctl/objects │
         │  /mongodb-data                │
         └───────────────────────────────┘
```

## Files Modified

### 1. `requirements.txt`
Replaced Redis with MongoDB:
```
motor==3.3.2        # Async MongoDB driver
pymongo==4.6.1      # MongoDB Python driver
```

### 2. `mongo_store.py` (NEW)
MongoDB helper module with methods:
- `connect()` - Connect to MongoDB
- `set_job()` - Store job data
- `get_job()` - Retrieve job data
- `update_job()` - Update job fields
- `delete_job()` - Remove job data
- `get_all_jobs()` - List all jobs

### 3. `main.py`
Updated to use MongoDB:
- Import `mongo_store` instead of `redis_store`
- Startup event: Connect to MongoDB
- Shutdown event: Disconnect from MongoDB
- All job operations now use MongoDB

### 4. `deploy.yaml`
Replaced Redis with MongoDB:
- MongoDB deployment (lines 14-52)
- MongoDB service (lines 54-67)
- MongoDB environment variables (lines 112-117)
- HostPath volume pointing to `/mnt/instana/stanctl/objects/mongodb-data`

## Storage Comparison

### Redis Storage (RAM-based)
```
┌─────────────────────────────────────┐
│  Redis Pod                          │
│  ┌───────────────────────────┐     │
│  │  RAM (256MB limit)        │     │
│  │  - Jobs stored in memory  │     │
│  │  - AOF writes to disk     │     │
│  └───────────┬───────────────┘     │
│              │ (slow)               │
│              ▼                      │
│  ┌───────────────────────────┐     │
│  │  Disk (/data)             │     │
│  │  - AOF log file           │     │
│  └───────────────────────────┘     │
└─────────────────────────────────────┘
```

### MongoDB Storage (Disk-based)
```
┌─────────────────────────────────────┐
│  MongoDB Pod                        │
│  ┌───────────────────────────┐     │
│  │  RAM (256MB - for cache)  │     │
│  │  - Working set only       │     │
│  └───────────┬───────────────┘     │
│              │ (fast)               │
│              ▼                      │
│  ┌───────────────────────────┐     │
│  │  Disk (/data/db)          │     │
│  │  - All jobs stored here   │     │
│  │  - Indexed for speed      │     │
│  └───────────────────────────┘     │
└─────────────────────────────────────┘
```

## Deployment Steps

### Step 1: Update Secrets
Edit `deploy.yaml` lines 8-12 with your actual values:
```yaml
stringData:
  payment_api_key: "YOUR_ACTUAL_PAYMENT_API_KEY"
  agent_identifier: "YOUR_ACTUAL_AGENT_IDENTIFIER"
  seller_vkey: "YOUR_ACTUAL_SELLER_VKEY"
  openai_api_key: "YOUR_ACTUAL_OPENAI_API_KEY"
  blockfrost_project_id: "YOUR_ACTUAL_BLOCKFROST_PROJECT_ID"
```

### Step 2: Build and Push Docker Image
```bash
# Build the image with MongoDB support
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v3 .

# Push to registry
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v3
```

### Step 3: Update Image in deploy.yaml
Change line 107 to use the new image:
```yaml
image: ghcr.io/vinaycharlie01/local-llama-agent-python:v3
```

### Step 4: Deploy to Kubernetes
```bash
# Apply the deployment
kubectl apply -f deploy.yaml

# Verify MongoDB is running
kubectl get pods -l app=mongodb

# Verify API pods are running (should see 2)
kubectl get pods -l app=python-api

# Check MongoDB connection in logs
kubectl logs -l app=python-api --tail=20 | grep MongoDB
```

### Step 5: Verify Deployment
```bash
# Check all pods
kubectl get pods

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# python-api-xxxxx-xxxxx        1/1     Running   0          1m
# python-api-xxxxx-xxxxx        1/1     Running   0          1m
# mongodb-xxxxx-xxxxx           1/1     Running   0          1m

# Test the API
curl http://161.156.165.133.nip.io/health
curl http://161.156.165.133.nip.io/availability
```

## MongoDB Operations

### Connect to MongoDB
```bash
# Get MongoDB pod name
kubectl get pods -l app=mongodb

# Connect to MongoDB shell
kubectl exec -it mongodb-xxxxx-xxxxx -- mongosh risklens
```

### Query Jobs
```javascript
// List all jobs
db.jobs.find()

// Find specific job
db.jobs.findOne({job_id: "YOUR_JOB_ID"})

// Count jobs by status
db.jobs.countDocuments({status: "completed"})

// List all completed jobs
db.jobs.find({status: "completed"})

// Delete old jobs
db.jobs.deleteMany({status: "completed"})
```

### Check Indexes
```javascript
// List indexes
db.jobs.getIndexes()

// Expected indexes:
// - job_id (unique)
// - status
// - blockchain_identifier
```

### Database Stats
```javascript
// Database statistics
db.stats()

// Collection statistics
db.jobs.stats()
```

## Disk Usage

### Check MongoDB Data Size
```bash
# On your node
du -sh /mnt/instana/stanctl/objects/mongodb-data

# Inside MongoDB pod
kubectl exec -it mongodb-xxxxx-xxxxx -- du -sh /data/db
```

### Monitor Disk Usage
```bash
# Watch disk usage in real-time
watch -n 5 'du -sh /mnt/instana/stanctl/objects/mongodb-data'
```

## Benefits

✅ **Disk-Based Storage**: Uses your 1TB disk efficiently  
✅ **Lower Memory**: Only 256MB RAM vs Redis's need for full dataset in RAM  
✅ **Native Persistence**: No AOF/RDB configuration needed  
✅ **Indexed Queries**: Fast lookups with automatic indexing  
✅ **Scalable**: Can store millions of jobs  
✅ **High Availability**: 2 API replicas + persistent MongoDB  
✅ **Better for Large Data**: Handles large result objects efficiently  

## Performance Comparison

### Redis
- **Memory**: 256MB (limited by RAM)
- **Max Jobs**: ~1,000 jobs (with 256KB each)
- **Persistence**: AOF writes (slower)
- **Query Speed**: Very fast (in-memory)

### MongoDB
- **Memory**: 256MB (working set cache)
- **Max Jobs**: Millions (limited by disk)
- **Persistence**: Native (fast)
- **Query Speed**: Fast (indexed)

## Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB pod is running
kubectl get pods -l app=mongodb

# Check MongoDB logs
kubectl logs -l app=mongodb

# Test MongoDB connectivity from API pod
kubectl exec -it $(kubectl get pod -l app=python-api -o jsonpath='{.items[0].metadata.name}') -- nc -zv mongodb 27017
```

### Job Not Found (404)
```bash
# Connect to MongoDB and check
kubectl exec -it mongodb-xxxxx-xxxxx -- mongosh risklens --eval 'db.jobs.findOne({job_id: "YOUR_JOB_ID"})'
```

### Disk Full
```bash
# Check disk usage
df -h /mnt/instana/stanctl/objects

# Clean old jobs
kubectl exec -it mongodb-xxxxx-xxxxx -- mongosh risklens --eval 'db.jobs.deleteMany({status: "completed", createdAt: {$lt: new Date(Date.now() - 7*24*60*60*1000)}})'
```

## Backup & Restore

### Backup MongoDB
```bash
# Backup to your disk
kubectl exec mongodb-xxxxx-xxxxx -- mongodump --db risklens --out /data/db/backup

# Copy backup to local machine
kubectl cp mongodb-xxxxx-xxxxx:/data/db/backup ./mongodb-backup
```

### Restore MongoDB
```bash
# Copy backup to pod
kubectl cp ./mongodb-backup mongodb-xxxxx-xxxxx:/data/db/restore

# Restore database
kubectl exec mongodb-xxxxx-xxxxx -- mongorestore --db risklens /data/db/restore/risklens
```

## Scaling

### Scale API Replicas
```bash
# Scale to 3 replicas
kubectl scale deployment python-api --replicas=3

# Scale to 5 replicas
kubectl scale deployment python-api --replicas=5
```

### MongoDB Replication (Advanced)
For production, consider MongoDB replica set:
- 3 MongoDB pods for high availability
- Automatic failover
- Read replicas for better performance

## Production Recommendations

1. **MongoDB Replica Set**: Use 3 MongoDB replicas for HA
2. **Authentication**: Add MongoDB username/password
3. **Monitoring**: Add Prometheus metrics
4. **Backup**: Automated daily backups
5. **Retention**: Auto-delete old jobs after 30 days
6. **Indexes**: Add custom indexes for your queries
7. **Compression**: Enable MongoDB compression

## Migration from Redis

If you had Redis before:
```bash
# 1. Deploy MongoDB alongside Redis
kubectl apply -f deploy.yaml

# 2. Verify MongoDB is working
kubectl logs -l app=python-api | grep "Connected to MongoDB"

# 3. Delete Redis (data will be lost)
kubectl delete deployment redis
kubectl delete service redis

# 4. Clean up Redis data
sudo rm -rf /mnt/instana/stanctl/objects/redis-data
```

## Support

For issues or questions, check:
- Pod logs: `kubectl logs -l app=python-api`
- MongoDB logs: `kubectl logs -l app=mongodb`
- Events: `kubectl get events --sort-by='.lastTimestamp'`
- MongoDB shell: `kubectl exec -it mongodb-xxxxx-xxxxx -- mongosh risklens`


