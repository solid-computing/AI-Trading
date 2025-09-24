#!/usr/bin/env python3
"""
Validation script to check the complete Freqtrade setup.
This script validates all configuration files, strategies, and deployment files.
"""

import json
import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {filepath}")
        return True
    else:
        status = "❌" if required else "⚠️"
        print(f"{status} {filepath} {'(required)' if required else '(optional)'}")
        return not required

def validate_json_file(filepath):
    """Validate JSON file syntax"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"✅ {filepath} - Valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {filepath} - Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {filepath} - File not found")
        return False

def validate_python_syntax(filepath):
    """Validate Python file syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ {filepath} - Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"❌ {filepath} - Syntax error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {filepath} - File not found")
        return False

def validate_docker_files():
    """Validate Docker-related files"""
    print("\n🐳 Docker Files:")
    files = [
        ("Dockerfile", True),
        ("docker-compose.yml", True),
        ("docker-compose.prod.yml", True),
        (".dockerignore", False),
    ]
    
    all_good = True
    for filepath, required in files:
        if not check_file_exists(filepath, required):
            all_good = False
    
    return all_good

def validate_config_files():
    """Validate configuration files"""
    print("\n⚙️ Configuration Files:")
    
    config_files = [
        "config.dryrun.json",
        "config.live.template.json", 
        "pairs.json"
    ]
    
    all_good = True
    for config_file in config_files:
        if not validate_json_file(config_file):
            all_good = False
    
    return all_good

def validate_strategies():
    """Validate strategy files"""
    print("\n📊 Strategy Files:")
    
    strategy_files = [
        "user_data/strategies/RsiMaStrategy.py",
        "user_data/strategies/AIEnhancedRsiMaStrategy.py"
    ]
    
    all_good = True
    for strategy_file in strategy_files:
        if not validate_python_syntax(strategy_file):
            all_good = False
    
    return all_good

def validate_ai_components():
    """Validate AI engine components"""
    print("\n🧠 AI Engine Components:")
    
    ai_files = [
        "user_data/ai_engine/__init__.py",
        "user_data/ai_engine/market_analyzer.py",
        "user_data/ai_engine/sentiment_engine.py", 
        "user_data/ai_engine/risk_manager.py",
        "user_data/ai_engine/decision_engine.py"
    ]
    
    all_good = True
    for ai_file in ai_files:
        if not validate_python_syntax(ai_file):
            all_good = False
    
    # Validate AI config
    if os.path.exists("user_data/ai_config.json"):
        if not validate_json_file("user_data/ai_config.json"):
            all_good = False
    else:
        print("⚠️ user_data/ai_config.json (optional)")
    
    return all_good

def validate_deployment_files():
    """Validate deployment files"""
    print("\n🚀 Deployment Files:") 
    
    deployment_files = [
        ("deployment/deploy.sh", True),
        ("deployment/deploy-terraform.sh", True),
        ("deployment/setup-vps.sh", True),
        ("deployment/freqtrade.service", True),
    ]
    
    all_good = True
    for filepath, required in deployment_files:
        if not check_file_exists(filepath, required):
            all_good = False
        elif filepath.endswith('.sh'):
            # Check if shell script is executable
            if os.access(filepath, os.X_OK):
                print(f"  ✅ {filepath} is executable")
            else:
                print(f"  ⚠️ {filepath} is not executable (run: chmod +x {filepath})")
    
    return all_good

def validate_ci_cd():
    """Validate CI/CD files"""
    print("\n🔄 CI/CD Files:")
    
    files = [
        (".circleci/config.yml", True),
    ]
    
    all_good = True
    for filepath, required in files:
        if not check_file_exists(filepath, required):
            all_good = False
    
    return all_good

def validate_documentation():
    """Validate documentation files"""
    print("\n📚 Documentation Files:")
    
    files = [
        ("readme.md", True),
        ("requirements.txt", True),
        (".gitignore", True),
        ("TERRAFORM.md", True),
    ]
    
    all_good = True
    for filepath, required in files:
        if not check_file_exists(filepath, required):
            all_good = False
    
    return all_good

def validate_terraform():
    """Validate Terraform infrastructure files"""
    print("\n🏗️ Terraform Infrastructure:")
    
    terraform_files = [
        ("terraform/main.tf", True),
        ("terraform/variables.tf", True),
        ("terraform/outputs.tf", True),
        ("terraform/cloud-init.yml", True),
        ("terraform/terraform.tfvars.example", True),
        ("terraform/deploy.sh", True),
        ("terraform/quick-start.sh", True),
        ("terraform/README.md", True),
    ]
    
    all_good = True
    for filepath, required in terraform_files:
        if not check_file_exists(filepath, required):
            all_good = False
        elif filepath.endswith('.sh'):
            # Check if shell script is executable
            if os.access(filepath, os.X_OK):
                print(f"  ✅ {filepath} is executable")
            else:
                print(f"  ⚠️ {filepath} is not executable (run: chmod +x {filepath})")
    
    # Check if terraform directory exists
    if os.path.isdir("terraform"):
        print("  ✅ terraform/ directory exists")
        
        # Check for terraform.tfvars (should not exist in repo)
        if os.path.exists("terraform/terraform.tfvars"):
            print("  ⚠️ terraform/terraform.tfvars exists (should be in .gitignore)")
        else:
            print("  ✅ terraform.tfvars not in repository (good)")
    else:
        print("  ❌ terraform/ directory missing")
        all_good = False
    
    return all_good

def validate_structure():
    """Validate directory structure"""
    print("\n📁 Directory Structure:")
    
    required_dirs = [
        "user_data",
        "user_data/strategies",
        "user_data/ai_engine",
        "deployment",
        "scripts",
        ".circleci",
        "terraform"
    ]
    
    all_good = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ (missing)")
            all_good = False
    
    return all_good

def main():
    """Main validation function"""
    print("🤖 Freqtrade Trading Bot Setup Validation")
    print("=" * 50)
    
    # Run all validations
    validations = [
        validate_structure(),
        validate_docker_files(),
        validate_config_files(),
        validate_strategies(),
        validate_ai_components(),
        validate_deployment_files(),
        validate_ci_cd(),
        validate_documentation(),
        validate_terraform(),
    ]
    
    # Summary
    print("\n" + "=" * 50)
    if all(validations):
        print("🎉 All validations passed! Your Freqtrade setup is ready.")
        print("\nNext steps:")
        print("1. Set up your API keys in CircleCI Context 'freqtrade-secrets'")
        print("2. Test locally with: docker-compose up -d")
        print("3. Check logs with: docker-compose logs -f freqtrade")
        print("4. Deploy infrastructure: make terraform-deploy")
        print("5. Deploy application: make deploy-terraform")
        return 0
    else:
        print("❌ Some validations failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())