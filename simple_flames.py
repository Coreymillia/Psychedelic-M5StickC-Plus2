#!/usr/bin/env python3
"""
Simple Flames - Stable Fire Effect
Simple animated flames rising from the bottom
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class SimpleFlames:
    def __init__(self):
        print("🔥 Initializing Simple Flames...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Simple flame particles
        self.flames = []
        
        # Fire colors - simple red to yellow gradient
        self.fire_colors = [
            (139, 0, 0),      # Dark red
            (178, 34, 34),    # Fire brick
            (220, 20, 60),    # Crimson  
            (255, 0, 0),      # Red
            (255, 69, 0),     # Red orange
            (255, 140, 0),    # Dark orange
            (255, 165, 0),    # Orange
            (255, 215, 0),    # Gold
            (255, 255, 0),    # Yellow
            (255, 255, 224),  # Light yellow
        ]
        
        self.time = 0
        print(f"🔥 Simple flames ready")
    
    def create_flame_particle(self):
        """Create a simple flame particle"""
        return {
            'x': random.randint(20, self.width - 20),
            'y': self.height - 1,
            'vy': random.uniform(-1.5, -3.0),
            'vx': random.uniform(-0.5, 0.5),
            'life': random.randint(30, 60),
            'max_life': random.randint(30, 60),
            'size': random.randint(1, 3)
        }
    
    def update(self):
        """Update flame particles"""
        self.time += 1
        
        # Spawn new flames from bottom
        if random.random() < 0.7:  # 70% chance
            self.flames.append(self.create_flame_particle())
        
        # Update existing flames
        for flame in self.flames[:]:
            # Move flame up and slightly sideways
            flame['y'] += flame['vy']
            flame['x'] += flame['vx']
            
            # Add some flickering motion
            flame['vx'] += random.uniform(-0.1, 0.1)
            flame['vx'] = max(-1, min(1, flame['vx']))  # Limit sideways motion
            
            # Age the flame
            flame['life'] -= 1
            
            # Remove old or off-screen flames
            if flame['life'] <= 0 or flame['y'] < -10:
                self.flames.remove(flame)
    
    def draw_frame(self):
        """Draw simple flames"""
        # Black background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Draw each flame particle
        for flame in self.flames:
            if 0 <= flame['y'] <= self.height and 0 <= flame['x'] < self.width:
                # Choose color based on age (newer = hotter = more yellow)
                age_factor = flame['life'] / flame['max_life']
                color_index = min(len(self.fire_colors) - 1, int(age_factor * len(self.fire_colors)))
                color = self.fire_colors[color_index]
                
                # Draw the flame particle
                x, y = int(flame['x']), int(flame['y'])
                size = flame['size']
                
                # Draw main particle
                if 0 <= x < self.width and 0 <= y < self.height:
                    image.putpixel((x, y), color)
                
                # Draw flame shape (make it look more flame-like)
                for dx in range(-size, size + 1):
                    for dy in range(-size, size + 1):
                        px, py = x + dx, y + dy
                        
                        # Create flame-like shape (wider at bottom, narrower at top)
                        if dy <= 0:  # Only draw upward/same level
                            dist = abs(dx) + abs(dy * 0.5)  # Bias toward vertical
                            if dist <= size and 0 <= px < self.width and 0 <= py < self.height:
                                # Fade intensity based on distance from center
                                intensity = 1.0 - (dist / size)
                                r, g, b = color
                                fade_color = (
                                    int(r * intensity),
                                    int(g * intensity),
                                    int(b * intensity)
                                )
                                
                                # Only draw if brighter than current pixel
                                current = image.getpixel((px, py))
                                if sum(fade_color) > sum(current):
                                    image.putpixel((px, py), fade_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔥 Starting Simple Flames...")
        print("   Stable flame effect rising from bottom")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update
                if frame % 400 == 0:
                    elapsed = time.time() - start_time
                    flame_count = len(self.flames)
                    print(f"🔥 {elapsed:.1f}s: {flame_count} flame particles")
                
                time.sleep(0.05)  # 20 FPS
                
        except KeyboardInterrupt:
            print(f"\n🔥 Flames extinguished")
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
        screensaver = SimpleFlames()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()