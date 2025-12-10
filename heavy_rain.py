#!/usr/bin/env python3
"""
Heavy Rain - Intense Downpour Effect
Very heavy rainfall with intense splashing and rapid puddle formation
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class HeavyRain:
    def __init__(self):
        print("⛈️ Initializing Heavy Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # HEAVY RAIN - Much denser streams
        self.raindrop_streams = []
        stream_spacing = 4  # Much tighter spacing for heavy rain
        for x in range(0, self.width, stream_spacing):
            self.raindrop_streams.append({
                'x': x,
                'drops': [],
                'spawn_timer': random.randint(0, 15),  # Much shorter delays
                'wind_offset': random.uniform(-3, 3),  # Stronger wind
                'intensity': random.uniform(0.8, 1.5)  # Variable intensity per stream
            })
        
        # Puddles form faster and bigger in heavy rain
        self.puddles = {}
        
        # More intense splash effects
        self.splashes = []
        
        # Stormy water colors - darker, more dramatic
        self.storm_colors = [
            (160, 200, 220),  # Storm blue
            (140, 180, 210),  # Dark sky blue
            (120, 160, 200),  # Stormy blue
            (200, 220, 240),  # Heavy rain white
            (180, 200, 220),  # Storm gray-blue
            (220, 230, 245),  # Bright rain white
        ]
        
        # Background gets darker in heavy rain
        self.storm_background = (15, 15, 25)  # Very dark stormy sky
        
        print(f"⛈️ Created {len(self.raindrop_streams)} heavy rain streams")
    
    def create_heavy_raindrop(self, stream):
        """Create a heavy raindrop - bigger and faster"""
        # Heavy rain has more large drops
        size_weights = ['small'] * 2 + ['medium'] * 4 + ['large'] * 4
        
        return {
            'y': random.uniform(-8, -3),
            'size': random.choice(size_weights),
            'color': random.choice(self.storm_colors),
            'speed': random.uniform(3.0, 7.0) * stream['intensity'],  # Much faster
            'brightness': random.randint(200, 255),
            'wind_drift': stream['wind_offset'] * random.uniform(0.8, 2.0),
            'trail_length': random.randint(5, 12)  # Longer trails
        }
    
    def create_heavy_splash(self, x, y, intensity):
        """Create intense splash effect"""
        splash = {
            'x': x,
            'y': y,
            'particles': [],
            'life': 30,  # Longer lasting splashes
            'intensity': intensity * 2  # Double intensity
        }
        
        # Create more splash particles
        for i in range(intensity * 3):  # Triple the particles
            angle = random.uniform(0, 3.14159)
            speed = random.uniform(2, 5)  # Faster splash particles
            splash['particles'].append({
                'dx': speed * random.uniform(-1.5, 1.5),
                'dy': -speed * random.uniform(1, 3),  # Higher splash
                'life': random.randint(15, 35),
                'size': random.choice(['tiny', 'small', 'medium']),
                'color': random.choice(self.storm_colors)
            })
        
        self.splashes.append(splash)
    
    def update_heavy_puddles(self, x):
        """Puddles form much faster in heavy rain"""
        if x not in self.puddles:
            self.puddles[x] = 0
        
        # Rapid accumulation in heavy rain
        self.puddles[x] = min(self.puddles[x] + 1.5, 15)  # Bigger puddles
        
        # Slower evaporation due to constant heavy rain
        for px in list(self.puddles.keys()):
            self.puddles[px] = max(0, self.puddles[px] - 0.01)
            if self.puddles[px] <= 0:
                del self.puddles[px]
    
    def update(self):
        """Update heavy rain and effects"""
        # Update raindrop streams
        for stream in self.raindrop_streams:
            # Spawn raindrops very frequently
            if stream['spawn_timer'] <= 0:
                if random.random() < 0.9:  # 90% chance - very frequent
                    stream['drops'].append(self.create_heavy_raindrop(stream))
                    
                    # Sometimes spawn multiple drops at once
                    if random.random() < 0.4:
                        stream['drops'].append(self.create_heavy_raindrop(stream))
                
                stream['spawn_timer'] = random.randint(3, 15)  # Very short delays
            else:
                stream['spawn_timer'] -= 1
            
            # Update existing drops
            for drop in stream['drops'][:]:
                drop['y'] += drop['speed']
                
                # Apply stronger wind drift
                drop['x_offset'] = getattr(drop, 'x_offset', 0) + drop['wind_drift'] * 0.15
                
                # Check collision with puddles
                puddle_height = self.puddles.get(stream['x'], 0)
                hit_surface = drop['y'] >= self.height - 1 - puddle_height
                
                if hit_surface:
                    # Create intense splash
                    splash_intensity = {'small': 4, 'medium': 7, 'large': 10}[drop['size']]
                    self.create_heavy_splash(stream['x'], drop['y'], splash_intensity)
                    
                    # Rapid puddle formation
                    self.update_heavy_puddles(stream['x'])
                    
                    # Remove drop
                    stream['drops'].remove(drop)
                elif drop['y'] > self.height + 10:
                    stream['drops'].remove(drop)
        
        # Update splashes
        for splash in self.splashes[:]:
            splash['life'] -= 1
            
            for particle in splash['particles'][:]:
                particle['life'] -= 1
                particle['dy'] += 0.25  # Stronger gravity
                
                if particle['life'] <= 0:
                    splash['particles'].remove(particle)
            
            if splash['life'] <= 0 or not splash['particles']:
                self.splashes.remove(splash)
    
    def draw_frame(self):
        """Draw heavy rain and storm effects"""
        # Darker stormy background
        image = Image.new('RGB', (self.width, self.height), self.storm_background)
        draw = ImageDraw.Draw(image)
        
        # Draw larger puddles
        for x, height in self.puddles.items():
            if height > 0:
                # Draw bigger puddles with ripple effect
                puddle_color = (80, 120, 160)  # Darker puddle blue
                for h in range(int(height)):
                    y = self.height - 1 - h
                    if 0 <= y < self.height:
                        # Wider puddles
                        puddle_width = min(6, int(height / 2) + 2)
                        for px in range(max(0, x - puddle_width), min(self.width, x + puddle_width + 1)):
                            # Add ripple effect
                            ripple_intensity = 1.0 - abs(px - x) / puddle_width
                            r, g, b = puddle_color
                            ripple_color = (
                                int(r * ripple_intensity),
                                int(g * ripple_intensity),
                                int(b * ripple_intensity)
                            )
                            image.putpixel((px, y), ripple_color)
        
        # Draw heavy raindrops
        for stream in self.raindrop_streams:
            for drop in stream['drops']:
                if 0 <= drop['y'] <= self.height:
                    x = stream['x'] + int(getattr(drop, 'x_offset', 0))
                    y = int(drop['y'])
                    
                    # Ensure x is in bounds
                    x = max(0, min(self.width - 1, x))
                    
                    # Draw larger drops for heavy rain
                    if drop['size'] == 'large':
                        # Draw 4-5 pixel large drop
                        for dy in range(-2, 3):
                            for dx in range(-2, 3):
                                if abs(dx) + abs(dy) <= 2:  # Diamond shape
                                    px, py = x + dx, y + dy
                                    if 0 <= px < self.width and 0 <= py < self.height:
                                        image.putpixel((px, py), drop['color'])
                    elif drop['size'] == 'medium':
                        # Draw 3-pixel drop
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if abs(dx) + abs(dy) <= 1:
                                    px, py = x + dx, y + dy
                                    if 0 <= px < self.width and 0 <= py < self.height:
                                        image.putpixel((px, py), drop['color'])
                    else:  # small
                        # 2-pixel drop
                        for dy in range(2):
                            px, py = x, y + dy
                            if 0 <= px < self.width and 0 <= py < self.height:
                                image.putpixel((px, py), drop['color'])
                    
                    # Draw longer, more visible trails
                    trail_length = min(drop['trail_length'], int(drop['speed'] * 1.5))
                    for t in range(1, trail_length):
                        trail_y = y - t
                        if 0 <= trail_y < self.height:
                            fade = 1.0 - (t / trail_length)
                            r, g, b = drop['color']
                            trail_color = (
                                int(r * fade * 0.8),  # Brighter trails
                                int(g * fade * 0.8),
                                int(b * fade * 0.8)
                            )
                            if 0 <= x < self.width:
                                image.putpixel((x, trail_y), trail_color)
        
        # Draw intense splash effects
        for splash in self.splashes:
            for particle in splash['particles']:
                px = int(splash['x'] + particle['dx'] * (30 - particle['life']) * 0.5)
                py = int(splash['y'] + particle['dy'] * (30 - particle['life']) * 0.5)
                
                if 0 <= px < self.width and 0 <= py < self.height:
                    fade = particle['life'] / 30.0
                    r, g, b = particle['color']
                    splash_color = (
                        int(r * fade * 1.2),  # Brighter splashes
                        int(g * fade * 1.2),
                        int(b * fade * 1.2)
                    )
                    image.putpixel((px, py), splash_color)
                    
                    # Add extra splash pixels for medium/large particles
                    if particle['size'] in ['medium', 'large'] and fade > 0.5:
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            spx, spy = px + dx, py + dy
                            if 0 <= spx < self.width and 0 <= spy < self.height:
                                dimmer_color = (
                                    int(r * fade * 0.6),
                                    int(g * fade * 0.6),
                                    int(b * fade * 0.6)
                                )
                                image.putpixel((spx, spy), dimmer_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("⛈️ Starting Heavy Rain...")
        print("   Intense downpour with heavy splashing and flooding")
        print("   Press Ctrl+C to stop the storm")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update
                if frame % 300 == 0:
                    elapsed = time.time() - start_time
                    total_drops = sum(len(s['drops']) for s in self.raindrop_streams)
                    active_splashes = len(self.splashes)
                    puddle_count = len(self.puddles)
                    avg_puddle_depth = sum(self.puddles.values()) / max(1, len(self.puddles))
                    print(f"⛈️ {elapsed:.1f}s: {total_drops} drops, {active_splashes} splashes, "
                          f"{puddle_count} puddles (avg depth: {avg_puddle_depth:.1f})")
                
                time.sleep(0.04)  # 25 FPS for intense motion
                
        except KeyboardInterrupt:
            print(f"\n⛈️ Storm passed")
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
        screensaver = HeavyRain()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()