#!/usr/bin/env python3
"""
Utility script to update Freqtrade configuration files.
This script reads pairs from pairs.json and updates configuration files.
"""

import json
import sys
from pathlib import Path

def load_pairs():
    """Load trading pairs from pairs.json"""
    try:
        with open('pairs.json', 'r') as f:
            data = json.load(f)
            return data['pairs']
    except FileNotFoundError:
        print("Error: pairs.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in pairs.json")
        sys.exit(1)

def update_config_file(config_file, pairs):
    """Update a configuration file with new pairs"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Update pair whitelist
        config['exchange']['pair_whitelist'] = pairs
        
        # Write back to file
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"Updated {config_file} with {len(pairs)} pairs")
        
    except FileNotFoundError:
        print(f"Warning: {config_file} not found, skipping")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {config_file}")

def main():
    """Main function"""
    print("Updating Freqtrade configuration files...")
    
    # Load pairs
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} pairs: {', '.join(pairs)}")
    
    # Update configuration files
    config_files = [
        'config.dryrun.json',
        'config.live.template.json',
    ]
    
    for config_file in config_files:
        update_config_file(config_file, pairs)
    
    print("Configuration update complete!")

if __name__ == "__main__":
    main()