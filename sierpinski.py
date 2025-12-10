#!/usr/bin/env python3
"""
Sierpinski Triangle - Recursive Fractal
Animated Sierpinski triangle with chaos game algorithm
"""

import LCD_1in44
import time
import random
import math
from PIL import Image

class SierpinskiTriangle:
    def __init__(self):
        print("🔺 Initializing Sierpinski Triangle...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Triangle vertices
        margin = 10
        self.vertices = [
            (self.width // 2, margin),                    # Top
            (margin, self.height - margin),               # Bottom left
            (self.width - margin, self.height - margin)   # Bottom right
        ]
        
        # Chaos game state
        self.current_point = (self.width // 2, self.height // 2)
        self.points = []
        self.max_points = 8000
        
        # Animation parameters
        self.rotation_angle = 0
        self.rotation_speed = 0.01
        self.color_time = 0
        
        # Colors
        self.sierpinski_colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (255, 100, 100),  # Light red
            (100, 255, 100),  # Light green
            (100, 100, 255),  # Light blue
        ]
        
        print(f"🔺 Sierpinski triangle ready")
    
    def rotate_point(self, point, center, angle):
        """Rotate a point around center by angle"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Translate to origin
        x = point[0] - center[0]
        y = point[1] - center[1]
        
        # Rotate
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        # Translate back
        return (new_x + center[0], new_y + center[1])
    
    def chaos_game_step(self):
        """Perform one step of the chaos game algorithm"""
        # Choose random vertex
        vertex = random.choice(self.vertices)
        
        # Move halfway to the chosen vertex
        new_x = (self.current_point[0] + vertex[0]) / 2
        new_y = (self.current_point[1] + vertex[1]) / 2
        
        self.current_point = (new_x, new_y)
        
        # Add point to collection with color info
        point_data = {
            'x': int(new_x),
            'y': int(new_y),
            'age': 0,
            'vertex_index': self.vertices.index(vertex)
        }
        
        self.points.append(point_data)
        
        # Remove old points
        if len(self.points) > self.max_points:
            self.points.pop(0)
    
    def update(self):
        """Update fractal generation and animation"""
        # Generate multiple points per frame for faster filling
        for _ in range(50):
            self.chaos_game_step()
        
        # Age all points
        for point in self.points:
            point['age'] += 1
        
        # Update animation parameters
        self.rotation_angle += self.rotation_speed
        self.color_time += 0.02
        
        # Rotate vertices slowly
        center = (self.width // 2, self.height // 2)
        if hasattr(self, 'original_vertices'):
            self.vertices = [
                self.rotate_point(v, center, self.rotation_angle) 
                for v in self.original_vertices
            ]
        else:
            self.original_vertices = self.vertices.copy()
    
    def draw_frame(self):
        """Draw Sierpinski triangle"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 20))
        
        # Draw triangle vertices
        for i, vertex in enumerate(self.vertices):
            x, y = int(vertex[0]), int(vertex[1])
            if 0 <= x < self.width and 0 <= y < self.height:
                vertex_color = self.sierpinski_colors[i % len(self.sierpinski_colors)]
                
                # Draw vertex as small circle
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if dx*dx + dy*dy <= 4:
                            px, py = x + dx, y + dy
                            if 0 <= px < self.width and 0 <= py < self.height:
                                image.putpixel((px, py), vertex_color)
        
        # Draw generated points
        for point in self.points:
            x, y = point['x'], point['y']
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Color based on which vertex was chosen and age
                vertex_index = point['vertex_index']
                base_color = self.sierpinski_colors[vertex_index]
                
                # Fade with age
                age_factor = max(0.1, 1.0 - point['age'] / 200.0)
                
                # Add time-based color variation
                color_shift = math.sin(self.color_time + vertex_index) * 0.3
                
                r, g, b = base_color
                final_color = (
                    int(r * age_factor * (1 + color_shift)),
                    int(g * age_factor * (1 + color_shift)),
                    int(b * age_factor * (1 + color_shift))
                )
                
                # Clamp values
                final_color = (
                    max(0, min(255, final_color[0])),
                    max(0, min(255, final_color[1])),
                    max(0, min(255, final_color[2]))
                )
                
                image.putpixel((x, y), final_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔺 Starting Sierpinski Triangle...")
        print("   Fractal generation using chaos game algorithm")
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
                    point_count = len(self.points)
                    print(f"🔺 {elapsed:.1f}s: {point_count} points generated")
                
                time.sleep(0.03)  # ~33 FPS
                
        except KeyboardInterrupt:
            print(f"\n🔺 Sierpinski triangle stopped")
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
        screensaver = SierpinskiTriangle()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()