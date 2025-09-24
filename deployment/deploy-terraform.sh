#!/bin/bash

# Enhanced deployment script for Terraform-provisioned infrastructure
# This script can deploy to infrastructure created by Terraform or manually

set -e

echo "Starting deployment to OVH VPS (Terraform-compatible)..."

# Variables (can be set from environment, Terraform outputs, or manually)
VPS_USER=${OVH_USER:-${TERRAFORM_USER:-freqtrade}}
VPS_HOST=${OVH_HOST:-${TERRAFORM_HOST}}
DEPLOY_PATH="/home/${VPS_USER}/AI-Trading"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to get Terraform outputs if available
get_terraform_vars() {
    local terraform_dir="../terraform"
    
    if [[ -d "$terraform_dir" ]] && [[ -f "$terraform_dir/terraform.tfstate" ]]; then
        log_info "Found Terraform state, extracting connection details..."
        
        cd "$terraform_dir"
        
        # Get outputs from Terraform
        TERRAFORM_HOST=$(terraform output -raw public_ip 2>/dev/null || echo "")
        TERRAFORM_USER=$(terraform output -raw deployment_vars 2>/dev/null | grep OVH_USER | cut -d'"' -f4 || echo "freqtrade")
        
        if [[ -n "$TERRAFORM_HOST" ]] && [[ -z "$VPS_HOST" ]]; then
            VPS_HOST="$TERRAFORM_HOST"
            log_success "Using Terraform host: $VPS_HOST"
        fi
        
        if [[ -n "$TERRAFORM_USER" ]] && [[ "$VPS_USER" == "freqtrade" ]]; then
            VPS_USER="$TERRAFORM_USER"
            log_success "Using Terraform user: $VPS_USER"
        fi
        
        cd - > /dev/null
    fi
}

# Validation
validate_environment() {
    if [[ -z "$VPS_USER" ]] || [[ -z "$VPS_HOST" ]]; then
        log_error "Missing required environment variables!"
        echo ""
        echo "Set manually:"
        echo "  export OVH_USER=freqtrade"
        echo "  export OVH_HOST=your_vps_ip"
        echo ""
        echo "Or use Terraform outputs:"
        echo "  cd terraform && ./deploy.sh"
        echo "  cd .. # back to project root"
        echo "  export OVH_HOST=\$(cd terraform && terraform output -raw public_ip)"
        echo "  export OVH_USER=freqtrade"
        echo ""
        exit 1
    fi
    
    log_success "Deployment target: $VPS_USER@$VPS_HOST"
}

# Test SSH connectivity
test_ssh_connection() {
    log_info "Testing SSH connection..."
    
    if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "echo 'SSH connection successful'" > /dev/null 2>&1; then
        log_success "SSH connection established"
    else
        log_error "Cannot connect to $VPS_USER@$VPS_HOST"
        log_info "Make sure:"
        echo "  1. VPS is running and accessible"
        echo "  2. SSH key is properly configured"
        echo "  3. Security group allows SSH access"
        echo "  4. User '$VPS_USER' exists on the VPS"
        exit 1
    fi
}

# Create temporary directory for deployment files
prepare_deployment_package() {
    log_info "Preparing deployment package..."
    
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT
    
    # Copy project files
    cp -r . "$TEMP_DIR/"
    cd "$TEMP_DIR"
    
    # Remove unnecessary files for production
    rm -rf .git .gitignore README.md .circleci deployment/setup-vps.sh
    rm -rf terraform/  # Don't deploy terraform files
    rm -f config.dryrun.json  # Only deploy live template
    
    # Create config.live.json from template with environment substitution
    if [[ -f "config.live.template.json" ]]; then
        envsubst < config.live.template.json > config.live.json
        log_success "Generated config.live.json from template"
    fi
    
    log_success "Deployment package prepared"
}

# Deploy to VPS
deploy_to_vps() {
    log_info "Deploying to VPS..."
    
    # Stop the service if it exists
    log_info "Stopping freqtrade service..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "sudo systemctl stop freqtrade || true"
    
    # Backup existing deployment
    log_info "Creating backup of existing deployment..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        if [ -d $DEPLOY_PATH ]; then
            sudo cp -r $DEPLOY_PATH ${DEPLOY_PATH}.backup.\$(date +%Y%m%d_%H%M%S)
        fi
    "
    
    # Deploy new version
    log_info "Copying files to VPS..."
    rsync -avz --delete \
        --exclude='.git*' \
        --exclude='user_data/logs/' \
        --exclude='user_data/backtest_results/' \
        --exclude='user_data/data/' \
        --exclude='terraform/' \
        "$TEMP_DIR/" "$VPS_USER@$VPS_HOST:$DEPLOY_PATH/"
    
    # Set proper permissions
    log_info "Setting permissions..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        sudo chown -R $VPS_USER:$VPS_USER $DEPLOY_PATH
        chmod +x $DEPLOY_PATH/deployment/*.sh
    "
    
    # Update systemd service if needed
    log_info "Updating systemd service..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        if [ -f $DEPLOY_PATH/deployment/freqtrade.service ]; then
            sudo cp $DEPLOY_PATH/deployment/freqtrade.service /etc/systemd/system/
            sudo systemctl daemon-reload
            sudo systemctl enable freqtrade
        fi
    "
    
    # Pull latest Docker images
    log_info "Pulling Docker images..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        cd $DEPLOY_PATH
        sudo docker-compose -f docker-compose.prod.yml pull
    "
    
    log_success "Application deployed successfully"
}

# Start services
start_services() {
    log_info "Starting Freqtrade service..."
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        sudo systemctl start freqtrade
        sudo systemctl status freqtrade --no-pager
    "
    
    # Wait for service to be ready
    log_info "Waiting for service to be ready..."
    sleep 10
    
    # Check service status
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        sudo systemctl is-active freqtrade
        sudo docker ps | grep freqtrade || true
    "
    
    log_success "Services started successfully"
}

# Show deployment summary
show_summary() {
    log_success "Deployment completed successfully!"
    echo ""
    echo "📊 Deployment Summary:"
    echo "======================"
    echo "Target: $VPS_USER@$VPS_HOST"
    echo "Deploy Path: $DEPLOY_PATH"
    echo ""
    echo "🔧 Management Commands:"
    echo "sudo systemctl status freqtrade   # Check status"
    echo "sudo systemctl restart freqtrade  # Restart service" 
    echo "journalctl -u freqtrade -f        # View logs"
    echo "docker-compose logs -f            # View application logs"
    echo ""
    
    # Check if FreqUI is enabled
    ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "
        if sudo netstat -tlnp | grep -q :8080; then
            echo '🌐 FreqUI: http://$VPS_HOST:8080'
        fi
    " || true
}

# Main deployment process
main() {
    echo "🚀 AI Trading Bot - Enhanced Deployment"
    echo "======================================="
    
    get_terraform_vars
    validate_environment
    test_ssh_connection
    prepare_deployment_package
    deploy_to_vps
    start_services
    show_summary
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "stop")
        validate_environment
        log_info "Stopping freqtrade service..."
        ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "sudo systemctl stop freqtrade"
        log_success "Service stopped"
        ;;
    "start")
        validate_environment
        log_info "Starting freqtrade service..."
        ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "sudo systemctl start freqtrade"
        log_success "Service started"
        ;;
    "status")
        validate_environment
        ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "sudo systemctl status freqtrade --no-pager"
        ;;
    "logs")
        validate_environment
        ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "journalctl -u freqtrade -f"
        ;;
    "help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy  - Deploy application (default)"
        echo "  start   - Start freqtrade service"
        echo "  stop    - Stop freqtrade service"
        echo "  status  - Show service status"
        echo "  logs    - Show service logs"
        echo "  help    - Show this help"
        ;;
    *)
        log_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac