#!/usr/bin/env python3
"""
Micro Dots - Ultra Tiny Falling Particles
Maximum density of 1-pixel dots in neon green and blue
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw

class MicroDots:
    def __init__(self):
        print("🔬 Initializing Micro Dots...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Ultra-dense pixel streams - every other pixel
        self.pixel_streams = []
        for x in range(0, self.width, 2):  # Every 2 pixels
            self.pixel_streams.append({
                'x': x,
                'dots': [],
                'spawn_timer': random.randint(0, 8),
                'intensity': random.uniform(0.3, 1.0)
            })
        
        # Color palettes
        self.neon_greens = [
            (0, 255, 0),      # Pure neon green
            (50, 255, 50),    # Bright green
            (0, 255, 100),    # Green-cyan
            (100, 255, 0),    # Lime green
            (0, 200, 50),     # Forest neon
        ]
        
        self.neon_blues = [
            (0, 100, 255),    # Neon blue
            (0, 150, 255),    # Electric blue
            (50, 200, 255),   # Cyan-blue
            (0, 255, 255),    # Pure cyan
            (100, 150, 255),  # Purple-blue
        ]
        
        print(f"🔬 Created {len(self.pixel_streams)} micro dot streams")
    
    def spawn_dot(self, stream):
        """Spawn a new micro dot"""
        # 70% green, 30% blue
        if random.random() < 0.7:
            color = random.choice(self.neon_greens)
        else:
            color = random.choice(self.neon_blues)
        
        return {
            'y': random.uniform(-3, 0),
            'color': color,
            'brightness': 255,
            'speed': random.uniform(0.3, 1.8) * stream['intensity'],
            'trail_length': random.randint(2, 6)
        }
    
    def update(self):
        """Update all micro dots"""
        for stream in self.pixel_streams:
            # High frequency spawning for maximum density
            if stream['spawn_timer'] <= 0:
                if random.random() < 0.8:  # 80% chance to spawn
                    stream['dots'].append(self.spawn_dot(stream))
                stream['spawn_timer'] = random.randint(2, 8)
            else:
                stream['spawn_timer'] -= 1
            
            # Update existing dots
            for dot in stream['dots'][:]:
                dot['y'] += dot['speed']
                dot['brightness'] = max(0, dot['brightness'] - 5)
                
                # Remove dots that are off screen or faded
                if dot['y'] > self.height + 3 or dot['brightness'] <= 0:
                    stream['dots'].remove(dot)
    
    def draw_frame(self):
        """Draw ultra-tiny dots"""
        # Start with black
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Draw each dot as 1-2 pixels
        for stream in self.pixel_streams:
            for dot in stream['dots']:
                if 0 <= dot['y'] <= self.height:
                    x = stream['x']
                    y = int(dot['y'])
                    
                    # Apply brightness fade to color
                    fade = dot['brightness'] / 255.0
                    r, g, b = dot['color']
                    faded_color = (
                        int(r * fade),
                        int(g * fade),
                        int(b * fade)
                    )
                    
                    # Draw main pixel
                    if 0 <= x < self.width and 0 <= y < self.height:
                        image.putpixel((x, y), faded_color)
                    
                    # Sometimes add a second pixel for slightly larger dots
                    if random.random() < 0.4 and dot['brightness'] > 150:
                        # Add neighboring pixel
                        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                # Dimmer neighboring pixel
                                dimmer_color = (
                                    int(r * fade * 0.6),
                                    int(g * fade * 0.6),
                                    int(b * fade * 0.6)
                                )
                                image.putpixel((nx, ny), dimmer_color)
                                break  # Only add one neighbor
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔬 Starting Micro Dots...")
        print("   Ultra-tiny neon particles at maximum density")
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
                if frame % 500 == 0:
                    elapsed = time.time() - start_time
                    total_dots = sum(len(s['dots']) for s in self.pixel_streams)
                    print(f"🔬 {elapsed:.1f}s: {total_dots} micro dots active")
                
                time.sleep(0.025)  # 40 FPS for ultra-smooth tiny motion
                
        except KeyboardInterrupt:
            print(f"\n🔬 Micro dots stopped")
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
        screensaver = MicroDots()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()