#!/usr/bin/env python3
"""
Micro Dots Dripping - Ultra Tiny Particles That Flow Through
Maximum density dots that accumulate and drip down through the bottom
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw

class MicroDotsDripping:
    def __init__(self):
        print("💧 Initializing Micro Dots Dripping...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Ultra-dense pixel streams
        self.pixel_streams = []
        for x in range(0, self.width, 2):
            self.pixel_streams.append({
                'x': x,
                'dots': [],
                'spawn_timer': random.randint(0, 8),
                'intensity': random.uniform(0.3, 1.0),
                'drip_accumulator': []  # Dots that pile up at bottom
            })
        
        # Bottom accumulation layer - tracks dots that have "settled"
        self.bottom_layer = {}  # {x: [dots]} - stacked dots
        
        # Color palettes
        self.neon_greens = [
            (0, 255, 0), (50, 255, 50), (0, 255, 100), 
            (100, 255, 0), (0, 200, 50)
        ]
        
        self.neon_blues = [
            (0, 100, 255), (0, 150, 255), (50, 200, 255),
            (0, 255, 255), (100, 150, 255)
        ]
        
        self.drip_timer = 0  # Controls dripping speed
        
        print(f"💧 Created {len(self.pixel_streams)} dripping streams")
    
    def spawn_dot(self, stream):
        """Spawn a new micro dot"""
        if random.random() < 0.7:
            color = random.choice(self.neon_greens)
        else:
            color = random.choice(self.neon_blues)
        
        return {
            'y': random.uniform(-3, 0),
            'color': color,
            'brightness': 255,
            'speed': random.uniform(0.3, 1.8) * stream['intensity'],
            'settled': False
        }
    
    def settle_dot_at_bottom(self, stream_x, dot):
        """Add dot to bottom accumulation"""
        if stream_x not in self.bottom_layer:
            self.bottom_layer[stream_x] = []
        
        # Add dot to stack with position based on how many are already there
        stack_height = len(self.bottom_layer[stream_x])
        settled_dot = {
            'color': dot['color'],
            'brightness': dot['brightness'],
            'y': self.height - 1 - stack_height,
            'age': 0,
            'drip_chance': random.uniform(0.001, 0.005)  # Chance to drip per frame
        }
        
        self.bottom_layer[stream_x].append(settled_dot)
        
        # Limit stack height to prevent overflow
        if len(self.bottom_layer[stream_x]) > self.height // 3:
            self.bottom_layer[stream_x].pop(0)  # Remove oldest
    
    def process_dripping(self):
        """Make accumulated dots occasionally drip through bottom"""
        self.drip_timer += 1
        
        if self.drip_timer % 10 == 0:  # Check for dripping every 10 frames
            for stream_x, dot_stack in self.bottom_layer.items():
                for dot in dot_stack[:]:
                    dot['age'] += 1
                    
                    # Chance to drip increases with age
                    drip_chance = dot['drip_chance'] * (1 + dot['age'] * 0.01)
                    
                    if random.random() < drip_chance:
                        # Remove from bottom layer and create dripping dot
                        dot_stack.remove(dot)
                        
                        # Create a new falling dot that starts from bottom
                        dripping_dot = {
                            'y': self.height,
                            'color': dot['color'],
                            'brightness': max(100, dot['brightness']),
                            'speed': random.uniform(0.5, 1.5),
                            'settled': False,
                            'is_dripping': True
                        }
                        
                        # Find the stream and add the dripping dot
                        for stream in self.pixel_streams:
                            if stream['x'] == stream_x:
                                stream['dots'].append(dripping_dot)
                                break
                        
                        # Reposition remaining dots in stack
                        for i, remaining_dot in enumerate(dot_stack):
                            remaining_dot['y'] = self.height - 1 - i
    
    def update(self):
        """Update all micro dots"""
        # Process dripping from bottom accumulation
        self.process_dripping()
        
        for stream in self.pixel_streams:
            # Spawn new dots
            if stream['spawn_timer'] <= 0:
                if random.random() < 0.8:
                    stream['dots'].append(self.spawn_dot(stream))
                stream['spawn_timer'] = random.randint(2, 8)
            else:
                stream['spawn_timer'] -= 1
            
            # Update existing dots
            for dot in stream['dots'][:]:
                if not dot['settled']:
                    dot['y'] += dot['speed']
                    
                    # Check if dot hits bottom or accumulated dots
                    hit_bottom = dot['y'] >= self.height - 1
                    hit_stack = False
                    
                    if stream['x'] in self.bottom_layer and self.bottom_layer[stream['x']]:
                        top_dot_y = min(d['y'] for d in self.bottom_layer[stream['x']])
                        hit_stack = dot['y'] >= top_dot_y - 1
                    
                    if hit_bottom or hit_stack:
                        # Settle the dot
                        if not dot.get('is_dripping', False):  # Don't re-settle dripping dots
                            self.settle_dot_at_bottom(stream['x'], dot)
                        stream['dots'].remove(dot)
                    else:
                        # Normal fading for falling dots
                        dot['brightness'] = max(0, dot['brightness'] - 3)
                        if dot['brightness'] <= 0:
                            stream['dots'].remove(dot)
                
                # Remove dots that drip completely off screen
                if dot.get('is_dripping', False) and dot['y'] > self.height + 10:
                    stream['dots'].remove(dot)
    
    def draw_frame(self):
        """Draw ultra-tiny dots with dripping effect"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Draw accumulated dots at bottom
        for stream_x, dot_stack in self.bottom_layer.items():
            for dot in dot_stack:
                if 0 <= dot['y'] < self.height:
                    fade = dot['brightness'] / 255.0
                    r, g, b = dot['color']
                    color = (int(r * fade), int(g * fade), int(b * fade))
                    
                    if 0 <= stream_x < self.width:
                        image.putpixel((stream_x, int(dot['y'])), color)
        
        # Draw falling dots
        for stream in self.pixel_streams:
            for dot in stream['dots']:
                if 0 <= dot['y'] <= self.height + 5:  # Allow dripping dots to show slightly below
                    x = stream['x']
                    y = int(dot['y'])
                    
                    fade = dot['brightness'] / 255.0
                    r, g, b = dot['color']
                    color = (int(r * fade), int(g * fade), int(b * fade))
                    
                    # Draw main pixel
                    if 0 <= x < self.width and 0 <= y < self.height:
                        image.putpixel((x, y), color)
                    
                    # Add slight glow for brighter dots
                    if dot['brightness'] > 150 and random.random() < 0.3:
                        for dx, dy in [(1, 0), (-1, 0), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                glow_color = (
                                    int(r * fade * 0.4),
                                    int(g * fade * 0.4),
                                    int(b * fade * 0.4)
                                )
                                # Only add glow if pixel is currently black
                                if image.getpixel((nx, ny)) == (0, 0, 0):
                                    image.putpixel((nx, ny), glow_color)
                                break
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("💧 Starting Micro Dots Dripping...")
        print("   Ultra-tiny dots that accumulate and drip through the bottom")
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
                if frame % 600 == 0:
                    elapsed = time.time() - start_time
                    falling_dots = sum(len(s['dots']) for s in self.pixel_streams)
                    accumulated_dots = sum(len(stack) for stack in self.bottom_layer.values())
                    print(f"💧 {elapsed:.1f}s: {falling_dots} falling, {accumulated_dots} accumulated")
                
                time.sleep(0.025)  # 40 FPS
                
        except KeyboardInterrupt:
            print(f"\n💧 Dripping dots stopped")
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
        screensaver = MicroDotsDripping()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()