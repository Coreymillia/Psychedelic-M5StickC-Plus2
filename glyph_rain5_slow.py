#!/usr/bin/env python3
"""
Glyph Rain 5 - Slow Accumulator
Very slow, subtle accumulation like dust settling over many hours
Perfect for all-day visual timer
"""

import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont

class SlowAccumulator:
    def __init__(self):
        print("🕰️ Initializing Slow Accumulator...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Very tiny characters and dots
        self.glyphs = ['·', '•', '▪', '▫', '○', '●', '◦', '◯', '⋅', '∘', '∙', '∴', '∵']
        self.rare_chars = ['☆', '★', '◇', '◆', '△', '▲', '♦']
        
        # Storage for settled particles
        self.settled = {}
        self.falling = []
        
        self.start_time = time.time()
        self.frame_count = 0
        
        print(f"🕰️ Slow accumulator ready - will build up very gradually")
    
    def get_subtle_color(self, elapsed_hours):
        """Very subtle color changes over time"""
        # Slow color progression through the day
        progress = (elapsed_hours / 24.0) % 1.0  # 0-1 over 24 hours
        
        if progress < 0.25:  # Dawn: purples to blues
            r = int(100 + progress * 4 * 50)
            g = int(50 + progress * 4 * 100)
            b = int(150 + progress * 4 * 100)
        elif progress < 0.5:  # Day: blues to greens
            p = (progress - 0.25) * 4
            r = int(150 - p * 100)
            g = int(150 + p * 50)
            b = int(250 - p * 100)
        elif progress < 0.75:  # Evening: greens to oranges
            p = (progress - 0.5) * 4
            r = int(50 + p * 150)
            g = int(200 - p * 50)
            b = int(150 - p * 100)
        else:  # Night: oranges to purples
            p = (progress - 0.75) * 4
            r = int(200 - p * 100)
            g = int(150 - p * 100)
            b = int(50 + p * 100)
        
        return (r, g, b)
    
    def update(self):
        """Very slow, subtle updates"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        elapsed_hours = elapsed_time / 3600
        
        # Very low spawn rate - only occasionally
        spawn_chance = 0.05 + (elapsed_hours * 0.01)  # Starts at 5%, slowly increases
        
        if random.random() < spawn_chance:
            # Occasionally spawn a rare character
            if random.random() < 0.1:
                char = random.choice(self.rare_chars)
            else:
                char = random.choice(self.glyphs)
            
            self.falling.append({
                'char': char,
                'x': random.randint(0, self.width - 4),
                'y': random.randint(-30, -5),
                'speed': random.uniform(0.1, 0.8),  # Very slow
                'color': self.get_subtle_color(elapsed_hours),
                'birth_time': elapsed_time
            })
        
        # Update falling particles
        for particle in self.falling[:]:
            particle['y'] += particle['speed']
            
            # Find where it should settle
            settle_y = self.height - 1
            for y in range(int(particle['y']), self.height):
                if (int(particle['x']), y) in self.settled:
                    settle_y = y - 1
                    break
            
            # Settle the particle
            if particle['y'] >= settle_y:
                if settle_y >= 0:
                    self.settled[(int(particle['x']), settle_y)] = {
                        'char': particle['char'],
                        'color': particle['color'],
                        'settle_time': elapsed_time,
                        'birth_time': particle['birth_time']
                    }
                self.falling.remove(particle)
            elif particle['y'] > self.height + 20:
                self.falling.remove(particle)
    
    def draw_frame(self):
        """Draw the current frame"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        current_time = time.time() - self.start_time
        
        # Draw settled particles with aging
        for (x, y), particle in self.settled.items():
            age = current_time - particle['settle_time']
            age_hours = age / 3600
            
            # Very subtle aging - particles dim very slowly
            age_factor = min(age_hours / 12.0, 0.5)  # Half brightness after 12 hours
            
            color = particle['color']
            aged_color = (
                int(color[0] * (1.0 - age_factor)),
                int(color[1] * (1.0 - age_factor)),
                int(color[2] * (1.0 - age_factor))
            )
            
            # Add subtle brightness variation
            brightness_var = 0.8 + 0.4 * random.random()
            final_color = (
                int(aged_color[0] * brightness_var),
                int(aged_color[1] * brightness_var),
                int(aged_color[2] * brightness_var)
            )
            
            try:
                draw.text((x, y), particle['char'], fill=final_color, font=font)
            except:
                draw.text((x, y), '·', fill=final_color, font=font)
        
        # Draw falling particles
        for particle in self.falling:
            if 0 <= particle['y'] <= self.height:
                try:
                    draw.text((int(particle['x']), int(particle['y'])), 
                             particle['char'], fill=particle['color'], font=font)
                except:
                    draw.text((int(particle['x']), int(particle['y'])), 
                             '·', fill=particle['color'], font=font)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🕰️ Starting Slow Accumulator...")
        print("   Very gradual accumulation over many hours")
        print("   Perfect for all-day visual timer")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                # Status every hour
                if self.frame_count % 3600 == 0:  # ~1 hour at 1 FPS
                    elapsed_time = time.time() - self.start_time
                    elapsed_hours = elapsed_time / 3600
                    settled_count = len(self.settled)
                    falling_count = len(self.falling)
                    
                    if settled_count > 0:
                        max_height = self.height - min(y for x, y in self.settled.keys())
                    else:
                        max_height = 0
                    
                    print(f"🕰️ {elapsed_hours:.1f}h: {settled_count} settled, "
                          f"{falling_count} falling, height: {max_height}")
                
                time.sleep(1.0)  # 1 FPS for very slow effect
                
        except KeyboardInterrupt:
            elapsed_time = time.time() - self.start_time
            settled_count = len(self.settled)
            print(f"\n🛑 Slow accumulator stopped after {elapsed_time/3600:.2f} hours")
            print(f"📊 Total particles settled: {settled_count}")
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
        screensaver = SlowAccumulator()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()