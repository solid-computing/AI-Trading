#!/bin/bash

# Quick start script for Terraform deployment
# This script guides users through the Terraform setup

set -e

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

echo "🚀 AI Trading Bot - Terraform Quick Start"
echo "========================================="
echo ""

# Check if we're in the terraform directory
if [[ ! -f "main.tf" ]]; then
    log_error "Please run this script from the terraform/ directory"
    exit 1
fi

# Step 1: Check prerequisites
log_info "Step 1: Checking prerequisites..."

# Check Terraform
if ! command -v terraform &> /dev/null; then
    log_error "Terraform not found!"
    echo ""
    echo "Install Terraform:"
    echo "  Ubuntu/Debian: wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg"
    echo "  Then: echo 'deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com \\$(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/hashicorp.list"
    echo "  Finally: sudo apt update && sudo apt install terraform"
    echo ""
    echo "  macOS: brew install terraform"
    echo ""
    echo "  Or download from: https://www.terraform.io/downloads"
    exit 1
fi

log_success "Terraform found: $(terraform version | head -n1)"

# Step 2: Check configuration
log_info "Step 2: Checking configuration..."

if [[ ! -f "terraform.tfvars" ]]; then
    log_warning "terraform.tfvars not found"
    
    if [[ -f "terraform.tfvars.example" ]]; then
        echo ""
        echo "Would you like to create terraform.tfvars from the example? (y/n)"
        read -r create_vars
        
        if [[ "$create_vars" == "y" || "$create_vars" == "Y" ]]; then
            cp terraform.tfvars.example terraform.tfvars
            log_success "Created terraform.tfvars"
            echo ""
            log_warning "Please edit terraform.tfvars with your actual OVH credentials:"
            echo "  nano terraform.tfvars"
            echo ""
            echo "You need:"
            echo "  - OVH API keys from https://api.ovh.com/createToken/"
            echo "  - OVH project ID"
            echo "  - OVH username and password"
            echo ""
            echo "After editing terraform.tfvars, run this script again."
            exit 0
        else
            echo ""
            log_error "terraform.tfvars is required for deployment"
            echo "Copy the example file and fill in your credentials:"
            echo "  cp terraform.tfvars.example terraform.tfvars"
            echo "  nano terraform.tfvars"
            exit 1
        fi
    fi
else
    log_success "terraform.tfvars found"
fi

# Check SSH key
SSH_KEY_PATH=$(grep ssh_public_key_path terraform.tfvars | cut -d'"' -f2 | sed "s|~|$HOME|")
if [[ ! -f "$SSH_KEY_PATH" ]]; then
    log_error "SSH public key not found at: $SSH_KEY_PATH"
    echo ""
    echo "Generate an SSH key pair:"
    echo "  ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C 'ai-trading-bot'"
    echo ""
    echo "Or update the ssh_public_key_path in terraform.tfvars"
    exit 1
fi

log_success "SSH key found at: $SSH_KEY_PATH"

# Step 3: Deploy
log_info "Step 3: Ready to deploy!"
echo ""
echo "This will:"
echo "  1. Initialize Terraform"
echo "  2. Plan the deployment"
echo "  3. Create OVH infrastructure"
echo "  4. Set up a VPS with Docker and required software"
echo ""
echo "Estimated cost: €3-15/month depending on instance size"
echo ""
echo "Proceed with deployment? (y/n)"
read -r proceed

if [[ "$proceed" != "y" && "$proceed" != "Y" ]]; then
    log_info "Deployment cancelled"
    exit 0
fi

# Initialize Terraform
log_info "Initializing Terraform..."
terraform init

# Plan deployment
log_info "Planning deployment..."
terraform plan -out=tfplan

echo ""
log_warning "Review the plan above. Proceed with apply? (y/n)"
read -r apply_confirm

if [[ "$apply_confirm" != "y" && "$apply_confirm" != "Y" ]]; then
    log_info "Deployment cancelled"
    rm -f tfplan
    exit 0
fi

# Apply deployment
log_info "Applying Terraform configuration..."
terraform apply tfplan
rm -f tfplan

# Show results
log_success "Infrastructure deployed successfully!"
echo ""
echo "📊 Deployment Results:"
echo "======================"
terraform output

echo ""
log_success "Next steps:"
echo "1. Copy the public IP address"
echo "2. Go back to the project root: cd .."
echo "3. Deploy the application: make deploy-terraform"
echo ""
echo "Or set environment variables and use the original deployment:"
echo "  export OVH_HOST=\$(cd terraform && terraform output -raw public_ip)"
echo "  export OVH_USER=freqtrade"
echo "  make deploy"
echo ""
log_info "Your VPS is ready for the AI Trading Bot!"