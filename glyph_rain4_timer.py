#!/usr/bin/env python3
"""
Glyph Rain 4 - Accumulating Timer
Tiny colored symbols that fall and accumulate over time
The longer it runs, the more the screen fills up like a visual timer
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont
import math

class GlyphRainTimer:
    def __init__(self):
        print("⏳ Initializing Accumulating Timer Glyph Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R  # Correct orientation
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Tiny symbols and characters
        self.glyphs = '·•▪▫○●◦◯△▲▽▼◇◆□■☆★♦♣♠♥※◊⋄⌘⊙⊗⊘⊚⊛'
        self.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        # Accumulation grid - tracks settled characters
        self.accumulation = {}  # {(x, y): {'char': char, 'color': color, 'age': age}}
        
        # Falling characters
        self.falling_chars = []
        
        # Timer settings
        self.start_time = time.time()
        self.spawn_rate = 0.3  # Probability of spawning per frame
        self.accumulation_height = 0  # How high the pile has grown
        
        print(f"⏳ Timer screensaver ready - will accumulate over time!")
    
    def get_time_color(self, elapsed_hours):
        """Get color based on time elapsed"""
        # Color shifts throughout the day
        hue = (elapsed_hours * 15) % 360  # Full cycle every 24 hours
        
        # Convert HSV to RGB
        h = hue
        s = 0.8  # High saturation
        v = 0.9  # High brightness
        
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
        """Update falling characters and accumulation"""
        elapsed_time = time.time() - self.start_time
        elapsed_hours = elapsed_time / 3600  # Hours elapsed
        
        # Spawn new falling characters (more as time goes on)
        spawn_chance = self.spawn_rate + (elapsed_hours * 0.1)  # Increase over time
        if random.random() < spawn_chance:
            char_set = self.glyphs if random.random() < 0.7 else self.letters
            self.falling_chars.append({
                'char': random.choice(char_set),
                'x': random.randint(0, self.width - 6),
                'y': random.randint(-20, -5),
                'speed': random.uniform(0.2, 1.5),  # Various speeds
                'color': self.get_time_color(elapsed_hours + random.uniform(-1, 1)),
                'size': random.choice(['tiny', 'small', 'normal'])
            })
        
        # Update falling characters
        for char in self.falling_chars[:]:
            char['y'] += char['speed']
            
            # Check if character should settle
            settle_y = self.height - 1
            
            # Check for collision with accumulated characters
            for acc_y in range(int(char['y']), self.height):
                if (int(char['x']), acc_y) in self.accumulation:
                    settle_y = acc_y - 1
                    break
            
            # If character reaches settle position
            if char['y'] >= settle_y:
                # Add to accumulation
                acc_x = int(char['x'])
                acc_y = settle_y
                
                if acc_y >= 0:  # Make sure it's on screen
                    self.accumulation[(acc_x, acc_y)] = {
                        'char': char['char'],
                        'color': char['color'],
                        'age': 0,
                        'size': char['size']
                    }
                    
                    # Update accumulation height
                    self.accumulation_height = max(self.accumulation_height, 
                                                 self.height - acc_y)
                
                self.falling_chars.remove(char)
            
            # Remove characters that fall off screen
            elif char['y'] > self.height + 10:
                self.falling_chars.remove(char)
        
        # Age accumulated characters
        for pos, char_data in self.accumulation.items():
            char_data['age'] += 1
    
    def draw_frame(self):
        """Draw the current frame"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw accumulated characters
        for (x, y), char_data in self.accumulation.items():
            age_factor = min(char_data['age'] / 300.0, 1.0)  # Fade over time
            color = char_data['color']
            
            # Slightly fade older characters
            fade = 1.0 - (age_factor * 0.3)
            faded_color = (int(color[0] * fade), 
                          int(color[1] * fade), 
                          int(color[2] * fade))
            
            try:
                draw.text((x, y), char_data['char'], fill=faded_color, font=font)
            except:
                draw.text((x, y), '·', fill=faded_color, font=font)
        
        # Draw falling characters
        for char in self.falling_chars:
            if 0 <= char['y'] <= self.height:
                try:
                    draw.text((int(char['x']), int(char['y'])), 
                             char['char'], fill=char['color'], font=font)
                except:
                    draw.text((int(char['x']), int(char['y'])), 
                             '·', fill=char['color'], font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("⏳ Starting Accumulating Timer Glyph Rain...")
        print("   Characters will build up over time like a visual timer")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update every 5 minutes
                if frame % 1800 == 0:  # ~5 min at 6 FPS
                    elapsed_time = time.time() - self.start_time
                    elapsed_hours = elapsed_time / 3600
                    total_accumulated = len(self.accumulation)
                    falling_count = len(self.falling_chars)
                    
                    print(f"⏳ {elapsed_hours:.2f}h: {total_accumulated} accumulated, "
                          f"{falling_count} falling, height: {self.accumulation_height}")
                
                time.sleep(0.167)  # ~6 FPS for gradual effect
                
        except KeyboardInterrupt:
            elapsed_time = time.time() - self.start_time
            total_accumulated = len(self.accumulation)
            print(f"\n🛑 Timer stopped after {elapsed_time/3600:.2f} hours")
            print(f"📊 Final stats: {total_accumulated} characters accumulated")
            print(f"📏 Maximum height reached: {self.accumulation_height} pixels")
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
        screensaver = GlyphRainTimer()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()