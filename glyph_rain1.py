#!/usr/bin/env python3
"""
Glyph Rain Screensaver - Using Official Waveshare 1.44" LCD Driver
Matrix-style falling characters
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class GlyphRain:
    def __init__(self):
        print("🌧️ Initializing Glyph Rain with official Waveshare driver...")
        
        # Initialize LCD using official driver
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R  # Setting #5
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Glyph characters for the matrix rain
        self.glyphs = '0123456789ABCDEFabcdef!@#$%^&*()[]{}+-=<>?/\\|_~πΩαβγδλμσφ'
        
        # Create falling columns
        self.columns = []
        col_width = 8  # Character width spacing
        for x in range(0, self.width, col_width):
            self.columns.append({
                'x': x,
                'chars': [],
                'spawn_timer': random.randint(0, 50)
            })
        
        print(f"🌧️ Created {len(self.columns)} falling columns")
    
    def update(self):
        """Update all falling characters"""
        for col in self.columns:
            # Spawn new character at top
            if col['spawn_timer'] <= 0:
                col['chars'].append({
                    'char': random.choice(self.glyphs),
                    'y': -10,
                    'brightness': 255,
                    'speed': random.uniform(0.8, 2.5)
                })
                col['spawn_timer'] = random.randint(25, 100)
            else:
                col['spawn_timer'] -= 1
            
            # Update existing characters
            for char in col['chars'][:]:
                char['y'] += char['speed']
                char['brightness'] = max(0, char['brightness'] - 4)
                
                # Remove characters that are off screen or too dim
                if char['y'] > self.height + 10 or char['brightness'] <= 0:
                    col['chars'].remove(char)
    
    def draw_frame(self):
        """Draw the current frame"""
        # Create black background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Use default font
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all falling characters
        for col in self.columns:
            for char in col['chars']:
                if 0 <= char['y'] <= self.height:
                    b = char['brightness']
                    
                    # Color scheme: bright white for lead, green trail
                    if b > 200:
                        color = (255, 255, 255)  # Bright white lead
                    elif b > 150:
                        color = (200, 255, 200)  # Light green
                    elif b > 100:
                        green = int(b * 0.9)
                        color = (0, green, 0)    # Medium green
                    else:
                        green = int(b * 0.6)
                        color = (0, green, 0)    # Dark green trail
                    
                    try:
                        draw.text((col['x'], int(char['y'])), 
                                 char['char'], fill=color, font=font)
                    except:
                        # Fallback for unsupported characters
                        draw.text((col['x'], int(char['y'])), 
                                 '?', fill=color, font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🌧️ Starting Matrix-style Glyph Rain...")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                # Update character positions
                self.update()
                
                # Draw frame
                image = self.draw_frame()
                
                # Display on LCD
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update every 10 seconds
                if frame % 300 == 0:
                    elapsed = time.time() - start_time
                    fps = frame / elapsed if elapsed > 0 else 0
                    total_chars = sum(len(col['chars']) for col in self.columns)
                    print(f"🌧️ {elapsed:.1f}s: {total_chars} glyphs, {fps:.1f} FPS")
                
                # Control frame rate (~30 FPS)
                time.sleep(0.033)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Glyph Rain stopped after {frame} frames")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            print("🧹 Clearing screen...")
            self.LCD.LCD_Clear()
            print("✅ Cleanup complete")
        except Exception as e:
            print(f"Cleanup error: {e}")

def main():
    try:
        screensaver = GlyphRain()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()