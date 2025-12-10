#!/usr/bin/env python3
"""
Dragon Curve - L-System Fractal
Animated Heighway dragon curve with growing iterations
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class DragonCurve:
    def __init__(self):
        print("🐉 Initializing Dragon Curve...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Dragon curve parameters
        self.max_iterations = 14
        self.current_iteration = 1
        self.line_length = 2
        self.angle = 0  # Current direction angle
        
        # Animation parameters
        self.growth_timer = 0
        self.growth_delay = 100  # Frames between iterations
        self.rotation_offset = 0
        self.color_time = 0
        
        # Dragon colors
        self.dragon_colors = [
            (255, 0, 0),      # Red
            (255, 128, 0),    # Orange
            (255, 255, 0),    # Yellow
            (128, 255, 0),    # Lime
            (0, 255, 0),      # Green
            (0, 255, 128),    # Cyan-green
            (0, 255, 255),    # Cyan
            (0, 128, 255),    # Blue
            (128, 0, 255),    # Purple
            (255, 0, 255),    # Magenta
        ]
        
        print(f"🐉 Dragon curve ready")
    
    def generate_dragon_string(self, iterations):
        """Generate L-system string for dragon curve"""
        if iterations == 0:
            return "F"
        
        # Start with initial axiom
        current = "F"
        
        # Apply rules for each iteration
        for _ in range(iterations):
            new_string = ""
            for char in current:
                if char == "F":
                    new_string += "F+F--F+F"
                else:
                    new_string += char
            current = new_string
        
        return current
    
    def draw_dragon_curve(self, dragon_string, start_x, start_y, angle_offset):
        """Draw dragon curve from L-system string"""
        points = []
        
        # Starting position and angle
        x, y = start_x, start_y
        angle = angle_offset
        
        # Track all points for the path
        points.append((int(x), int(y)))
        
        for char in dragon_string:
            if char == "F":
                # Move forward
                new_x = x + self.line_length * math.cos(math.radians(angle))
                new_y = y + self.line_length * math.sin(math.radians(angle))
                
                points.append((int(new_x), int(new_y)))
                x, y = new_x, new_y
                
            elif char == "+":
                # Turn right 90 degrees
                angle += 90
            elif char == "-":
                # Turn left 90 degrees
                angle -= 90
        
        return points
    
    def draw_frame(self):
        """Draw dragon curve"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 10))
        draw = ImageDraw.Draw(image)
        
        # Generate dragon curve for current iteration
        dragon_string = self.generate_dragon_string(self.current_iteration)
        
        # Calculate starting position to center the curve
        start_x = self.width // 2
        start_y = self.height // 2
        
        # Get all points of the dragon curve
        points = self.draw_dragon_curve(dragon_string, start_x, start_y, self.rotation_offset)
        
        # Draw the dragon curve
        if len(points) > 1:
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Skip if points are off screen
                if (not (0 <= x1 < self.width and 0 <= y1 < self.height) and
                    not (0 <= x2 < self.width and 0 <= y2 < self.height)):
                    continue
                
                # Color based on position along curve
                color_index = (i + int(self.color_time * 10)) % len(self.dragon_colors)
                color = self.dragon_colors[color_index]
                
                # Add some color variation
                color_var = 0.8 + 0.4 * math.sin(self.color_time + i * 0.1)
                r, g, b = color
                varied_color = (
                    int(r * color_var),
                    int(g * color_var),
                    int(b * color_var)
                )
                
                try:
                    draw.line([(x1, y1), (x2, y2)], fill=varied_color, width=1)
                except:
                    # Fallback to individual pixels if line drawing fails
                    if 0 <= x1 < self.width and 0 <= y1 < self.height:
                        image.putpixel((x1, y1), varied_color)
        
        return image
    
    def update(self):
        """Update dragon curve parameters"""
        self.growth_timer += 1
        self.color_time += 0.02
        self.rotation_offset += 0.5  # Slow rotation
        
        # Grow the dragon curve
        if self.growth_timer >= self.growth_delay:
            self.current_iteration += 1
            self.growth_timer = 0
            
            # Reset when reaching max iterations
            if self.current_iteration > self.max_iterations:
                self.current_iteration = 1
                # Change colors or parameters for variety
                random.shuffle(self.dragon_colors)
                self.line_length = random.choice([1, 2, 3])
    
    def run(self):
        """Main animation loop"""
        print("🐉 Starting Dragon Curve...")
        print("   L-system fractal with growing complexity")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                if frame % 200 == 0:
                    elapsed = time.time() - start_time
                    print(f"🐉 {elapsed:.1f}s: iteration {self.current_iteration}/{self.max_iterations}")
                
                time.sleep(0.05)  # 20 FPS
                
        except KeyboardInterrupt:
            print(f"\n🐉 Dragon curve stopped")
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
        screensaver = DragonCurve()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()