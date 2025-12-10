#!/usr/bin/env python3
"""
Glyph Rain 3 - Rainbow Matrix
Matrix-style falling characters with rainbow colors
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont
import math

class GlyphRain3:
    def __init__(self):
        print("🌈 Initializing Rainbow Matrix Glyph Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R  # Correct orientation
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Unicode and special characters for variety
        self.glyphs = '0123456789ABCDEFabcdef!@#$%^&*()[]{}+-=<>?/\\|_~♦♣♠♥★☆○●△▲'
        
        # Create falling columns
        self.columns = []
        col_width = 9
        for x in range(0, self.width, col_width):
            self.columns.append({
                'x': x,
                'chars': [],
                'spawn_timer': random.randint(0, 60),
                'color_offset': random.randint(0, 360)  # For rainbow effect
            })
        
        self.time_offset = 0
        print(f"🌈 Created {len(self.columns)} rainbow columns")
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def update(self):
        """Update all falling characters"""
        self.time_offset += 1
        
        for col in self.columns:
            # Spawn new character
            if col['spawn_timer'] <= 0:
                col['chars'].append({
                    'char': random.choice(self.glyphs),
                    'y': -10,
                    'brightness': 255,
                    'speed': random.uniform(0.5, 2.0),
                    'hue': (col['color_offset'] + self.time_offset * 2) % 360
                })
                col['spawn_timer'] = random.randint(30, 90)
            else:
                col['spawn_timer'] -= 1
            
            # Update existing characters
            for char in col['chars'][:]:
                char['y'] += char['speed']
                char['brightness'] = max(0, char['brightness'] - 3)
                char['hue'] = (char['hue'] + 1) % 360  # Slowly shift hue
                
                if char['y'] > self.height + 10 or char['brightness'] <= 0:
                    col['chars'].remove(char)
    
    def draw_frame(self):
        """Draw the current frame with rainbow colors"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all falling characters with rainbow colors
        for col in self.columns:
            for char in col['chars']:
                if 0 <= char['y'] <= self.height:
                    brightness_factor = char['brightness'] / 255.0
                    
                    # Get rainbow color
                    if brightness_factor > 0.8:
                        # Bright white for lead
                        color = (255, 255, 255)
                    else:
                        # Rainbow colors for trail
                        saturation = 1.0
                        value = brightness_factor * 0.9
                        color = self.hsv_to_rgb(char['hue'], saturation, value)
                    
                    try:
                        draw.text((col['x'], int(char['y'])), 
                                 char['char'], fill=color, font=font)
                    except:
                        draw.text((col['x'], int(char['y'])), 
                                 '?', fill=color, font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🌈 Starting Rainbow Matrix Glyph Rain...")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                if frame % 300 == 0:
                    elapsed = time.time() - start_time
                    fps = frame / elapsed if elapsed > 0 else 0
                    total_chars = sum(len(col['chars']) for col in self.columns)
                    print(f"🌈 {elapsed:.1f}s: {total_chars} glyphs, {fps:.1f} FPS")
                
                time.sleep(0.04)  # 25 FPS for smooth color transitions
                
        except KeyboardInterrupt:
            print(f"\n🛑 Rainbow Matrix stopped after {frame} frames")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Clearing screen...")
            self.LCD.LCD_Clear()
            print("✅ Cleanup complete")
        except Exception as e:
            print(f"Cleanup error: {e}")

if __name__ == "__main__":
    try:
        screensaver = GlyphRain3()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()