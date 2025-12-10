#!/usr/bin/env python3
"""
Campfire - Cozy Fire Effect
Simple campfire with flickering flames and warm colors
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class Campfire:
    def __init__(self):
        print("🏕️ Initializing Campfire...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Campfire base
        self.fire_base_y = self.height - 10
        
        # Flame tongues
        self.flame_tongues = []
        
        # Create several flame sources
        for i in range(5):
            x = 30 + i * 15  # Spread across middle of screen
            self.flame_tongues.append({
                'x': x,
                'base_height': random.randint(20, 40),
                'current_height': 0,
                'flicker_phase': random.uniform(0, 2 * math.pi),
                'flicker_speed': random.uniform(0.1, 0.3),
                'width': random.randint(8, 15)
            })
        
        # Simple fire colors
        self.campfire_colors = [
            (60, 0, 0),       # Dark ember
            (120, 0, 0),      # Deep red
            (180, 0, 0),      # Red
            (255, 50, 0),     # Red-orange
            (255, 100, 0),    # Orange
            (255, 150, 0),    # Light orange
            (255, 200, 50),   # Yellow-orange
            (255, 255, 100),  # Yellow
        ]
        
        self.time = 0
        print(f"🏕️ Campfire ready with {len(self.flame_tongues)} flame tongues")
    
    def update(self):
        """Update campfire flames"""
        self.time += 1
        
        # Update each flame tongue
        for tongue in self.flame_tongues:
            # Update flicker
            tongue['flicker_phase'] += tongue['flicker_speed']
            
            # Calculate current height with flicker
            flicker = 0.7 + 0.3 * math.sin(tongue['flicker_phase'])
            tongue['current_height'] = int(tongue['base_height'] * flicker)
    
    def draw_frame(self):
        """Draw campfire"""
        # Dark background
        image = Image.new('RGB', (self.width, self.height), (5, 5, 15))
        draw = ImageDraw.Draw(image)
        
        # Draw each flame tongue
        for tongue in self.flame_tongues:
            x = tongue['x']
            height = tongue['current_height']
            width = tongue['width']
            
            # Draw flame as a series of ellipses getting smaller toward top
            segments = height // 4
            
            for i in range(segments):
                y = self.fire_base_y - (i * 4)
                
                # Flame gets narrower toward top
                segment_width = width * (1.0 - i / segments * 0.7)
                segment_height = 6
                
                # Color gets lighter/yellower toward top
                color_index = min(len(self.campfire_colors) - 1, 
                                int((i / segments) * len(self.campfire_colors)))
                color = self.campfire_colors[color_index]
                
                # Add some random flicker to color
                r, g, b = color
                flicker_factor = 0.8 + 0.2 * random.random()
                final_color = (
                    int(r * flicker_factor),
                    int(g * flicker_factor),
                    int(b * flicker_factor)
                )
                
                # Draw flame segment
                if y > 0:
                    left = int(x - segment_width // 2)
                    right = int(x + segment_width // 2)
                    top = int(y - segment_height // 2)
                    bottom = int(y + segment_height // 2)
                    
                    try:
                        draw.ellipse([left, top, right, bottom], fill=final_color)
                    except:
                        # Fallback to rectangle if ellipse fails
                        draw.rectangle([left, top, right, bottom], fill=final_color)
        
        # Add some sparks/embers
        if random.random() < 0.1:  # 10% chance
            for _ in range(random.randint(1, 3)):
                spark_x = random.randint(20, self.width - 20)
                spark_y = random.randint(self.fire_base_y - 30, self.fire_base_y - 10)
                
                if 0 <= spark_x < self.width and 0 <= spark_y < self.height:
                    spark_color = random.choice([
                        (255, 100, 0),    # Orange spark
                        (255, 150, 50),   # Yellow spark
                        (255, 200, 100),  # Bright spark
                    ])
                    image.putpixel((spark_x, spark_y), spark_color)
        
        # Add warm glow at base
        glow_y = self.fire_base_y + 5
        for x in range(self.width):
            if glow_y < self.height:
                # Distance from center affects glow intensity
                center_x = self.width // 2
                dist = abs(x - center_x)
                max_dist = self.width // 2
                
                if dist < max_dist:
                    glow_intensity = 1.0 - (dist / max_dist)
                    glow_color = (
                        int(40 * glow_intensity),
                        int(10 * glow_intensity),
                        0
                    )
                    
                    # Blend with existing pixel
                    current = image.getpixel((x, glow_y))
                    new_color = (
                        min(255, current[0] + glow_color[0]),
                        min(255, current[1] + glow_color[1]),
                        min(255, current[2] + glow_color[2])
                    )
                    image.putpixel((x, glow_y), new_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🏕️ Starting Campfire...")
        print("   Cozy flickering campfire")
        print("   Press Ctrl+C to put out the fire")
        
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
                    print(f"🏕️ {elapsed:.1f}s: Campfire burning steadily")
                
                time.sleep(0.08)  # ~12 FPS for gentle flicker
                
        except KeyboardInterrupt:
            print(f"\n🏕️ Campfire extinguished")
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
        screensaver = Campfire()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()