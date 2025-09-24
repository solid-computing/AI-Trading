# Terraform Infrastructure for AI Trading Bot on OVH Cloud

This directory contains Terraform configuration files to provision infrastructure for the AI Trading Bot on OVH Public Cloud.

## Prerequisites

1. **OVH Account**: You need an OVH account with Public Cloud service enabled
2. **OVH API Keys**: Create API keys at https://api.ovh.com/createToken/
3. **Terraform**: Install Terraform >= 1.0 
4. **SSH Key**: Generate an SSH key pair for server access

## Quick Start

### 1. Install Terraform

```bash
# Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# macOS
brew install terraform

# Or download from https://www.terraform.io/downloads
```

### 2. Set up OVH API Keys

1. Go to https://api.ovh.com/createToken/
2. Fill in the form:
   - **Application name**: AI Trading Bot
   - **Application description**: Terraform infrastructure management
   - **Validity**: Unlimited (or as needed)
   - **Rights**: 
     - `GET /cloud/*`
     - `POST /cloud/*`
     - `PUT /cloud/*`
     - `DELETE /cloud/*`
3. Note down the generated keys: Application Key, Application Secret, Consumer Key

### 3. Configure Variables

```bash
# Copy the example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars
```

Required variables:
- `ovh_application_key`: Your OVH API application key
- `ovh_application_secret`: Your OVH API application secret  
- `ovh_consumer_key`: Your OVH API consumer key
- `ovh_project_id`: Your OVH Public Cloud project ID
- `openstack_username`: Your OVH username
- `openstack_password`: Your OVH password

### 4. Generate SSH Key (if needed)

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "ai-trading-bot"

# Update terraform.tfvars with the public key path
ssh_public_key_path = "~/.ssh/id_rsa.pub"
```

### 5. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

### 6. Get Connection Details

After deployment, Terraform will output connection details:

```bash
# Get outputs
terraform output

# Connect to your VPS
ssh freqtrade@<public_ip>
```

## Configuration Options

### Instance Types

| Flavor | vCPU | RAM | Storage | Monthly Cost* |
|--------|------|-----|---------|---------------|
| s1-2   | 1    | 2GB | 10GB    | ~€3-5         |
| s1-4   | 1    | 4GB | 20GB    | ~€6-8         |
| s1-8   | 2    | 8GB | 40GB    | ~€12-15       |
| b2-7   | 2    | 7GB | 50GB    | ~€10-12       |
| b2-15  | 4    | 15GB| 100GB   | ~€20-25       |

*Approximate costs, check OVH pricing for exact rates

### Security Configuration

```hcl
# Restrict access to your IP only
allowed_ip_range = "1.2.3.4/32"

# Enable FreqUI for development
enable_freqtrade_ui = true

# For production, keep these false
enable_http_access  = false
enable_https_access = false
```

### Storage Options

```hcl
# Enable additional data volume
create_data_volume = true
data_volume_size   = 20  # GB
```

## File Structure

```
terraform/
├── main.tf                 # Main infrastructure configuration 
├── variables.tf            # Variable definitions
├── outputs.tf              # Output definitions
├── cloud-init.yml          # Cloud-init user data script
├── terraform.tfvars.example # Example variables file
├── README.md              # This file
└── .terraform/            # Terraform state (created after init)
```

## Management Commands

```bash
# Show current state
terraform show

# List resources
terraform state list

# Get specific output
terraform output public_ip

# Destroy infrastructure
terraform destroy

# Format code
terraform fmt

# Validate configuration
terraform validate
```

## Integration with Existing Deployment

After creating infrastructure with Terraform:

1. **Get connection details**:
   ```bash
   terraform output deployment_vars
   ```

2. **Update your CI/CD**:
   - Set `OVH_HOST` to the output public IP
   - Set `OVH_USER` to `freqtrade`

3. **Deploy using existing scripts**:
   ```bash
   export OVH_HOST=$(terraform output -raw public_ip)
   export OVH_USER=freqtrade
   make deploy
   ```

## Cost Optimization

- Use `s1-2` flavor for small-scale trading ($3-5/month)
- Disable monitoring and backups initially
- Use `terraform destroy` when not trading to save costs
- Monitor your OVH billing dashboard

## Troubleshooting

### Common Issues

1. **Authentication errors**: Check your API keys and project ID
2. **Quota exceeded**: Check your OVH project quotas  
3. **SSH connection fails**: Verify security group rules and SSH key
4. **Instance won't start**: Check cloud-init logs on OVH console

### Debug Commands

```bash
# Check Terraform logs
export TF_LOG=DEBUG
terraform apply

# SSH debug
ssh -v freqtrade@<ip>

# Check instance console (OVH control panel)
# Manager > Public Cloud > Instances > [your-instance] > Console
```

### Getting Help

- Check cloud-init logs: `sudo cloud-init status --long`
- View system logs: `sudo journalctl -xe`
- OVH API documentation: https://docs.ovh.com/
- Terraform OVH provider: https://registry.terraform.io/providers/ovh/ovh/

## Security Best Practices

1. **Restrict IP access**: Set `allowed_ip_range` to your specific IP/network
2. **Use strong SSH keys**: Generate 4096-bit RSA keys
3. **Keep secrets secure**: Never commit `terraform.tfvars` to git
4. **Regular updates**: Keep Terraform and providers updated
5. **Monitor access**: Check OVH logs regularly

## Next Steps

After infrastructure is deployed:

1. Configure your trading bot environment variables
2. Deploy application using existing CI/CD pipeline  
3. Set up monitoring and alerting
4. Configure backups for important data
5. Test disaster recovery procedures

For detailed application setup, see the main [SETUP.md](../SETUP.md) guide.