#!/bin/bash

# Terraform deployment script for AI Trading Bot
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
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

# Check if terraform is installed
check_terraform() {
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform is not installed. Please install Terraform first."
        echo "Visit: https://www.terraform.io/downloads"
        exit 1
    fi
    
    log_info "Terraform version: $(terraform version | head -n1)"
}

# Check if required files exist
check_requirements() {
    if [[ ! -f "terraform.tfvars" ]]; then
        log_error "terraform.tfvars not found!"
        log_info "Copy terraform.tfvars.example to terraform.tfvars and fill in your values:"
        echo "  cp terraform.tfvars.example terraform.tfvars"
        echo "  nano terraform.tfvars"
        exit 1
    fi
    
    # Check if SSH key exists
    SSH_KEY_PATH=$(grep ssh_public_key_path terraform.tfvars | cut -d'"' -f2 | sed "s|~|$HOME|")
    if [[ ! -f "$SSH_KEY_PATH" ]]; then
        log_error "SSH public key not found at: $SSH_KEY_PATH"
        log_info "Generate an SSH key pair:"
        echo "  ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C 'ai-trading-bot'"
        exit 1
    fi
    
    log_success "Requirements check passed"
}

# Initialize Terraform
init_terraform() {
    log_info "Initializing Terraform..."
    terraform init
    log_success "Terraform initialized"
}

# Plan deployment
plan_deployment() {
    log_info "Planning Terraform deployment..."
    terraform plan -out=tfplan
    log_success "Terraform plan created"
}

# Apply deployment
apply_deployment() {
    log_info "Applying Terraform configuration..."
    terraform apply tfplan
    log_success "Infrastructure deployed successfully!"
    
    # Clean up plan file
    rm -f tfplan
}

# Show outputs
show_outputs() {
    log_info "Deployment outputs:"
    echo "===================="
    terraform output
    echo "===================="
    
    # Get specific outputs for easy copying
    PUBLIC_IP=$(terraform output -raw public_ip 2>/dev/null || echo "Not available")
    SSH_COMMAND=$(terraform output -raw ssh_connection_command 2>/dev/null || echo "Not available")
    
    log_success "VPS is ready!"
    echo ""
    echo "Public IP: $PUBLIC_IP"
    echo "SSH Command: $SSH_COMMAND"
    echo ""
    log_info "You can now deploy your trading bot using:"
    echo "  export OVH_HOST=$PUBLIC_IP"
    echo "  export OVH_USER=freqtrade"
    echo "  cd .. && make deploy"
}

# Destroy infrastructure
destroy_infrastructure() {
    log_warning "This will destroy all infrastructure created by Terraform!"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    
    if [[ "$confirm" == "yes" ]]; then
        log_info "Destroying infrastructure..."
        terraform destroy
        log_success "Infrastructure destroyed"
    else
        log_info "Destruction cancelled"
    fi
}

# Main function
main() {
    echo "🚀 AI Trading Bot - Terraform Deployment"
    echo "========================================"
    
    case "${1:-deploy}" in
        "deploy"|"apply")
            check_terraform
            check_requirements
            init_terraform
            plan_deployment
            apply_deployment
            show_outputs
            ;;
        "plan")
            check_terraform
            check_requirements
            init_terraform
            plan_deployment
            ;;
        "destroy")
            check_terraform
            destroy_infrastructure
            ;;
        "output"|"outputs")
            terraform output
            ;;
        "init")
            check_terraform
            init_terraform
            ;;
        "help"|"-h"|"--help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  deploy    - Deploy infrastructure (default)"
            echo "  plan      - Show deployment plan"
            echo "  destroy   - Destroy infrastructure"
            echo "  output    - Show deployment outputs"
            echo "  init      - Initialize Terraform"
            echo "  help      - Show this help"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"