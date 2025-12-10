#!/usr/bin/env python3
"""
Background Launcher - Run screensavers in background (survive terminal closing)
"""

import subprocess
import sys
import os

def run_in_background(screensaver_num):
    """Launch screensaver in background using nohup"""
    
    screensavers = {
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
        22: 'dragon_curve.py',
        80: 'simple_button_switcher.py',
        81: 'button_screensaver.py'
    }
    
    if screensaver_num not in screensavers:
        print(f"❌ Invalid screensaver number: {screensaver_num}")
        return False
    
    filepath = screensavers[screensaver_num]
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Stop any existing screensavers first
    print("🧹 Stopping existing screensavers...")
    try:
        subprocess.run(['pkill', '-f', 'glyph_rain'], capture_output=True)
        subprocess.run(['pkill', '-f', 'button_switcher'], capture_output=True)
        subprocess.run(['pkill', '-f', 'screensaver'], capture_output=True)
    except:
        pass
    
    # Launch in background with nohup
    print(f"🚀 Starting screensaver #{screensaver_num} in background...")
    print(f"📄 File: {filepath}")
    
    try:
        # Use nohup to detach from terminal
        subprocess.Popen(['nohup', 'python3', filepath], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        preexec_fn=os.setsid)  # Create new process group
        
        print("✅ Screensaver started in background!")
        print("   - Will survive terminal closing")
        print("   - Running independently") 
        print("   - Check your LCD display")
        print()
        print("To stop it later:")
        print(f"   pkill -f {filepath}")
        print("   or")
        print("   ./saver 96  (disable all)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start in background: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("🔄 Background Launcher")
        print("Usage: python3 background_launcher.py [screensaver_number]")
        print()
        print("Examples:")
        print("  python3 background_launcher.py 1    # Fixed matrix rain in background")
        print("  python3 background_launcher.py 80   # Button switcher in background")
        print("  python3 background_launcher.py 11   # Micro dots in background")
        return
    
    try:
        num = int(sys.argv[1])
        run_in_background(num)
    except ValueError:
        print("❌ Please enter a valid number")

if __name__ == "__main__":
    main()