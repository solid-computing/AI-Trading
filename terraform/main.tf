# Main Terraform configuration for AI Trading Bot on OVH Cloud
terraform {
  required_version = ">= 1.0"
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 0.45"
    }
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.54"
    }
  }
}

# Configure OVH provider
provider "ovh" {
  endpoint          = var.ovh_endpoint
  application_key   = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key      = var.ovh_consumer_key
}

# Configure OpenStack provider for OVH Public Cloud
provider "openstack" {
  auth_url    = var.openstack_auth_url
  domain_name = "default"
  tenant_name = var.ovh_project_id
  user_name   = var.openstack_username
  password    = var.openstack_password
  region      = var.ovh_region
}

# Create SSH key pair
resource "openstack_compute_keypair_v2" "ai_trading_keypair" {
  name       = "${var.project_name}-keypair"
  public_key = file(var.ssh_public_key_path)
}

# Create security group
resource "openstack_networking_secgroup_v2" "ai_trading_secgroup" {
  name        = "${var.project_name}-secgroup"
  description = "Security group for AI Trading Bot"
}

# SSH access rule
resource "openstack_networking_secgroup_rule_v2" "ssh_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.ai_trading_secgroup.id
}

# FreqUI access rule (optional, for development)
resource "openstack_networking_secgroup_rule_v2" "freqtrade_ui_rule" {
  count             = var.enable_freqtrade_ui ? 1 : 0
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 8080
  port_range_max    = 8080
  remote_ip_prefix  = var.allowed_ip_range
  security_group_id = openstack_networking_secgroup_v2.ai_trading_secgroup.id
}

# HTTP access rule (for health checks, webhooks)
resource "openstack_networking_secgroup_rule_v2" "http_rule" {
  count             = var.enable_http_access ? 1 : 0
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 80
  port_range_max    = 80
  remote_ip_prefix  = var.allowed_ip_range
  security_group_id = openstack_networking_secgroup_v2.ai_trading_secgroup.id
}

# HTTPS access rule
resource "openstack_networking_secgroup_rule_v2" "https_rule" {
  count             = var.enable_https_access ? 1 : 0
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 443
  port_range_max    = 443
  remote_ip_prefix  = var.allowed_ip_range
  security_group_id = openstack_networking_secgroup_v2.ai_trading_secgroup.id
}

# Get available flavors (instance types)
data "openstack_compute_flavor_v2" "ai_trading_flavor" {
  name = var.instance_flavor
}

# Get Ubuntu image
data "openstack_images_image_v2" "ubuntu" {
  name        = var.instance_image
  most_recent = true
}

# Create the VPS instance
resource "openstack_compute_instance_v2" "ai_trading_vps" {
  name        = "${var.project_name}-vps"
  image_id    = data.openstack_images_image_v2.ubuntu.id
  flavor_id   = data.openstack_compute_flavor_v2.ai_trading_flavor.id
  key_pair    = openstack_compute_keypair_v2.ai_trading_keypair.name
  
  security_groups = [openstack_networking_secgroup_v2.ai_trading_secgroup.name]

  # User data script for initial setup
  user_data = templatefile("${path.module}/cloud-init.yml", {
    project_name = var.project_name
    deploy_user  = var.deploy_user
  })

  # Metadata
  metadata = {
    Name        = "${var.project_name}-vps"
    Environment = var.environment
    Project     = "AI-Trading-Bot"
    ManagedBy   = "Terraform"
  }

  tags = [
    "ai-trading",
    var.environment,
    "freqtrade"
  ]
}

# Create and attach a floating IP
resource "openstack_networking_floatingip_v2" "ai_trading_fip" {
  pool = var.floating_ip_pool
}

resource "openstack_compute_floatingip_associate_v2" "ai_trading_fip_associate" {
  floating_ip = openstack_networking_floatingip_v2.ai_trading_fip.address
  instance_id = openstack_compute_instance_v2.ai_trading_vps.id
}

# Optional: Create a volume for persistent data
resource "openstack_blockstorage_volume_v3" "ai_trading_data" {
  count = var.create_data_volume ? 1 : 0
  name  = "${var.project_name}-data"
  size  = var.data_volume_size
  
  metadata = {
    Environment = var.environment
    Project     = "AI-Trading-Bot"
    ManagedBy   = "Terraform"
  }
}

resource "openstack_compute_volume_attach_v2" "ai_trading_data_attach" {
  count       = var.create_data_volume ? 1 : 0
  instance_id = openstack_compute_instance_v2.ai_trading_vps.id
  volume_id   = openstack_blockstorage_volume_v3.ai_trading_data[0].id
}