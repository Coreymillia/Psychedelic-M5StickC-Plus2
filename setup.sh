#!/bin/bash
# Setup script for Waveshare LCD Screensavers
# Makes it easy to configure auto-start options

echo "🖥️  Waveshare 1.44\" LCD HAT Screensavers Setup"
echo "=============================================="
echo ""
echo "What would you like to do?"
echo ""
echo "1) Run random screensaver on boot (starts once at boot)"
echo "2) Run random screensaver every 15 minutes"
echo "3) Disable all auto-start"
echo "4) Check current status"
echo "5) Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Setting up random screensaver on boot..."
        
        # Get current directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        # Create systemd service
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

        # Enable and start service
        sudo systemctl daemon-reload
        sudo systemctl enable lcd-screensaver.service
        sudo systemctl start lcd-screensaver.service
        
        echo "✅ Random screensaver will now start on boot!"
        echo "   Use 'sudo systemctl status lcd-screensaver' to check status"
        ;;
        
    2)
        echo "Setting up random screensaver every 15 minutes..."
        
        # Get current directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        # Add to crontab
        (crontab -l 2>/dev/null; echo "*/15 * * * * /usr/bin/pkill -f 'python3.*\.py' > /dev/null 2>&1; cd ${SCRIPT_DIR} && /usr/bin/python3 screensaver_launcher.py random > /dev/null 2>&1 &") | crontab -
        
        echo "✅ Random screensaver will change every 15 minutes!"
        echo "   Use 'crontab -l' to see the cron job"
        ;;
        
    3)
        echo "Disabling all auto-start options..."
        
        # Stop and disable systemd service
        sudo systemctl stop lcd-screensaver.service 2>/dev/null
        sudo systemctl disable lcd-screensaver.service 2>/dev/null
        sudo rm -f /etc/systemd/system/lcd-screensaver.service
        sudo systemctl daemon-reload
        
        # Remove from crontab
        crontab -l 2>/dev/null | grep -v "screensaver_launcher.py" | crontab -
        
        # Kill any running screensavers
        pkill -f "python3.*\.py" 2>/dev/null
        
        echo "✅ All auto-start options disabled!"
        echo "   Screensavers stopped and removed from boot/cron"
        ;;
        
    4)
        echo "Current Status:"
        echo "==============="
        
        # Check systemd service
        echo "Boot Service:"
        if systemctl is-enabled lcd-screensaver.service 2>/dev/null | grep -q "enabled"; then
            echo "  ✅ Random screensaver on boot: ENABLED"
            echo "     Status: $(systemctl is-active lcd-screensaver.service 2>/dev/null)"
        else
            echo "  ❌ Random screensaver on boot: DISABLED"
        fi
        
        # Check crontab
        echo ""
        echo "Cron Jobs:"
        if crontab -l 2>/dev/null | grep -q "screensaver_launcher.py"; then
            echo "  ✅ Random screensaver every 15 min: ENABLED"
            echo "     Cron entry: $(crontab -l 2>/dev/null | grep screensaver_launcher.py)"
        else
            echo "  ❌ Random screensaver every 15 min: DISABLED"
        fi
        
        # Check running processes
        echo ""
        echo "Currently Running:"
        if pgrep -f "python3.*\.py" > /dev/null; then
            echo "  🟢 Screensaver is running:"
            ps aux | grep "python3.*\.py" | grep -v grep | head -5
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
echo "  python3 screensaver_launcher.py random    # Run random screensaver now"
echo "  python3 screensaver_launcher.py           # Show interactive menu"
echo "  ./setup.sh                                # Run this setup again"
echo ""