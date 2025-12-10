#!/usr/bin/env python3
"""
Glyph Rain 2 - Blue Matrix Theme
Matrix-style falling characters in blue colors
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class GlyphRain2:
    def __init__(self):
        print("🌧️ Initializing Blue Matrix Glyph Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R  # Correct orientation
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Binary and hex characters for a more digital feel
        self.glyphs = '01ABCDEF0123456789{}[]()<>+-*/=?!@#$%^&|\\~_'
        
        # Create falling columns
        self.columns = []
        col_width = 10  # Slightly wider spacing
        for x in range(0, self.width, col_width):
            self.columns.append({
                'x': x,
                'chars': [],
                'spawn_timer': random.randint(0, 40)
            })
        
        print(f"🔵 Created {len(self.columns)} blue matrix columns")
    
    def update(self):
        """Update all falling characters"""
        for col in self.columns:
            # Spawn new character
            if col['spawn_timer'] <= 0:
                col['chars'].append({
                    'char': random.choice(self.glyphs),
                    'y': -10,
                    'brightness': 255,
                    'speed': random.uniform(1.0, 3.0)  # Faster than original
                })
                col['spawn_timer'] = random.randint(15, 70)
            else:
                col['spawn_timer'] -= 1
            
            # Update existing characters
            for char in col['chars'][:]:
                char['y'] += char['speed']
                char['brightness'] = max(0, char['brightness'] - 5)  # Faster fade
                
                if char['y'] > self.height + 10 or char['brightness'] <= 0:
                    col['chars'].remove(char)
    
    def draw_frame(self):
        """Draw the current frame with blue theme"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all falling characters in blue tones
        for col in self.columns:
            for char in col['chars']:
                if 0 <= char['y'] <= self.height:
                    b = char['brightness']
                    
                    # Blue color scheme
                    if b > 200:
                        color = (255, 255, 255)  # White lead
                    elif b > 150:
                        color = (200, 200, 255)  # Light blue
                    elif b > 100:
                        blue = int(b * 0.9)
                        color = (0, 50, blue)    # Medium blue
                    else:
                        blue = int(b * 0.7)
                        color = (0, 20, blue)    # Dark blue trail
                    
                    try:
                        draw.text((col['x'], int(char['y'])), 
                                 char['char'], fill=color, font=font)
                    except:
                        draw.text((col['x'], int(char['y'])), 
                                 '?', fill=color, font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔵 Starting Blue Matrix Glyph Rain...")
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
                    print(f"🔵 {elapsed:.1f}s: {total_chars} glyphs, {fps:.1f} FPS")
                
                time.sleep(0.025)  # Slightly faster (~40 FPS)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Blue Matrix stopped after {frame} frames")
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
        screensaver = GlyphRain2()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()