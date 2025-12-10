#!/usr/bin/env python3
"""
Neon Rain - Tiny Shapes
Very small neon green shapes with blue accents falling densely
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class NeonRain:
    def __init__(self):
        print("💚 Initializing Neon Rain...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Tiny symbols and shapes - very small
        self.tiny_shapes = [
            '·', '•', '▪', '▫', '○', '●', '◦', '◯', '⋅', '∘', '∙',
            '▸', '▾', '▴', '▂', '▃', '▄', '▅', '▆', '▇', '█',
            '░', '▒', '▓', '┼', '┤', '├', '┴', '┬', '│', '─',
            '┌', '┐', '└', '┘', '╭', '╮', '╯', '╰', '╱', '╲',
            '⬢', '⬡', '⬠', '⬟', '⬞', '⬝', '◆', '◇', '◈', '◉'
        ]
        
        # Create very dense falling streams - tiny spacing
        self.streams = []
        stream_spacing = 3  # Very tight spacing for dense effect
        for x in range(0, self.width, stream_spacing):
            self.streams.append({
                'x': x,
                'particles': [],
                'spawn_timer': random.randint(0, 10),
                'color_bias': random.choice(['green', 'blue', 'mixed'])
            })
        
        print(f"💚 Created {len(self.streams)} neon streams")
    
    def get_neon_color(self, stream_bias, brightness):
        """Get neon green or blue color"""
        fade_factor = brightness / 255.0
        
        if stream_bias == 'green' or (stream_bias == 'mixed' and random.random() < 0.7):
            # Neon green variants
            base_colors = [
                (0, 255, 0),      # Pure neon green
                (50, 255, 50),    # Bright green
                (0, 255, 100),    # Green-cyan
                (100, 255, 0),    # Yellow-green
                (0, 200, 0),      # Deep green
            ]
        else:
            # Neon blue variants
            base_colors = [
                (0, 100, 255),    # Neon blue
                (0, 150, 255),    # Bright blue
                (50, 200, 255),   # Cyan-blue
                (0, 255, 255),    # Pure cyan
                (100, 150, 255),  # Purple-blue
            ]
        
        r, g, b = random.choice(base_colors)
        
        # Apply brightness fade
        return (
            int(r * fade_factor),
            int(g * fade_factor),
            int(b * fade_factor)
        )
    
    def update(self):
        """Update falling particles"""
        for stream in self.streams:
            # Spawn new particles frequently for dense effect
            if stream['spawn_timer'] <= 0:
                stream['particles'].append({
                    'shape': random.choice(self.tiny_shapes),
                    'y': random.uniform(-5, -1),
                    'brightness': 255,
                    'speed': random.uniform(0.5, 2.5),
                    'size_var': random.uniform(0.8, 1.2)  # Slight size variation
                })
                stream['spawn_timer'] = random.randint(3, 12)  # Very frequent
            else:
                stream['spawn_timer'] -= 1
            
            # Update existing particles
            for particle in stream['particles'][:]:
                particle['y'] += particle['speed']
                particle['brightness'] = max(0, particle['brightness'] - 4)
                
                # Remove particles that are off screen or faded
                if particle['y'] > self.height + 5 or particle['brightness'] <= 0:
                    stream['particles'].remove(particle)
    
    def draw_frame(self):
        """Draw the current frame"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Use smallest possible font or create pixel-level shapes
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw all particles
        for stream in self.streams:
            for particle in stream['particles']:
                if 0 <= particle['y'] <= self.height:
                    # Get neon color
                    color = self.get_neon_color(stream['color_bias'], particle['brightness'])
                    
                    x = stream['x']
                    y = int(particle['y'])
                    
                    # For very tiny effect, sometimes just draw pixels instead of text
                    if random.random() < 0.3:  # 30% chance for pixel dots
                        # Draw tiny pixel cluster (1-2 pixels)
                        size = int(particle['size_var'])
                        for px in range(size):
                            for py in range(size):
                                if x + px < self.width and y + py < self.height:
                                    image.putpixel((x + px, y + py), color)
                    else:
                        # Draw tiny shape
                        try:
                            draw.text((x, y), particle['shape'], fill=color, font=font)
                        except:
                            # Fallback to pixel
                            if x < self.width and y < self.height:
                                image.putpixel((x, y), color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("💚 Starting Neon Rain...")
        print("   Tiny neon shapes falling like digital rain")
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
                    total_particles = sum(len(s['particles']) for s in self.streams)
                    print(f"💚 {elapsed:.1f}s: {total_particles} neon particles falling")
                
                time.sleep(0.03)  # ~33 FPS for smooth neon effect
                
        except KeyboardInterrupt:
            print(f"\n💚 Neon rain stopped")
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
        screensaver = NeonRain()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()