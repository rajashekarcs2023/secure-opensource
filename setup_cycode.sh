#!/bin/bash

echo "🔧 Cycode Setup Script"
echo "======================"

# Add Cycode to PATH
export PATH="/Users/radhikadanda/Library/Python/3.12/bin:$PATH"

echo ""
echo "✅ Cycode added to PATH"
echo ""

# Check if cycode is accessible
if command -v cycode &> /dev/null; then
    echo "✅ Cycode command found"
    
    # Check version
    echo ""
    echo "📦 Cycode Version:"
    cycode --version
    
    echo ""
    echo "🔄 Starting Cycode authentication..."
    echo ""
    echo "A browser window will open. Please:"
    echo "  1. Sign up or log in to Cycode"
    echo "  2. Click 'Allow' to authorize the CLI"
    echo ""
    read -p "Press Enter to start authentication..."
    
    # Run cycode auth
    cycode auth
    
    echo ""
    echo "🔄 Checking authentication status..."
    cycode status
    
    echo ""
    echo "✅ Cycode setup complete!"
    echo ""
    echo "Test it with: python3 test_3_cycode.py"
else
    echo "❌ Cycode command not found"
    echo ""
    echo "Try running manually:"
    echo "  export PATH=\"/Users/radhikadanda/Library/Python/3.12/bin:\$PATH\""
    echo "  cycode auth"
fi
