# 🔧 Cycode Setup Guide

Cycode is now installed! Let's authenticate it.

## Step 1: Add Cycode to PATH (Temporary Fix)

Run this in your terminal:

```bash
export PATH="/Users/radhikadanda/Library/Python/3.12/bin:$PATH"
```

## Step 2: Authenticate with Cycode

Now run:

```bash
cycode auth
```

### What will happen:
1. ✅ A browser window will open
2. ✅ You'll see Cycode login page
3. ✅ Sign up for free account (or log in if you have one)
4. ✅ Click "Allow" to authorize the CLI
5. ✅ Terminal will show: "Successfully logged into cycode"

**This takes ~2 minutes**

---

## Step 3: Verify It Works

After authentication, run:

```bash
cycode status
```

Expected output:
```
✅ Cycode CLI version: X.X.X
✅ Authenticated as: your-email@domain.com
```

---

## Alternative: Manual Configuration (If Auth Fails)

If the browser auth doesn't work, you can configure manually:

### A. Get Credentials from Cycode Dashboard
1. Go to: https://app.cycode.com/
2. Sign up/log in
3. Go to Settings → API Keys
4. Generate a new API key pair
5. Copy the Client ID and Client Secret

### B. Configure CLI
```bash
cycode configure
```

When prompted:
- **Cycode API URL**: Press Enter (use default)
- **Cycode APP URL**: Press Enter (use default)  
- **Cycode Client ID**: Paste your Client ID
- **Cycode Client Secret**: Paste your Client Secret

---

## ✅ Testing Cycode

Once authenticated, test it:

```bash
python3 test_3_cycode.py
```

Expected:
```
✅ Cycode installed
✅ Cycode authenticated
✅ MCP server available
✅ Available scans: Secrets, SCA, SAST, IaC
```

---

## 🎯 Quick Commands

```bash
# Export PATH (run this first)
export PATH="/Users/radhikadanda/Library/Python/3.12/bin:$PATH"

# Authenticate
cycode auth

# Check status
cycode status

# Test scanning
cycode scan path .

# Start MCP server (for the agent)
cycode mcp
```

---

## 💡 Pro Tip: Make PATH Permanent

Add this to your `~/.zshrc` file:

```bash
echo 'export PATH="/Users/radhikadanda/Library/Python/3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Now `cycode` will work in all terminals!

---

## 🆘 If You Get Stuck

**Error: "command not found: cycode"**
- Run: `export PATH="/Users/radhikadanda/Library/Python/3.12/bin:$PATH"`

**Error: "Not authenticated"**
- Run: `cycode auth` again
- Or use: `cycode configure` for manual setup

**Browser doesn't open**
- Try: `cycode configure` (manual method)
- Get keys from: https://app.cycode.com/

---

## ✅ You're Ready When...

You can run these without errors:
```bash
cycode --version
cycode status
```

Then proceed to test the other MCPs!
