#!/usr/bin/env python3
"""
Quick Launch - Start screensavers directly without menu conflicts
Usage: python3 quick_launch.py [screensaver_number]
"""

import sys
import os
import subprocess
import time

# Screensaver mapping
SCREENSAVERS = {
    1: 'glyph_rain1_fixed.py',
    2: 'glyph_rain1.py',
    3: 'glyph_rain2.py',
    4: 'glyph_rain3.py',
    5: 'matrix_binary.py',
    6: 'neon_rain.py',
    7: 'glyph_rain4_timer.py',
    8: 'glyph_rain5_slow.py',
    9: 'raindrops.py',
    10: 'heavy_rain.py',
    11: 'micro_dots.py',
    12: 'micro_dots_dripping.py',
    13: 'simple_flames.py',
    14: 'campfire.py',
    15: 'retro_geometry.py',
    16: 'plasma_field.py',
    17: 'bouncing_balls.py',
    18: 'kaleidoscope.py',
    19: 'mandelbrot.py',
    20: 'julia_set.py',
    21: 'sierpinski.py',
    22: 'dragon_curve.py'
}

def quick_cleanup():
    """Quick targeted cleanup"""
    print("🔧 Quick cleanup...")
    
    # Stop services only
    services = ['lcd-stable.service', 'lcd-glyph-locked.service']
    for service in services:
        subprocess.run(['sudo', 'systemctl', 'stop', service], 
                      capture_output=True)
    
    # Kill specific processes by name (not pattern matching)
    specific_processes = [
        'glyph_rain1_fixed.py', 'glyph_rain1.py', 'glyph_rain2.py',
        'micro_dots.py', 'simple_flames.py', 'plasma_field.py'
    ]
    
    for proc in specific_processes:
        subprocess.run(['pkill', '-f', proc], capture_output=True)
    
    time.sleep(1)
    print("✅ Ready")

def launch_screensaver(num):
    """Launch screensaver by number"""
    if num not in SCREENSAVERS:
        print(f"❌ Invalid screensaver number: {num}")
        print("Available: 1-22")
        return False
    
    filepath = SCREENSAVERS[num]
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    quick_cleanup()
    
    print(f"🚀 Starting screensaver #{num}: {filepath}")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run(['python3', filepath])
        return True
    except KeyboardInterrupt:
        print("\n✅ Screensaver stopped")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("🚀 Quick Launch - Start screensavers directly")
        print("Usage: python3 quick_launch.py [1-22]")
        print()
        print("Examples:")
        print("  python3 quick_launch.py 1    # Fixed matrix rain")
        print("  python3 quick_launch.py 11   # Micro dots")
        print("  python3 quick_launch.py 16   # Plasma field")
        return
    
    try:
        num = int(sys.argv[1])
        launch_screensaver(num)
    except ValueError:
        print("❌ Please enter a valid number (1-22)")

if __name__ == "__main__":
    main()