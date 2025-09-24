#!/bin/bash

# Deployment script for CircleCI
# This script deploys the Freqtrade bot to the OVH VPS

set -e

echo "Starting deployment to OVH VPS..."

# Variables (set by CircleCI environment)
VPS_USER=${OVH_USER}
VPS_HOST=${OVH_HOST}
DEPLOY_PATH="/home/freqtrade/AI-Trading"

# Create temporary directory for deployment files
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Prepare deployment package
echo "Preparing deployment package..."
cp -r . $TEMP_DIR/
cd $TEMP_DIR

# Remove unnecessary files for production
rm -rf .git .gitignore README.md .circleci deployment/setup-vps.sh
rm -f config.dryrun.json  # Only deploy live template

# Create config.live.json from template with environment substitution
envsubst < config.live.template.json > config.live.json

echo "Deploying to VPS..."

# Stop the service
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "sudo systemctl stop freqtrade || true"

# Backup existing deployment
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "
  if [ -d $DEPLOY_PATH ]; then
    sudo cp -r $DEPLOY_PATH ${DEPLOY_PATH}.backup.$(date +%Y%m%d_%H%M%S)
  fi
"

# Deploy new version
echo "Copying files to VPS..."
rsync -avz --delete \
  --exclude='.git*' \
  --exclude='user_data/logs/' \
  --exclude='user_data/backtest_results/' \
  --exclude='user_data/data/' \
  $TEMP_DIR/ $VPS_USER@$VPS_HOST:$DEPLOY_PATH/

# Set proper permissions
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "
  sudo chown -R freqtrade:freqtrade $DEPLOY_PATH
  chmod +x $DEPLOY_PATH/deployment/*.sh
"

# Pull latest Docker images
echo "Pulling Docker images..."
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "
  cd $DEPLOY_PATH
  sudo docker-compose -f docker-compose.prod.yml pull
"

# Start the service
echo "Starting Freqtrade service..."
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "
  sudo systemctl start freqtrade
  sudo systemctl status freqtrade --no-pager
"

# Wait for service to be ready
echo "Waiting for service to be ready..."
sleep 10

# Check service status
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "
  sudo systemctl is-active freqtrade
  sudo docker ps | grep freqtrade || true
"

echo "Deployment completed successfully!"
echo "Service status:"
ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST "sudo systemctl status freqtrade --no-pager"