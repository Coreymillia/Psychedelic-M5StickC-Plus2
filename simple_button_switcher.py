#!/usr/bin/env python3
"""
Simple 3-Button Screensaver Switcher for Waveshare 1.44" LCD HAT
Just 3 buttons - super simple controls!

Controls:
- KEY1 (Pin 21): Next screensaver →
- KEY2 (Pin 20): Previous screensaver ←  
- KEY3 (Pin 16): Exit switcher
"""

import time
import subprocess
import os
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44

class SimpleButtonSwitcher:
    def __init__(self):
        print("🕹️ Simple 3-Button Screensaver Switcher")
        print("🔧 Initializing GPIO buttons...")
        
        try:
            # Initialize LCD first
            self.LCD = LCD_1in44.LCD()
            Lcd_ScanDir = LCD_1in44.U2D_L2R
            self.LCD.LCD_Init(Lcd_ScanDir)
            self.LCD.LCD_Clear()
            print("✅ LCD initialized")
            
            # Simple 3-button setup with error handling
            try:
                self.key1 = Button(21, pull_up=True)      # Next →
                print("✅ KEY1 (Pin 21) initialized")
            except Exception as e:
                print(f"❌ KEY1 (Pin 21) failed: {e}")
                self.key1 = None
                
            try:
                self.key2 = Button(20, pull_up=True)      # Previous ←
                print("✅ KEY2 (Pin 20) initialized")
            except Exception as e:
                print(f"❌ KEY2 (Pin 20) failed: {e}")
                self.key2 = None
                
            try:
                self.key3 = Button(16, pull_up=True)      # Exit
                print("✅ KEY3 (Pin 16) initialized")
            except Exception as e:
                print(f"❌ KEY3 (Pin 16) failed: {e}")
                self.key3 = None
            
        except Exception as e:
            print(f"❌ LCD initialization failed: {e}")
            raise
        
        # Curated screensaver list - best ones only
        self.screensavers = [
            'glyph_rain1_fixed.py',    # 1. Stable matrix rain
            'glyph_rain2.py',          # 2. Blue matrix
            'glyph_rain3.py',          # 3. Rainbow matrix
            'neon_rain.py',            # 4. Neon rain
            'simple_flames.py',        # 5. Flames
            'plasma_field.py',         # 6. Plasma
            'bouncing_balls.py',       # 7. Bouncing balls
            'kaleidoscope.py',         # 8. Kaleidoscope
            'micro_dots.py',           # 9. Micro dots
            'raindrops.py'             # 10. Raindrops
        ]
        
        # State
        self.current_index = 0
        self.current_process = None
        self.running = True
        self.last_button_time = 0
        
        # Button handlers with null checks
        if self.key1:
            self.key1.when_pressed = self.next_screensaver
        if self.key2:
            self.key2.when_pressed = self.previous_screensaver
        if self.key3:
            self.key3.when_pressed = self.exit_switcher
        
        print("✅ Simple switcher ready!")
        
        # Show which buttons work
        working_buttons = []
        if self.key1: working_buttons.append("KEY1(Next)")
        if self.key2: working_buttons.append("KEY2(Prev)")  
        if self.key3: working_buttons.append("KEY3(Exit)")
        
        if working_buttons:
            print(f"🎮 Working buttons: {', '.join(working_buttons)}")
        else:
            print("⚠️ No buttons initialized - check GPIO connections")
        
    def debounce_check(self):
        """Prevent button spam"""
        current_time = time.time()
        if current_time - self.last_button_time < 0.5:
            return False
        self.last_button_time = current_time
        return True
    
    def show_status(self):
        """Show current screensaver number on LCD"""
        image = Image.new('RGB', (self.LCD.width, self.LCD.height), (0, 30, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Current screensaver info
        saver_name = self.screensavers[self.current_index].replace('.py', '').replace('_', ' ').title()
        
        # Center the text
        draw.text((10, 30), f"Screensaver #{self.current_index + 1}", 
                 fill=(255, 255, 0), font=font)
        draw.text((10, 50), saver_name[:15], fill=(255, 255, 255), font=font)
        
        # Controls
        draw.text((10, 80), "KEY1: Next →", fill=(100, 255, 100), font=font)
        draw.text((10, 95), "KEY2: ← Prev", fill=(100, 255, 100), font=font)
        draw.text((10, 110), "KEY3: Exit", fill=(255, 100, 100), font=font)
        
        self.LCD.LCD_ShowImage(image, 0, 0)
        time.sleep(1.5)
    
    def start_screensaver(self, index):
        """Start screensaver by index"""
        if index >= len(self.screensavers):
            return False
            
        filepath = self.screensavers[index]
        if not os.path.exists(filepath):
            print(f"❌ Missing: {filepath}")
            return False
        
        # Stop current
        self.stop_current()
        
        # Show status
        self.show_status()
        
        try:
            print(f"🚀 Starting #{index + 1}: {filepath}")
            self.current_process = subprocess.Popen(['python3', filepath])
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def stop_current(self):
        """Stop current screensaver"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=2)
            except:
                try:
                    self.current_process.kill()
                except:
                    pass
            self.current_process = None
        
        # Kill any strays
        try:
            subprocess.run(['pkill', '-f', 'glyph_rain'], capture_output=True)
        except:
            pass
    
    def next_screensaver(self):
        """Next screensaver"""
        if not self.debounce_check():
            return
        
        self.current_index = (self.current_index + 1) % len(self.screensavers)
        print(f"➡️ Next: #{self.current_index + 1}")
        self.start_screensaver(self.current_index)
    
    def previous_screensaver(self):
        """Previous screensaver"""
        if not self.debounce_check():
            return
        
        self.current_index = (self.current_index - 1) % len(self.screensavers)
        print(f"⬅️ Previous: #{self.current_index + 1}")
        self.start_screensaver(self.current_index)
    
    def exit_switcher(self):
        """Exit"""
        if not self.debounce_check():
            return
        
        print("🚪 Exit pressed")
        self.running = False
    
    def run(self):
        """Main loop"""
        print("\n🕹️ SIMPLE BUTTON SWITCHER ACTIVE!")
        print("="*40)
        print("Controls:")
        print("  KEY1 (Button 1): Next screensaver →")
        print("  KEY2 (Button 2): Previous screensaver ←")
        print("  KEY3 (Button 3): Exit switcher")
        print(f"  {len(self.screensavers)} screensavers loaded")
        print("="*40)
        
        # Start first screensaver
        self.start_screensaver(0)
        
        try:
            while self.running:
                time.sleep(0.1)
                
                # Restart if crashed
                if self.current_process and self.current_process.poll() is not None:
                    print("⚠️ Restarting screensaver...")
                    time.sleep(1)
                    self.start_screensaver(self.current_index)
                    
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt")
        
        print("🧹 Cleaning up...")
        self.stop_current()
        
        # Show exit message
        image = Image.new('RGB', (self.LCD.width, self.LCD.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((20, 60), "Switcher OFF", fill=(255, 100, 100), font=font)
        self.LCD.LCD_ShowImage(image, 0, 0)
        time.sleep(2)
        self.LCD.LCD_Clear()
        
        print("✅ Simple switcher stopped!")

def main():
    try:
        switcher = SimpleButtonSwitcher()
        switcher.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()