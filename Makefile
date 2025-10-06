# Makefile for Freqtrade Trading Bot
# Provides convenient commands for development, testing, and deployment

.PHONY: help validate build up down logs clean test lint deploy deploy-terraform terraform-init terraform-plan terraform-apply terraform-destroy terraform-output terraform-deploy setup-telegram generate-pdf

# Default target
help:
	@echo "🤖 Freqtrade Trading Bot - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "Development:"
	@echo "  validate      - Validate complete setup"
	@echo "  build         - Build Docker image"
	@echo "  up            - Start bot in dry-run mode"
	@echo "  down          - Stop bot"
	@echo "  logs          - Show bot logs"
	@echo "  clean         - Clean Docker containers and images"
	@echo ""
	@echo "Testing:"
	@echo "  test          - Run basic tests and validations"
	@echo "  lint          - Run linting on strategy files"
	@echo ""
	@echo "Configuration:"
	@echo "  update-config - Update config files with pairs from pairs.json"
	@echo "  setup-telegram - Helper to setup Telegram bot (requires TOKEN)"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy        - Deploy to VPS (requires environment variables)"
	@echo "  deploy-terraform - Deploy to Terraform-provisioned VPS"
	@echo ""
	@echo "Infrastructure (Terraform):"
	@echo "  terraform-deploy  - Deploy infrastructure with Terraform"
	@echo "  terraform-init    - Initialize Terraform"
	@echo "  terraform-plan    - Plan Terraform deployment"
	@echo "  terraform-apply   - Apply Terraform configuration"
	@echo "  terraform-output  - Show Terraform outputs"
	@echo "  terraform-destroy - Destroy Terraform infrastructure"
	@echo ""
	@echo "Documentation:"
	@echo "  generate-pdf      - Generate PDF documentation for end users"
	@echo ""
	@echo "Examples:"
	@echo "  make validate"
	@echo "  make up"
	@echo "  make logs"
	@echo "  make setup-telegram TOKEN=your_bot_token"
	@echo "  make generate-pdf"

# Validation
validate:
	@echo "🔍 Validating setup..."
	@python3 scripts/validate-setup.py

# Docker commands
build:
	@echo "🏗️ Building Docker image..."
	@docker-compose build

up:
	@echo "🚀 Starting Freqtrade bot (dry-run mode)..."
	@docker-compose up -d
	@echo "✅ Bot started! Check logs with: make logs"

down:
	@echo "🛑 Stopping Freqtrade bot..."
	@docker-compose down

logs:
	@echo "📋 Showing bot logs (press Ctrl+C to exit)..."
	@docker-compose logs -f freqtrade

clean:
	@echo "🧹 Cleaning Docker containers and images..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f

# Testing
test: validate lint
	@echo "✅ All tests passed!"

lint:
	@echo "🔍 Running linting checks..."
	@python3 -m py_compile user_data/strategies/RsiMaStrategy.py
	@echo "✅ Strategy syntax is valid"

# Configuration
update-config:
	@echo "⚙️ Updating configuration files..."
	@python3 scripts/update-config.py

setup-telegram:
	@echo "📱 Setting up Telegram bot..."
	@if [ -z "$(TOKEN)" ]; then \
		echo "❌ Usage: make setup-telegram TOKEN=your_bot_token"; \
		exit 1; \
	fi
	@python3 scripts/setup-telegram.py $(TOKEN)

# Deployment
deploy:
	@echo "🚀 Deploying to VPS..."
	@if [ -z "$(OVH_HOST)" ] || [ -z "$(OVH_USER)" ]; then \
		echo "❌ Missing environment variables: OVH_HOST, OVH_USER"; \
		exit 1; \
	fi
	@chmod +x deployment/deploy.sh
	@./deployment/deploy.sh

# Enhanced deployment with Terraform support
deploy-terraform:
	@echo "🚀 Deploying to Terraform-provisioned VPS..."
	@chmod +x deployment/deploy-terraform.sh
	@./deployment/deploy-terraform.sh

# Terraform infrastructure management
terraform-init:
	@echo "🏗️ Initializing Terraform..."
	@cd terraform && terraform init

terraform-plan:
	@echo "📋 Planning Terraform deployment..."
	@cd terraform && terraform plan

terraform-apply:
	@echo "🚀 Applying Terraform configuration..."
	@cd terraform && terraform apply

terraform-destroy:
	@echo "💥 Destroying Terraform infrastructure..."
	@cd terraform && terraform destroy

terraform-output:
	@echo "📊 Terraform outputs..."
	@cd terraform && terraform output

# Terraform deployment helper
terraform-deploy:
	@echo "🏗️ Deploying infrastructure with Terraform..."
	@chmod +x terraform/deploy.sh
	@cd terraform && ./deploy.sh

# Development helpers
install-dev:
	@echo "📦 Installing development dependencies..."
	@pip3 install --user black flake8 isort

format:
	@echo "🎨 Formatting code..."
	@black user_data/strategies/
	@isort user_data/strategies/

# Status check
status:
	@echo "📊 Checking bot status..."
	@docker-compose ps
	@echo ""
	@if docker-compose ps | grep -q "freqtrade.*Up"; then \
		echo "✅ Bot is running"; \
	else \
		echo "⚠️ Bot is not running"; \
	fi

# Quick start
quick-start: validate build up
	@echo ""
	@echo "🎉 Quick start complete!"
	@echo "📋 Check logs: make logs"
	@echo "🛑 Stop bot: make down"

# Documentation
generate-pdf:
	@echo "📄 Generating PDF documentation..."
	@chmod +x scripts/generate-pdf.sh
	@./scripts/generate-pdf.sh