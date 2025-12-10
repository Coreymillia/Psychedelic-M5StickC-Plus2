#!/usr/bin/env python3
"""
Plasma Field - Classic 1990s Plasma Effect
Retro plasma field with mathematical color patterns
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class PlasmaField:
    def __init__(self):
        print("🌈 Initializing Plasma Field...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Plasma parameters
        self.time = 0
        self.plasma_speed = 0.05
        
        # Classic 1990s palette generation
        self.palette = self.generate_retro_palette()
        
        print(f"🌈 Plasma field initialized")
    
    def generate_retro_palette(self):
        """Generate classic 1990s color palette"""
        palette = []
        
        for i in range(256):
            # Classic plasma colors - lots of purples, blues, magentas
            t = i / 255.0
            
            # Multi-wave color generation for retro feel
            r = int(128 + 127 * math.sin(t * math.pi * 2))
            g = int(128 + 127 * math.sin(t * math.pi * 2 + math.pi / 3))
            b = int(128 + 127 * math.sin(t * math.pi * 2 + 2 * math.pi / 3))
            
            # Boost certain retro colors
            if 0.2 < t < 0.4:  # Enhance magentas
                r = min(255, int(r * 1.3))
                b = min(255, int(b * 1.2))
            elif 0.6 < t < 0.8:  # Enhance cyans
                g = min(255, int(g * 1.3))
                b = min(255, int(b * 1.3))
            
            palette.append((r, g, b))
        
        return palette
    
    def plasma_function(self, x, y, time):
        """Calculate plasma value for given coordinates"""
        # Multiple sine waves for classic plasma effect
        value = 0
        
        # Wave 1 - horizontal movement
        value += math.sin((x + time * 30) / 16)
        
        # Wave 2 - vertical movement
        value += math.sin((y + time * 20) / 8)
        
        # Wave 3 - diagonal movement
        value += math.sin((x + y + time * 25) / 16)
        
        # Wave 4 - circular patterns
        cx, cy = self.width // 2, self.height // 2
        dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        value += math.sin(dist / 8 + time * 15)
        
        # Wave 5 - rotating pattern
        angle = math.atan2(y - cy, x - cx)
        value += math.sin(angle * 3 + time * 10)
        
        # Normalize to 0-1 range
        return (value + 5) / 10
    
    def draw_frame(self):
        """Draw plasma field"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Calculate plasma for each pixel
        for y in range(self.height):
            for x in range(self.width):
                # Calculate plasma value
                plasma_value = self.plasma_function(x, y, self.time)
                
                # Map to palette index
                palette_index = int(plasma_value * 255) % 256
                color = self.palette[palette_index]
                
                # Set pixel
                image.putpixel((x, y), color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🌈 Starting Plasma Field...")
        print("   Classic 1990s mathematical plasma effect")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                # Update time for animation
                self.time += self.plasma_speed
                frame += 1
                
                # Status update
                if frame % 300 == 0:
                    elapsed = time.time() - start_time
                    print(f"🌈 {elapsed:.1f}s: Plasma time = {self.time:.2f}")
                
                time.sleep(0.05)  # 20 FPS
                
        except KeyboardInterrupt:
            print(f"\n🌈 Plasma field stopped")
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
        screensaver = PlasmaField()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()