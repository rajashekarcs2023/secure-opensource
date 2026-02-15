#!/usr/bin/env python3
"""
Test 2: GitHub API
Test GitHub token and repository access
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("TEST 2: GITHUB API")
print("=" * 60)

# Check if token exists
token = os.getenv('GITHUB_TOKEN')
if not token:
    print("❌ FAILED: GITHUB_TOKEN not found in .env file")
    print("\nHow to get a GitHub token:")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Select scopes: repo, read:org, write:discussion")
    print("4. Copy token and add to .env as: GITHUB_TOKEN=ghp_xxx")
    exit(1)

print(f"✅ Token found: {token[:10]}...")

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

try:
    # Test 1: Get user info
    print("\n🔄 Testing authentication...")
    response = requests.get('https://api.github.com/user', headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Authenticated as: {user['login']}")
        print(f"   Name: {user.get('name', 'N/A')}")
        print(f"   Public repos: {user['public_repos']}")
    else:
        print(f"❌ Auth failed: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
    
    # Test 2: Check repo access
    print("\n🔄 Testing repository access...")
    response = requests.get('https://api.github.com/user/repos', headers=headers, params={'per_page': 5})
    
    if response.status_code == 200:
        repos = response.json()
        print(f"✅ Can access repositories ({len(repos)} shown)")
        for repo in repos[:3]:
            print(f"   - {repo['full_name']}")
    else:
        print(f"⚠️  Repo access issue: {response.status_code}")
    
    # Test 3: Check rate limit
    print("\n🔄 Checking API rate limit...")
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    
    if response.status_code == 200:
        rate_limit = response.json()
        core = rate_limit['resources']['core']
        print(f"✅ Rate limit: {core['remaining']}/{core['limit']} requests remaining")
        
        if core['remaining'] < 100:
            print(f"⚠️  WARNING: Low rate limit remaining!")
    
    # Test 4: Test PR capabilities (check permissions)
    print("\n🔄 Testing required permissions...")
    scopes = response.headers.get('X-OAuth-Scopes', '')
    print(f"✅ Token scopes: {scopes}")
    
    if 'repo' in scopes:
        print("   ✅ 'repo' scope present - can create PRs")
    else:
        print("   ⚠️  'repo' scope missing - PR creation may fail")
    
    print("\n" + "=" * 60)
    print("🎉 GITHUB API TEST PASSED!")
    print("=" * 60)
    
except requests.exceptions.RequestException as e:
    print(f"\n❌ FAILED: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check internet connection")
    print("2. Verify token is correct")
    print("3. Check token hasn't expired")
    exit(1)
except Exception as e:
    print(f"\n❌ FAILED: {str(e)}")
    exit(1)
