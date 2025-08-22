#!/usr/bin/env python3
"""
GitHub Token Test Script
Tests your GitHub Personal Access Token and displays repository information.
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_github_token():
    """Test GitHub token and display repository information."""
    
    # Get token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN environment variable not found!")
        print("💡 Set it with: export GITHUB_TOKEN=your_token_here")
        return False
    
    # Validate token format
    if not token.startswith(('ghp_', 'github_pat_')):
        print("⚠️  Token format looks unusual. GitHub tokens usually start with 'ghp_' or 'github_pat_'")
    
    print(f"🔍 Testing GitHub token: {token[:8]}...")
    
    # Test basic authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Test 1: Get user information
        print("\n📋 Test 1: User Authentication")
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Authenticated as: {user_data.get('login', 'Unknown')}")
            print(f"   Name: {user_data.get('name', 'Not set')}")
            print(f"   Email: {user_data.get('email', 'Not public')}")
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Error: {response.json().get('message', 'Unknown error')}")
            return False
        
        # Test 2: List repositories
        print("\n📋 Test 2: Repository Access")
        response = requests.get('https://api.github.com/user/repos?per_page=5', headers=headers)
        
        if response.status_code == 200:
            repos = response.json()
            print(f"✅ Can access repositories ({len(repos)} shown):")
            for repo in repos[:3]:
                print(f"   - {repo['full_name']} ({'private' if repo['private'] else 'public'})")
        else:
            print(f"❌ Repository access failed: {response.status_code}")
        
        # Test 3: Check rate limits
        print("\n📋 Test 3: Rate Limits")
        response = requests.get('https://api.github.com/rate_limit', headers=headers)
        
        if response.status_code == 200:
            rate_data = response.json()
            core_limit = rate_data['resources']['core']
            print(f"✅ Rate limit status:")
            print(f"   Limit: {core_limit['limit']} requests/hour")
            print(f"   Remaining: {core_limit['remaining']}")
            print(f"   Reset: {core_limit['reset']}")
        
        # Test 4: Check token scopes
        print("\n📋 Test 4: Token Scopes")
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if 'X-OAuth-Scopes' in response.headers:
            scopes = response.headers['X-OAuth-Scopes'].split(', ')
            print("✅ Token scopes:")
            for scope in scopes:
                if scope:
                    print(f"   - {scope}")
        
        print("\n🎉 GitHub token is working correctly!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def setup_instructions():
    """Display setup instructions."""
    print("\n" + "="*60)
    print("🚀 GITHUB TOKEN SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("1. Create a token at: https://github.com/settings/tokens/new")
    print("2. Set the token in your environment:")
    print("   export GITHUB_TOKEN=your_token_here")
    print("3. Run this script again to test")
    print()
    print("For detailed instructions, see: scripts/github_token_setup.md")
    print("="*60)

def main():
    """Main function."""
    print("🔧 GitHub Token Tester for Agent Factory")
    print("="*50)
    
    if not test_github_token():
        setup_instructions()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
