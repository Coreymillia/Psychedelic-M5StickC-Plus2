# Installation Guide - Waveshare 1.44" LCD HAT Screensavers

This guide will help you install and set up the screensaver collection on your Raspberry Pi.

## Prerequisites

### Hardware
- Raspberry Pi (any model with GPIO pins)
- Waveshare 1.44" LCD HAT (128×128, ST7735S controller)
- MicroSD card with Raspberry Pi OS

### Software  
- Raspberry Pi OS (Lite or Desktop)
- Python 3 (usually pre-installed)
- Internet connection for downloading dependencies

## Step-by-Step Installation

### 1. Update Your System
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Enable SPI Interface
The LCD HAT requires SPI to be enabled:

**Method 1: Using raspi-config**
```bash
sudo raspi-config
```
- Navigate to: `Interface Options`
- Select: `SPI`
- Choose: `Yes` to enable
- Reboot when prompted

**Method 2: Manual configuration**
```bash
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
sudo reboot
```

### 3. Install Python Dependencies
```bash
# Install system packages
sudo apt install python3-pip python3-numpy python3-pil -y

# Install Python packages
pip3 install RPi.GPIO spidev gpiozero

# Alternative for system-wide installation:
# sudo apt install python3-rpi.gpio python3-spidev python3-gpiozero
```

### 4. Download the Screensaver Package
```bash
# Clone from GitHub (replace with actual repo URL)
git clone https://github.com/yourusername/waveshare-screensavers.git
cd waveshare-screensavers

# Or download and extract ZIP
# wget https://github.com/yourusername/waveshare-screensavers/archive/main.zip
# unzip main.zip
# cd waveshare-screensavers-main
```

### 5. Test the Installation
```bash
# Make the setup script executable
chmod +x setup.sh

# Test that drivers work
python3 -c "import config; print('✅ Config loaded successfully')"
python3 -c "import LCD_1in44; print('✅ LCD driver loaded successfully')"

# Test a screensaver
python3 screensaver_launcher.py random
```

If you see the LCD light up with a screensaver, installation is successful!

### 6. Configure Auto-Start (Optional)
```bash
# Run the setup script
./setup.sh

# Choose option 1 for boot-time screensaver
# or option 2 for periodic screensavers
```

## Verification Steps

### Check SPI is Working
```bash
# SPI should be listed
lsmod | grep spi

# SPI devices should exist
ls -l /dev/spi*
```

### Check GPIO Permissions
```bash
# Your user should be in gpio and spi groups
groups

# If not, add yourself:
sudo usermod -a -G gpio,spi $USER
# Then log out and back in
```

### Test Hardware Connection
```bash
# Basic GPIO test
python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
print('✅ GPIO test passed')
GPIO.cleanup()
"
```

## Troubleshooting

### Issue: "No module named 'config'"
**Solution**: Make sure you're running from the correct directory and all files are present:
```bash
ls -la config.py LCD_1in44.py LCD_Config.py
```

### Issue: "Permission denied" accessing GPIO/SPI
**Solution**: Add user to required groups:
```bash
sudo usermod -a -G gpio,spi,i2c $USER
sudo reboot
```

### Issue: LCD stays blank
**Solutions**:
1. Check HAT is properly seated on GPIO pins
2. Verify you have the correct Waveshare 1.44" LCD HAT model
3. Check SPI is enabled: `sudo raspi-config`
4. Test with original Waveshare demo code

### Issue: "Cannot determine SOC peripheral base address" 
**Solution**: This often happens on newer Pi models. The package includes updated drivers that should resolve this.

### Issue: Service won't start automatically
**Solutions**:
```bash
# Check service status
sudo systemctl status lcd-screensaver.service

# Check logs
sudo journalctl -u lcd-screensaver.service -f

# Manually restart service
sudo systemctl restart lcd-screensaver.service
```

## Manual Service Configuration

If the automated setup doesn't work, you can manually create the service:

```bash
# Create service file
sudo nano /etc/systemd/system/lcd-screensaver.service
```

Add this content (adjust paths as needed):
```ini
[Unit]
Description=Waveshare LCD Random Screensaver
After=multi-user.target network.target dev-gpiomem.device
Wants=dev-gpiomem.device

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/waveshare-screensavers
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/python3 /home/pi/waveshare-screensavers/screensaver_launcher.py random
Restart=on-failure
RestartSec=10
Environment="DISPLAY=:0"
Environment="XDG_RUNTIME_DIR=/run/user/1000"

[Install]
WantedBy=multi-user.target
```

Then enable it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lcd-screensaver.service
sudo systemctl start lcd-screensaver.service
```

## Next Steps

Once installed successfully:
1. Explore different screensavers: `python3 screensaver_launcher.py list`
2. Customize timing in individual screensaver files
3. Create your own screensaver by copying and modifying existing ones
4. Set up different screensavers for different times of day

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Verify your hardware connections
3. Test with original Waveshare examples
4. Check Raspberry Pi forums for GPIO/SPI issues
5. Open an issue on the project GitHub page

## Success Indicators

You know everything is working when:
- ✅ `python3 screensaver_launcher.py random` shows colorful animations
- ✅ LCD backlight turns on/off properly  
- ✅ No error messages about GPIO or SPI
- ✅ Service starts automatically after reboot (if configured)