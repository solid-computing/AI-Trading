# Terraform Infrastructure for AI Trading Bot

This document provides a comprehensive overview of the Terraform infrastructure implementation for deploying the AI Trading Bot on OVH Cloud.

## 🎯 Overview

The Terraform configuration automates the provisioning of cloud infrastructure on OVH Public Cloud, providing:

- **Infrastructure as Code**: Version-controlled, reproducible infrastructure
- **Automated VPS Setup**: Complete server configuration via cloud-init  
- **Security**: Proper firewall rules and SSH key management
- **Cost Optimization**: Right-sized instances with optional components
- **Integration**: Seamless integration with existing deployment scripts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     OVH Public Cloud                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │   VPS Instance   │    │  Security Group  │               │
│  │   - Ubuntu 22.04 │    │  - SSH (22)      │               │
│  │   - Docker       │    │  - FreqUI (8080) │               │
│  │   - AI Trading   │    │  - HTTP (80)     │               │
│  │     Bot          │    │  - HTTPS (443)   │               │
│  └─────────────────┘    └──────────────────┘               │
│           │                       │                        │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │ Floating IP     │    │   SSH Key Pair   │               │
│  │ (Public Access) │    │   (Authentication)│               │
│  └─────────────────┘    └──────────────────┘               │
│           │                       │                        │
│  ┌─────────────────┐    ┌──────────────────┐               │
│  │   Data Volume   │    │    Cloud-init    │               │
│  │  (Persistent    │    │   (Auto Setup)   │               │
│  │   Storage)      │    │                  │               │
│  └─────────────────┘    └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
terraform/
├── main.tf                     # Main infrastructure configuration
├── variables.tf                # Input variables definition
├── outputs.tf                  # Output values definition
├── cloud-init.yml              # VPS bootstrap script
├── terraform.tfvars.example    # Example configuration
├── deploy.sh                   # Deployment automation script
├── quick-start.sh              # Interactive setup guide
└── README.md                   # Detailed documentation
```

## 🚀 Key Features

### 1. **Complete VPS Provisioning**
- Ubuntu 22.04 LTS base image
- Configurable instance sizes (s1-2, s1-4, s1-8, etc.)
- Automated software installation via cloud-init
- Docker and Docker Compose pre-installed

### 2. **Security Configuration**
- Security groups with minimal required ports
- SSH key-based authentication
- Optional IP range restrictions
- Firewall (UFW) automatically configured

### 3. **Network Setup**
- Floating IP for public access
- Security group rules for selective port access
- Optional FreqUI web interface access

### 4. **Storage Options**
- Optional additional data volume for persistence
- Automatic volume mounting and formatting
- Configurable volume sizes

### 5. **Cost Optimization**
- Multiple instance size options
- Optional monitoring and backup services
- Easy teardown with `terraform destroy`

## 💰 Cost Breakdown

| Component | Size/Type | Monthly Cost (EUR) |
|-----------|-----------|-------------------|
| VPS s1-2  | 1 vCPU, 2GB RAM | €3-5 |
| VPS s1-4  | 1 vCPU, 4GB RAM | €6-8 |
| VPS s1-8  | 2 vCPU, 8GB RAM | €12-15 |
| Data Volume | 20GB SSD | €0.80 |
| Floating IP | 1 IP | Included |
| Monitoring | Optional | +€2-3 |
| Backups | Optional | +€1-2 |

**Recommended for small trading**: s1-2 instance ≈ **€4-6/month total**

## 🔧 Configuration Options

### Instance Types
```hcl
# Small trading bot (recommended)
instance_flavor = "s1-2"  # 1 vCPU, 2GB RAM, 10GB SSD

# Medium workload
instance_flavor = "s1-4"  # 1 vCPU, 4GB RAM, 20GB SSD

# High-frequency trading
instance_flavor = "s1-8"  # 2 vCPU, 8GB RAM, 40GB SSD
```

### Security Settings
```hcl
# Restrict access to your IP only (recommended)
allowed_ip_range = "1.2.3.4/32"

# Allow from anywhere (less secure)
allowed_ip_range = "0.0.0.0/0"

# Enable FreqUI web interface
enable_freqtrade_ui = true  # Adds port 8080 access
```

### Storage Configuration
```hcl
# Enable additional data volume
create_data_volume = true
data_volume_size   = 20  # GB

# Disable for cost savings
create_data_volume = false
```

## 🔄 Integration with Existing Deployment

The Terraform infrastructure seamlessly integrates with the existing deployment pipeline:

### 1. **Infrastructure Deployment**
```bash
# Deploy infrastructure
make terraform-deploy

# Get connection details
terraform output
```

### 2. **Application Deployment**
```bash
# Deploy trading bot to Terraform-provisioned VPS
make deploy-terraform

# Or manually:
export OVH_HOST=$(cd terraform && terraform output -raw public_ip)
export OVH_USER=freqtrade
./deployment/deploy-terraform.sh
```

### 3. **CI/CD Integration**
The existing CircleCI pipeline can be extended to:
- Use Terraform outputs for deployment targets
- Automatically provision infrastructure for new environments
- Tear down test environments after use

## 🛡️ Security Best Practices

### 1. **API Key Management**
- Never commit `terraform.tfvars` to version control
- Use OVH API keys with minimal required permissions
- Rotate API keys regularly

### 2. **Network Security**
- Restrict `allowed_ip_range` to your specific IP/network
- Disable unnecessary services (FreqUI in production)
- Use strong SSH keys (4096-bit RSA recommended)

### 3. **Instance Security**
- Regular system updates via cloud-init
- UFW firewall automatically configured
- Non-root user (freqtrade) for application

## 🚨 Operational Considerations

### 1. **State Management**
- Terraform state contains sensitive information
- Consider using remote state (OVH Object Storage, AWS S3)
- Regular state backups recommended

### 2. **Disaster Recovery**
- Infrastructure can be recreated from Terraform config
- Application data should be backed up separately
- Document recovery procedures

### 3. **Monitoring**
- OVH provides basic monitoring
- Consider external monitoring for production
- Set up alerts for critical metrics

## 🔄 Lifecycle Management

### 1. **Updates**
```bash
# Update infrastructure
terraform plan  # Review changes
terraform apply # Apply updates

# Update application
make deploy-terraform
```

### 2. **Scaling**
```hcl
# Edit terraform.tfvars
instance_flavor = "s1-4"  # Upgrade to larger instance

# Apply changes
terraform apply
```

### 3. **Cleanup**
```bash
# Destroy infrastructure
terraform destroy

# Or use the deployment script
cd terraform && ./deploy.sh destroy
```

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify OVH API keys in terraform.tfvars
   - Check project ID and permissions
   - Ensure tokens haven't expired

2. **SSH Connection Failures**
   - Verify SSH key path in terraform.tfvars
   - Check security group rules
   - Confirm floating IP assignment

3. **Resource Quotas**
   - Check OVH project quotas
   - Verify available regions
   - Contact OVH support for limit increases

### Debug Commands
```bash
# Enable Terraform debug logging
export TF_LOG=DEBUG
terraform apply

# Check instance console (OVH panel)
# Monitor cloud-init progress
sudo cloud-init status --long

# View system logs
sudo journalctl -xe
```

## 📚 Additional Resources

- [OVH Public Cloud Documentation](https://docs.ovh.com/gb/en/public-cloud/)
- [Terraform OVH Provider](https://registry.terraform.io/providers/ovh/ovh/)
- [OVH API Console](https://api.ovh.com/console/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

## 🎯 Future Enhancements

Potential improvements for the Terraform infrastructure:

1. **Multi-Environment Support**
   - Separate configurations for dev/staging/prod
   - Environment-specific variable files
   - Terraform workspaces

2. **Remote State Management**
   - Store state in OVH Object Storage
   - State locking for team collaboration
   - Encrypted state storage

3. **Advanced Monitoring**
   - Integration with OVH monitoring services
   - Custom dashboards and alerts
   - Log aggregation and analysis

4. **High Availability**
   - Multi-region deployment
   - Load balancing
   - Automated failover

5. **Backup Automation**
   - Automated volume snapshots
   - Application data backups
   - Disaster recovery testing

---

*This Terraform implementation provides a solid foundation for deploying the AI Trading Bot on OVH Cloud with infrastructure as code best practices.*