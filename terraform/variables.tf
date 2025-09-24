# Variables for OVH Cloud Terraform configuration

# OVH API Configuration
variable "ovh_endpoint" {
  description = "OVH API endpoint (ovh-eu, ovh-us, ovh-ca, kimsufi-eu, kimsufi-ca, soyoustart-eu, soyoustart-ca)"
  type        = string
  default     = "ovh-eu"
}

variable "ovh_application_key" {
  description = "OVH API application key"
  type        = string
  sensitive   = true
}

variable "ovh_application_secret" {
  description = "OVH API application secret"
  type        = string
  sensitive   = true
}

variable "ovh_consumer_key" {
  description = "OVH API consumer key"
  type        = string
  sensitive   = true
}

variable "ovh_project_id" {
  description = "OVH Public Cloud project ID"
  type        = string
}

variable "ovh_region" {
  description = "OVH region for deployment"
  type        = string
  default     = "GRA9"
}

# OpenStack Configuration
variable "openstack_auth_url" {
  description = "OpenStack authentication URL"
  type        = string
  default     = "https://auth.cloud.ovh.net/v3/"
}

variable "openstack_username" {
  description = "OpenStack username (usually same as OVH username)"
  type        = string
}

variable "openstack_password" {
  description = "OpenStack password"
  type        = string
  sensitive   = true
}

# Project Configuration
variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "ai-trading-bot"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

# Instance Configuration
variable "instance_flavor" {
  description = "OVH instance flavor/type"
  type        = string
  default     = "s1-2"  # 1 vCPU, 2GB RAM, 10GB SSD - good for small trading bot
  
  validation {
    condition = contains([
      "s1-2",   # 1 vCPU, 2GB RAM, 10GB SSD
      "s1-4",   # 1 vCPU, 4GB RAM, 20GB SSD  
      "s1-8",   # 2 vCPU, 8GB RAM, 40GB SSD
      "b2-7",   # 2 vCPU, 7GB RAM, 50GB SSD
      "b2-15",  # 4 vCPU, 15GB RAM, 100GB SSD
    ], var.instance_flavor)
    error_message = "Instance flavor must be one of the supported OVH flavors."
  }
}

variable "instance_image" {
  description = "Operating system image name"
  type        = string
  default     = "Ubuntu 22.04"
}

# SSH Configuration
variable "ssh_public_key_path" {
  description = "Path to SSH public key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "deploy_user" {
  description = "Username for deployment and application management"
  type        = string
  default     = "freqtrade"
}

# Network Configuration
variable "floating_ip_pool" {
  description = "Floating IP pool name"
  type        = string
  default     = "Ext-Net"
}

variable "allowed_ip_range" {
  description = "IP range allowed to access the instance (CIDR notation)"
  type        = string
  default     = "0.0.0.0/0"  # Allow from anywhere - restrict this in production
}

# Security Configuration
variable "enable_freqtrade_ui" {
  description = "Enable FreqUI web interface access (port 8080)"
  type        = bool
  default     = false  # Disabled by default for security
}

variable "enable_http_access" {
  description = "Enable HTTP access (port 80) for health checks/webhooks"
  type        = bool
  default     = false
}

variable "enable_https_access" {
  description = "Enable HTTPS access (port 443)"
  type        = bool
  default     = false
}

# Storage Configuration
variable "create_data_volume" {
  description = "Create additional volume for persistent data storage"
  type        = bool
  default     = true
}

variable "data_volume_size" {
  description = "Size of the data volume in GB"
  type        = number
  default     = 20
  
  validation {
    condition     = var.data_volume_size >= 10 && var.data_volume_size <= 1000
    error_message = "Data volume size must be between 10 and 1000 GB."
  }
}

# Cost optimization
variable "enable_monitoring" {
  description = "Enable OVH monitoring services"
  type        = bool
  default     = false  # Additional cost
}

variable "backup_enabled" {
  description = "Enable automatic backups"
  type        = bool
  default     = false  # Additional cost
}