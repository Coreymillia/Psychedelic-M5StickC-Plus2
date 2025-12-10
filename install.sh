#!/bin/bash
# Installation script for Waveshare LCD HAT Screensaver System

echo "🖥️ Waveshare LCD HAT Screensaver System Installation"
echo "===================================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    echo "   The system may not work correctly on other platforms"
    read -p "Continue anyway? (y/N): " continue_install
    if [[ ! "$continue_install" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 1
    fi
fi

echo "🔍 Checking dependencies..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.7"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)"; then
    echo "❌ Python 3.7+ required. Found: Python $python_version"
    echo "   Please upgrade Python and try again"
    exit 1
fi

echo "✅ Python $python_version found"

# Install system dependencies
echo "📦 Installing system dependencies..."

# Update package list
sudo apt update

# Install required packages
packages=(
    "python3-pip"
    "python3-pil" 
    "python3-gpiozero"
    "python3-spidev"
    "python3-numpy"
    "git"
)

for package in "${packages[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package "; then
        echo "   Installing $package..."
        sudo apt install -y "$package"
    else
        echo "   ✅ $package already installed"
    fi
done

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --user
else
    # Fallback if requirements.txt missing
    pip3 install --user pillow gpiozero spidev numpy
fi

# Enable SPI
echo "🔧 Configuring system settings..."

if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "   Enabling SPI interface..."
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    spi_enabled=true
fi

# Configure GPIO pins for LCD HAT
if ! grep -q "gpio=6,19,5,26,13,21,20,16=pu" /boot/config.txt; then
    echo "   Configuring GPIO pins for LCD HAT..."
    echo "gpio=6,19,5,26,13,21,20,16=pu" | sudo tee -a /boot/config.txt
    gpio_configured=true
fi

# Make scripts executable
echo "🔧 Setting up executables..."
chmod +x saver
chmod +x *.py
chmod +x *.sh

# Create symbolic link for easy access (optional)
if [ ! -f "/usr/local/bin/saver" ]; then
    echo "   Creating system-wide launcher..."
    sudo ln -s "$(pwd)/saver" /usr/local/bin/saver 2>/dev/null || true
fi

# Test basic functionality
echo "🧪 Running basic system test..."
python3 test_system.py

# Check LCD HAT detection
echo "🔌 Checking LCD HAT connection..."
if [ -c "/dev/spidev0.0" ]; then
    echo "   ✅ SPI interface detected"
else
    echo "   ⚠️  SPI interface not found - LCD HAT may not work"
fi

# Installation complete
echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "📋 What was installed:"
echo "   • System dependencies (gpiozero, PIL, etc.)"
echo "   • Python requirements"
echo "   • SPI interface enabled"
echo "   • GPIO pins configured for LCD HAT"
echo "   • All scripts made executable"
echo ""

if [ "$spi_enabled" = true ] || [ "$gpio_configured" = true ]; then
    echo "⚠️  REBOOT REQUIRED"
    echo "   System settings were changed. Please reboot before using:"
    echo "   sudo reboot"
    echo ""
fi

echo "🚀 Quick Start:"
echo "   ./saver                    # Launch main menu"
echo "   ./saver 1                  # Test fixed matrix rain"
echo "   ./saver 51                 # Boot manager (recommended)"
echo "   ./saver 80                 # Test button controls"
echo ""
echo "📚 Documentation:"
echo "   README.md                  # Main documentation"
echo "   docs/QUICK_START.md       # Getting started guide"
echo "   docs/BUTTON_CONTROLS.md   # Physical button usage"
echo ""
echo "🛠️  Troubleshooting:"
echo "   ./saver 94                 # Fix GPIO conflicts"
echo "   python3 test_system.py    # Run system tests"
echo ""

if [ -f "/usr/local/bin/saver" ]; then
    echo "💡 System-wide access enabled:"
    echo "   You can now run 'saver' from anywhere in the terminal"
    echo ""
fi

echo "✅ Ready to use! Connect your Waveshare 1.44\" LCD HAT and run './saver'"