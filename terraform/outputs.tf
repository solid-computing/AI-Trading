# Terraform outputs for AI Trading Bot infrastructure

output "instance_id" {
  description = "ID of the created VPS instance"
  value       = openstack_compute_instance_v2.ai_trading_vps.id
}

output "instance_name" {
  description = "Name of the created VPS instance"
  value       = openstack_compute_instance_v2.ai_trading_vps.name
}

output "public_ip" {
  description = "Public IP address of the VPS"
  value       = openstack_networking_floatingip_v2.ai_trading_fip.address
}

output "private_ip" {
  description = "Private IP address of the VPS"
  value       = openstack_compute_instance_v2.ai_trading_vps.access_ip_v4
}

output "ssh_connection_command" {
  description = "SSH command to connect to the VPS"
  value       = "ssh -i ~/.ssh/id_rsa ${var.deploy_user}@${openstack_networking_floatingip_v2.ai_trading_fip.address}"
}

output "instance_flavor" {
  description = "Instance flavor used"
  value       = var.instance_flavor
}

output "instance_region" {
  description = "Region where instance is deployed"
  value       = var.ovh_region
}

output "security_group_id" {
  description = "Security group ID"
  value       = openstack_networking_secgroup_v2.ai_trading_secgroup.id
}

output "ssh_key_name" {
  description = "Name of the SSH key pair"
  value       = openstack_compute_keypair_v2.ai_trading_keypair.name
}

output "data_volume_id" {
  description = "ID of the data volume (if created)"
  value       = var.create_data_volume ? openstack_blockstorage_volume_v3.ai_trading_data[0].id : null
}

output "freqtrade_ui_url" {
  description = "URL for FreqUI interface (if enabled)"
  value       = var.enable_freqtrade_ui ? "http://${openstack_networking_floatingip_v2.ai_trading_fip.address}:8080" : "FreqUI not enabled"
}

# Environment information
output "environment_info" {
  description = "Environment and deployment information"
  value = {
    project_name = var.project_name
    environment  = var.environment
    region       = var.ovh_region
    created_at   = timestamp()
  }
}

# Connection details for CI/CD
output "deployment_vars" {
  description = "Variables needed for deployment scripts"
  value = {
    OVH_HOST = openstack_networking_floatingip_v2.ai_trading_fip.address
    OVH_USER = var.deploy_user
  }
  sensitive = false
}

# Cost estimation helper
output "estimated_monthly_cost" {
  description = "Estimated monthly cost in EUR (approximate)"
  value = {
    instance_cost = var.instance_flavor == "s1-2" ? "3-5 EUR" : var.instance_flavor == "s1-4" ? "6-8 EUR" : "10+ EUR"
    storage_cost  = var.create_data_volume ? "${var.data_volume_size * 0.04} EUR" : "0 EUR"
    total_note    = "Costs are approximate. Check OVH pricing for exact rates."
  }
}