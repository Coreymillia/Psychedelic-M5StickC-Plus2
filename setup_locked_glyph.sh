#!/bin/bash
# Setup script to run only the fixed glyph rain screensaver
# This locks the system to use the stable glyph rain variant

echo "🔒 Waveshare LCD - Lock to Fixed Glyph Rain Setup"
echo "================================================"
echo ""
echo "This will replace the random screensaver with a stable, memory-leak-free"
echo "glyph rain that runs continuously without freezing."
echo ""
echo "What would you like to do?"
echo ""
echo "1) Enable locked glyph rain screensaver (replaces random)"
echo "2) Test the fixed glyph rain for 60 seconds"
echo "3) Revert to random screensaver system"
echo "4) Check current status"
echo "5) Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Setting up locked glyph rain screensaver..."
        
        # Get current directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        # Stop existing service
        sudo systemctl stop lcd-screensaver.service 2>/dev/null
        
        # Create new systemd service for locked glyph rain
        sudo tee /etc/systemd/system/lcd-glyph-locked.service > /dev/null <<EOF
[Unit]
Description=Waveshare LCD Locked Glyph Rain (Memory-Safe)
After=multi-user.target

[Service]
Type=simple
User=$(whoami)
Group=$(whoami)
WorkingDirectory=${SCRIPT_DIR}
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/glyph_rain1_fixed.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits to prevent system issues
MemoryMax=200M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
EOF

        # Disable old service and enable new one
        sudo systemctl disable lcd-screensaver.service 2>/dev/null
        sudo systemctl daemon-reload
        sudo systemctl enable lcd-glyph-locked.service
        sudo systemctl start lcd-glyph-locked.service
        
        echo "✅ Fixed glyph rain screensaver is now running!"
        echo "   This version includes:"
        echo "   - Memory leak protection"
        echo "   - Automatic resource cleanup"
        echo "   - Restart protection"
        echo "   - CPU and memory limits"
        echo ""
        echo "   Use 'sudo systemctl status lcd-glyph-locked' to check status"
        ;;
        
    2)
        echo "Testing fixed glyph rain for 60 seconds..."
        
        # Get current directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        echo "Starting test... (will auto-stop after 60 seconds)"
        timeout 60s python3 "${SCRIPT_DIR}/glyph_rain1_fixed.py" || true
        
        echo ""
        echo "✅ 60-second test completed!"
        echo "   Did it run smoothly without freezing? If so, option 1 will work great."
        ;;
        
    3)
        echo "Reverting to original random screensaver system..."
        
        # Stop locked service
        sudo systemctl stop lcd-glyph-locked.service 2>/dev/null
        sudo systemctl disable lcd-glyph-locked.service 2>/dev/null
        sudo rm -f /etc/systemd/system/lcd-glyph-locked.service
        sudo systemctl daemon-reload
        
        # Re-enable original service
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        sudo tee /etc/systemd/system/lcd-screensaver.service > /dev/null <<EOF
[Unit]
Description=Waveshare LCD Random Screensaver
After=multi-user.target

[Service]
Type=simple
User=$(whoami)
Group=$(whoami)
WorkingDirectory=${SCRIPT_DIR}
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/screensaver_launcher.py random
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl daemon-reload
        sudo systemctl enable lcd-screensaver.service
        sudo systemctl start lcd-screensaver.service
        
        echo "✅ Reverted to original random screensaver system!"
        ;;
        
    4)
        echo "Current Status:"
        echo "==============="
        
        # Check locked service
        echo "Locked Glyph Rain Service:"
        if systemctl is-enabled lcd-glyph-locked.service 2>/dev/null | grep -q "enabled"; then
            echo "  ✅ Fixed glyph rain: ENABLED"
            echo "     Status: $(systemctl is-active lcd-glyph-locked.service 2>/dev/null)"
        else
            echo "  ❌ Fixed glyph rain: DISABLED"
        fi
        
        # Check original service
        echo ""
        echo "Original Random Service:"
        if systemctl is-enabled lcd-screensaver.service 2>/dev/null | grep -q "enabled"; then
            echo "  ✅ Random screensaver: ENABLED"
            echo "     Status: $(systemctl is-active lcd-screensaver.service 2>/dev/null)"
        else
            echo "  ❌ Random screensaver: DISABLED"
        fi
        
        # Check running processes
        echo ""
        echo "Currently Running:"
        if pgrep -f "glyph_rain1_fixed.py" > /dev/null; then
            echo "  🟢 Fixed Glyph Rain is running"
        elif pgrep -f "screensaver_launcher.py" > /dev/null; then
            echo "  🟢 Random screensaver launcher is running"
        elif pgrep -f "python3.*\.py" > /dev/null; then
            echo "  🟡 Some Python screensaver is running:"
            ps aux | grep "python3.*\.py" | grep -v grep | head -3
        else
            echo "  ⚫ No screensaver currently running"
        fi
        ;;
        
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "Setup complete! 🎉"
echo ""
echo "Quick commands:"
echo "  python3 glyph_rain1_fixed.py                # Test fixed glyph rain manually"
echo "  sudo systemctl status lcd-glyph-locked      # Check locked service status"
echo "  sudo systemctl restart lcd-glyph-locked     # Restart if needed"
echo "  ./setup_locked_glyph.sh                     # Run this setup again"
echo ""