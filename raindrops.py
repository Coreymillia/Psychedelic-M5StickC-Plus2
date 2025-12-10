#!/usr/bin/env python3
"""
Raindrops - Realistic Water Drop Effect
Falling raindrops with water-like appearance and splashing
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class Raindrops:
    def __init__(self):
        print("🌧️ Initializing Raindrops...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Raindrop streams - less dense than micro dots for realistic effect
        self.raindrop_streams = []
        stream_spacing = 8  # More space between drops
        for x in range(0, self.width, stream_spacing):
            self.raindrop_streams.append({
                'x': x,
                'drops': [],
                'spawn_timer': random.randint(0, 60),  # Longer delays
                'wind_offset': random.uniform(-2, 2)  # Slight wind effect
            })
        
        # Water puddles at bottom - where drops collect
        self.puddles = {}  # {x: puddle_height}
        
        # Splash effects
        self.splashes = []
        
        # Water color palette - blues and whites
        self.water_colors = [
            (173, 216, 230),  # Light blue
            (135, 206, 235),  # Sky blue
            (176, 224, 230),  # Powder blue
            (240, 248, 255),  # Alice blue
            (230, 230, 250),  # Lavender
            (200, 200, 255),  # Light periwinkle
        ]
        
        print(f"🌧️ Created {len(self.raindrop_streams)} raindrop streams")
    
    def create_raindrop(self, stream):
        """Create a realistic raindrop"""
        return {
            'y': random.uniform(-10, -5),
            'size': random.choice(['small', 'medium', 'large']),
            'color': random.choice(self.water_colors),
            'speed': random.uniform(1.5, 4.0),
            'brightness': random.randint(180, 255),
            'wind_drift': stream['wind_offset'] * random.uniform(0.5, 1.5),
            'trail_length': random.randint(3, 8)
        }
    
    def create_splash(self, x, y, intensity):
        """Create splash effect when drop hits something"""
        splash = {
            'x': x,
            'y': y,
            'particles': [],
            'life': 20,  # Frames to live
            'intensity': intensity
        }
        
        # Create splash particles
        for i in range(intensity):
            angle = random.uniform(0, 3.14159)  # Half circle upward
            speed = random.uniform(1, 3)
            splash['particles'].append({
                'dx': speed * random.uniform(-1, 1),
                'dy': -speed * random.uniform(0.5, 2),  # Upward motion
                'life': random.randint(10, 25),
                'size': random.choice(['tiny', 'small']),
                'color': random.choice(self.water_colors)
            })
        
        self.splashes.append(splash)
    
    def update_puddles(self, x):
        """Add to puddle at position x"""
        if x not in self.puddles:
            self.puddles[x] = 0
        
        # Slowly accumulate water
        self.puddles[x] = min(self.puddles[x] + 0.5, 8)  # Max puddle height
        
        # Evaporation - puddles slowly shrink
        for px in list(self.puddles.keys()):
            self.puddles[px] = max(0, self.puddles[px] - 0.02)
            if self.puddles[px] <= 0:
                del self.puddles[px]
    
    def update(self):
        """Update raindrops and effects"""
        # Update raindrop streams
        for stream in self.raindrop_streams:
            # Spawn new raindrops occasionally
            if stream['spawn_timer'] <= 0:
                if random.random() < 0.3:  # 30% chance
                    stream['drops'].append(self.create_raindrop(stream))
                stream['spawn_timer'] = random.randint(30, 120)  # Varied timing
            else:
                stream['spawn_timer'] -= 1
            
            # Update existing drops
            for drop in stream['drops'][:]:
                drop['y'] += drop['speed']
                
                # Apply wind drift
                drop['x_offset'] = getattr(drop, 'x_offset', 0) + drop['wind_drift'] * 0.1
                
                # Check if drop hits bottom or puddle
                puddle_height = self.puddles.get(stream['x'], 0)
                hit_surface = drop['y'] >= self.height - 1 - puddle_height
                
                if hit_surface:
                    # Create splash
                    splash_intensity = {'small': 2, 'medium': 4, 'large': 6}[drop['size']]
                    self.create_splash(stream['x'], drop['y'], splash_intensity)
                    
                    # Add to puddle
                    self.update_puddles(stream['x'])
                    
                    # Remove drop
                    stream['drops'].remove(drop)
                elif drop['y'] > self.height + 10:
                    stream['drops'].remove(drop)
        
        # Update splashes
        for splash in self.splashes[:]:
            splash['life'] -= 1
            
            for particle in splash['particles'][:]:
                particle['life'] -= 1
                particle['dy'] += 0.2  # Gravity
                
                if particle['life'] <= 0:
                    splash['particles'].remove(particle)
            
            if splash['life'] <= 0 or not splash['particles']:
                self.splashes.remove(splash)
    
    def draw_frame(self):
        """Draw raindrops and water effects"""
        image = Image.new('RGB', (self.width, self.height), (20, 20, 40))  # Dark blue-gray sky
        draw = ImageDraw.Draw(image)
        
        # Draw puddles at bottom
        for x, height in self.puddles.items():
            if height > 0:
                # Draw puddle as horizontal line(s)
                puddle_color = (100, 150, 200)  # Puddle blue
                for h in range(int(height)):
                    y = self.height - 1 - h
                    if 0 <= y < self.height:
                        # Draw puddle line with some width
                        for px in range(max(0, x-2), min(self.width, x+3)):
                            image.putpixel((px, y), puddle_color)
        
        # Draw raindrops
        for stream in self.raindrop_streams:
            for drop in stream['drops']:
                if 0 <= drop['y'] <= self.height:
                    x = stream['x'] + int(getattr(drop, 'x_offset', 0))
                    y = int(drop['y'])
                    
                    # Ensure x is in bounds
                    x = max(0, min(self.width - 1, x))
                    
                    # Draw drop based on size
                    if drop['size'] == 'large':
                        # Draw 3-pixel drop
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                px, py = x + dx, y + dy
                                if 0 <= px < self.width and 0 <= py < self.height:
                                    image.putpixel((px, py), drop['color'])
                    elif drop['size'] == 'medium':
                        # Draw 2-pixel drop
                        for dy in range(-1, 1):
                            px, py = x, y + dy
                            if 0 <= px < self.width and 0 <= py < self.height:
                                image.putpixel((px, py), drop['color'])
                        # Add side pixels occasionally
                        if random.random() < 0.5:
                            for dx in [-1, 1]:
                                px, py = x + dx, y
                                if 0 <= px < self.width and 0 <= py < self.height:
                                    image.putpixel((px, py), drop['color'])
                    else:  # small
                        # Single pixel drop
                        if 0 <= x < self.width and 0 <= y < self.height:
                            image.putpixel((x, y), drop['color'])
                    
                    # Draw trail for faster drops
                    if drop['speed'] > 2.5:
                        trail_length = min(drop['trail_length'], int(drop['speed']))
                        for t in range(1, trail_length):
                            trail_y = y - t
                            if 0 <= trail_y < self.height:
                                # Fading trail
                                fade = 1.0 - (t / trail_length)
                                r, g, b = drop['color']
                                trail_color = (
                                    int(r * fade * 0.6),
                                    int(g * fade * 0.6),
                                    int(b * fade * 0.6)
                                )
                                if 0 <= x < self.width:
                                    image.putpixel((x, trail_y), trail_color)
        
        # Draw splash effects
        for splash in self.splashes:
            for particle in splash['particles']:
                px = int(splash['x'] + particle['dx'] * (20 - particle['life']))
                py = int(splash['y'] + particle['dy'] * (20 - particle['life']))
                
                if 0 <= px < self.width and 0 <= py < self.height:
                    # Fading splash particles
                    fade = particle['life'] / 20.0
                    r, g, b = particle['color']
                    splash_color = (
                        int(r * fade),
                        int(g * fade),
                        int(b * fade)
                    )
                    image.putpixel((px, py), splash_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🌧️ Starting Raindrops...")
        print("   Realistic falling rain with splashes and puddles")
        print("   Press Ctrl+C to stop the rain")
        
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
                    total_drops = sum(len(s['drops']) for s in self.raindrop_streams)
                    active_splashes = len(self.splashes)
                    puddle_count = len(self.puddles)
                    print(f"🌧️ {elapsed:.1f}s: {total_drops} drops, {active_splashes} splashes, {puddle_count} puddles")
                
                time.sleep(0.05)  # 20 FPS for realistic motion
                
        except KeyboardInterrupt:
            print(f"\n🌧️ Rain stopped")
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
        screensaver = Raindrops()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()