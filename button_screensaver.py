#!/usr/bin/env python3
"""
Button-Controlled Screensaver Switcher for Waveshare 1.44" LCD HAT
Physical button controls to switch between screensavers on the fly!

Controls:
- KEY1 (Pin 21): Next screensaver
- KEY2 (Pin 20): Previous screensaver  
- KEY3 (Pin 16): Toggle pause/resume
- Joystick UP (Pin 6): Jump to favorite screensavers
- Joystick DOWN (Pin 19): Show current screensaver info
- Joystick PRESS (Pin 13): Exit switcher
"""

import time
import threading
import subprocess
import os
import signal
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44

class ButtonScreensaverSwitcher:
    def __init__(self):
        print("🕹️ Initializing Button-Controlled Screensaver Switcher...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        
        # Button setup (with pull-up resistors)
        self.key1 = Button(21, pull_up=True)      # Next screensaver
        self.key2 = Button(20, pull_up=True)      # Previous screensaver
        self.key3 = Button(16, pull_up=True)      # Pause/Resume
        self.joy_up = Button(6, pull_up=True)     # Jump to favorites
        self.joy_down = Button(19, pull_up=True)  # Show info
        self.joy_press = Button(13, pull_up=True) # Exit
        
        # Screensaver list (prioritized for button switching)
        self.screensavers = [
            # Top picks - most stable and visually appealing
            {
                'file': 'glyph_rain1_fixed.py',
                'name': 'Fixed Matrix Rain',
                'category': '⭐ STABLE',
                'description': 'Memory-safe classic matrix'
            },
            {
                'file': 'glyph_rain2.py',
                'name': 'Blue Matrix Rain',
                'category': 'Matrix',
                'description': 'Blue matrix theme'
            },
            {
                'file': 'glyph_rain3.py',
                'name': 'Rainbow Matrix',
                'category': 'Matrix',
                'description': 'Rainbow colored matrix'
            },
            {
                'file': 'neon_rain.py',
                'name': 'Neon Rain',
                'category': 'Matrix',
                'description': 'Neon shapes rain'
            },
            {
                'file': 'simple_flames.py',
                'name': 'Simple Flames',
                'category': 'Fire',
                'description': 'Stable flame effect'
            },
            {
                'file': 'plasma_field.py',
                'name': 'Plasma Field',
                'category': 'Retro',
                'description': 'Mathematical plasma'
            },
            {
                'file': 'bouncing_balls.py',
                'name': 'Bouncing Balls',
                'category': 'Retro',
                'description': 'Classic bouncing balls'
            },
            {
                'file': 'kaleidoscope.py',
                'name': 'Kaleidoscope',
                'category': 'Visual',
                'description': 'Rotating patterns'
            },
            {
                'file': 'micro_dots.py',
                'name': 'Micro Dots',
                'category': 'Particles',
                'description': 'Ultra-tiny dots'
            },
            {
                'file': 'raindrops.py',
                'name': 'Raindrops',
                'category': 'Water',
                'description': 'Realistic rain'
            }
        ]
        
        # Favorites (accessed with UP button)
        self.favorites = [0, 1, 4, 5]  # Indices of favorite screensavers
        self.favorite_index = 0
        
        # State
        self.current_index = 0
        self.current_process = None
        self.paused = False
        self.running = True
        self.last_button_time = 0
        self.debounce_time = 0.3
        
        # Setup button handlers
        self.setup_button_handlers()
        
        print("✅ Button switcher ready!")
        self.show_controls()
        
    def setup_button_handlers(self):
        """Setup button event handlers"""
        self.key1.when_pressed = self.next_screensaver
        self.key2.when_pressed = self.previous_screensaver
        self.key3.when_pressed = self.toggle_pause
        self.joy_up.when_pressed = self.next_favorite
        self.joy_down.when_pressed = self.show_info
        self.joy_press.when_pressed = self.exit_switcher
        
    def debounce_check(self):
        """Simple debounce to prevent button spam"""
        current_time = time.time()
        if current_time - self.last_button_time < self.debounce_time:
            return False
        self.last_button_time = current_time
        return True
    
    def show_controls(self):
        """Display control instructions on LCD"""
        image = Image.new('RGB', (self.LCD.width, self.LCD.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        lines = [
            "Button Controls:",
            "",
            "KEY1: Next →",
            "KEY2: ← Prev", 
            "KEY3: Pause ⏸",
            "↑: Favorites ⭐",
            "↓: Info ℹ️",
            "⭕: Exit"
        ]
        
        y = 5
        for line in lines:
            draw.text((2, y), line, fill=(255, 255, 255), font=font)
            y += 12
        
        self.LCD.LCD_ShowImage(image, 0, 0)
        time.sleep(3)
    
    def show_screensaver_info(self, index):
        """Display current screensaver info"""
        if index >= len(self.screensavers):
            return
            
        saver = self.screensavers[index]
        image = Image.new('RGB', (self.LCD.width, self.LCD.height), (0, 20, 40))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        # Title
        draw.text((2, 2), f"#{index + 1}: {saver['name'][:12]}", 
                 fill=(255, 255, 0), font=font)
        
        # Category
        draw.text((2, 18), f"Cat: {saver['category']}", 
                 fill=(200, 200, 255), font=font)
        
        # Description (word wrap)
        desc_lines = []
        words = saver['description'].split()
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) <= 15:  # Rough character limit
                current_line = test_line
            else:
                if current_line:
                    desc_lines.append(current_line)
                current_line = word
        if current_line:
            desc_lines.append(current_line)
        
        y = 34
        for line in desc_lines[:4]:  # Max 4 lines
            draw.text((2, y), line, fill=(200, 255, 200), font=font)
            y += 12
        
        # Controls reminder
        draw.text((2, 110), "KEY1→ KEY2← KEY3⏸", fill=(150, 150, 150), font=font)
        
        self.LCD.LCD_ShowImage(image, 0, 0)
        time.sleep(2)
    
    def start_screensaver(self, index):
        """Start a specific screensaver"""
        if index >= len(self.screensavers):
            print(f"❌ Invalid screensaver index: {index}")
            return False
            
        saver = self.screensavers[index]
        filepath = saver['file']
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
        
        # Stop current screensaver
        self.stop_current_screensaver()
        
        # Show info briefly
        self.show_screensaver_info(index)
        
        try:
            print(f"🚀 Starting: {saver['name']}")
            self.current_process = subprocess.Popen(['python3', filepath])
            return True
        except Exception as e:
            print(f"❌ Error starting screensaver: {e}")
            return False
    
    def stop_current_screensaver(self):
        """Stop the currently running screensaver"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            except:
                pass
            finally:
                self.current_process = None
        
        # Also kill any orphaned Python screensaver processes
        try:
            subprocess.run(['pkill', '-f', 'glyph_rain'], capture_output=True)
            subprocess.run(['pkill', '-f', 'screensaver'], capture_output=True)
        except:
            pass
    
    def next_screensaver(self):
        """Switch to next screensaver"""
        if not self.debounce_check():
            return
            
        self.current_index = (self.current_index + 1) % len(self.screensavers)
        print(f"🔄 Next → #{self.current_index + 1}")
        self.start_screensaver(self.current_index)
    
    def previous_screensaver(self):
        """Switch to previous screensaver"""
        if not self.debounce_check():
            return
            
        self.current_index = (self.current_index - 1) % len(self.screensavers)
        print(f"🔄 Prev ← #{self.current_index + 1}")
        self.start_screensaver(self.current_index)
    
    def next_favorite(self):
        """Jump to next favorite screensaver"""
        if not self.debounce_check():
            return
            
        self.favorite_index = (self.favorite_index + 1) % len(self.favorites)
        self.current_index = self.favorites[self.favorite_index]
        print(f"⭐ Favorite → #{self.current_index + 1}")
        self.start_screensaver(self.current_index)
    
    def toggle_pause(self):
        """Toggle pause/resume current screensaver"""
        if not self.debounce_check():
            return
            
        if self.current_process:
            try:
                if self.paused:
                    # Resume
                    self.current_process.send_signal(signal.SIGCONT)
                    self.paused = False
                    print("▶️ Resumed")
                else:
                    # Pause
                    self.current_process.send_signal(signal.SIGSTOP)
                    self.paused = True
                    print("⏸️ Paused")
            except Exception as e:
                print(f"❌ Pause/resume error: {e}")
    
    def show_info(self):
        """Show current screensaver info"""
        if not self.debounce_check():
            return
            
        print(f"ℹ️ Info: #{self.current_index + 1}")
        self.show_screensaver_info(self.current_index)
    
    def exit_switcher(self):
        """Exit the switcher"""
        if not self.debounce_check():
            return
            
        print("🚪 Exit button pressed")
        self.running = False
    
    def run(self):
        """Main run loop"""
        print("🕹️ Button Screensaver Switcher Active!")
        print("📋 Controls:")
        print("   KEY1 (Pin 21): Next screensaver →")
        print("   KEY2 (Pin 20): Previous screensaver ←") 
        print("   KEY3 (Pin 16): Pause/Resume ⏸️")
        print("   UP (Pin 6): Next favorite ⭐")
        print("   DOWN (Pin 19): Show info ℹ️")
        print("   PRESS (Pin 13): Exit 🚪")
        print()
        
        # Start with first screensaver
        self.start_screensaver(self.current_index)
        
        try:
            # Keep running until exit button pressed
            while self.running:
                time.sleep(0.1)
                
                # Check if current screensaver crashed
                if self.current_process and self.current_process.poll() is not None:
                    print("⚠️ Screensaver ended, restarting...")
                    self.start_screensaver(self.current_index)
                    
        except KeyboardInterrupt:
            print("\n🛑 Ctrl+C pressed")
        
        print("🧹 Cleaning up...")
        self.stop_current_screensaver()
        self.LCD.LCD_Clear()
        print("✅ Button switcher stopped!")

def main():
    try:
        switcher = ButtonScreensaverSwitcher()
        switcher.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()