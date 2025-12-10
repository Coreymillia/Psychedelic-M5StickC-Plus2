#!/usr/bin/env python3
"""
Kaleidoscope - Symmetrical Pattern Generator
Rotating kaleidoscope with mirrored patterns and colors
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class Kaleidoscope:
    def __init__(self):
        print("🔮 Initializing Kaleidoscope...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = min(self.width, self.height) // 2 - 5
        
        # Kaleidoscope parameters
        self.segments = 6  # Number of mirror segments
        self.rotation_angle = 0
        self.rotation_speed = 0.02
        
        # Pattern elements
        self.pattern_elements = []
        self.max_elements = 12
        
        # Kaleidoscope colors - vibrant and varied
        self.kaleido_colors = [
            (255, 0, 128),    # Hot pink
            (128, 0, 255),    # Purple
            (0, 128, 255),    # Blue
            (0, 255, 255),    # Cyan
            (0, 255, 128),    # Green-cyan
            (128, 255, 0),    # Lime
            (255, 255, 0),    # Yellow
            (255, 128, 0),    # Orange
            (255, 0, 0),      # Red
            (255, 0, 255),    # Magenta
            (128, 128, 255),  # Light purple
            (255, 128, 128),  # Light pink
        ]
        
        # Initialize pattern elements
        for _ in range(self.max_elements):
            self.pattern_elements.append(self.create_pattern_element())
        
        print(f"🔮 Kaleidoscope ready with {self.segments} segments")
    
    def create_pattern_element(self):
        """Create a pattern element for the kaleidoscope"""
        # Position in one segment (will be mirrored)
        angle = random.uniform(0, 2 * math.pi / self.segments)
        distance = random.uniform(5, self.radius * 0.8)
        
        return {
            'angle': angle,
            'distance': distance,
            'color': random.choice(self.kaleido_colors),
            'size': random.randint(2, 6),
            'shape': random.choice(['circle', 'square', 'diamond', 'star']),
            'rotation': random.uniform(0, 2 * math.pi),
            'rotation_speed': random.uniform(-0.1, 0.1),
            'pulse_phase': random.uniform(0, 2 * math.pi),
            'pulse_speed': random.uniform(0.05, 0.15),
            'life': random.randint(200, 600)
        }
    
    def update(self):
        """Update kaleidoscope rotation and elements"""
        # Rotate the whole kaleidoscope
        self.rotation_angle += self.rotation_speed
        
        # Update pattern elements
        for element in self.pattern_elements[:]:
            # Rotate individual elements
            element['rotation'] += element['rotation_speed']
            element['pulse_phase'] += element['pulse_speed']
            element['life'] -= 1
            
            # Slowly drift elements
            element['angle'] += random.uniform(-0.005, 0.005)
            element['distance'] += random.uniform(-0.2, 0.2)
            element['distance'] = max(5, min(self.radius * 0.8, element['distance']))
            
            # Remove old elements
            if element['life'] <= 0:
                self.pattern_elements.remove(element)
        
        # Add new elements to maintain count
        while len(self.pattern_elements) < self.max_elements:
            self.pattern_elements.append(self.create_pattern_element())
    
    def draw_shape(self, draw, x, y, element):
        """Draw a single shape at given coordinates"""
        size = element['size']
        pulse = 1.0 + 0.3 * math.sin(element['pulse_phase'])
        actual_size = int(size * pulse)
        color = element['color']
        shape = element['shape']
        rotation = element['rotation']
        
        # Ensure coordinates are in bounds
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        try:
            if shape == 'circle':
                draw.ellipse([
                    x - actual_size, y - actual_size,
                    x + actual_size, y + actual_size
                ], fill=color)
                
            elif shape == 'square':
                draw.rectangle([
                    x - actual_size, y - actual_size,
                    x + actual_size, y + actual_size
                ], fill=color)
                
            elif shape == 'diamond':
                # Diamond shape as polygon
                points = [
                    (x, y - actual_size),  # Top
                    (x + actual_size, y),  # Right
                    (x, y + actual_size),  # Bottom
                    (x - actual_size, y)   # Left
                ]
                draw.polygon(points, fill=color)
                
            elif shape == 'star':
                # Simple 4-pointed star
                star_points = []
                for i in range(8):
                    angle = rotation + i * math.pi / 4
                    if i % 2 == 0:
                        # Outer points
                        r = actual_size
                    else:
                        # Inner points
                        r = actual_size * 0.5
                    
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    star_points.append((int(px), int(py)))
                
                draw.polygon(star_points, fill=color)
                
        except Exception:
            # Fallback to simple pixel if drawing fails
            if 0 <= x < self.width and 0 <= y < self.height:
                pass  # Skip if we can't draw
    
    def get_mirrored_positions(self, angle, distance):
        """Get all mirrored positions for a point"""
        positions = []
        segment_angle = 2 * math.pi / self.segments
        
        for i in range(self.segments):
            # Calculate position in each segment
            seg_angle = self.rotation_angle + i * segment_angle + angle
            
            x = self.center_x + distance * math.cos(seg_angle)
            y = self.center_y + distance * math.sin(seg_angle)
            
            positions.append((int(x), int(y)))
            
            # Add mirror reflection within segment for true kaleidoscope effect
            mirror_angle = self.rotation_angle + i * segment_angle - angle
            mirror_x = self.center_x + distance * math.cos(mirror_angle)
            mirror_y = self.center_y + distance * math.sin(mirror_angle)
            
            positions.append((int(mirror_x), int(mirror_y)))
        
        return positions
    
    def draw_frame(self):
        """Draw kaleidoscope frame"""
        # Dark background
        image = Image.new('RGB', (self.width, self.height), (10, 10, 20))
        draw = ImageDraw.Draw(image)
        
        # Draw kaleidoscope boundary (optional)
        if random.random() < 0.1:  # Occasionally show boundary
            draw.ellipse([
                self.center_x - self.radius, self.center_y - self.radius,
                self.center_x + self.radius, self.center_y + self.radius
            ], outline=(50, 50, 50))
        
        # Draw pattern elements with symmetry
        for element in self.pattern_elements:
            # Get all mirrored positions
            positions = self.get_mirrored_positions(element['angle'], element['distance'])
            
            # Draw element at each mirrored position
            for x, y in positions:
                # Only draw if within the circular boundary
                dist_from_center = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
                if dist_from_center <= self.radius:
                    self.draw_shape(draw, x, y, element)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("🔮 Starting Kaleidoscope...")
        print("   Symmetrical patterns with rotating mirrors")
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
                    rotation_degrees = (self.rotation_angle * 180 / math.pi) % 360
                    element_count = len(self.pattern_elements)
                    print(f"🔮 {elapsed:.1f}s: {rotation_degrees:.1f}° rotation, {element_count} elements")
                
                time.sleep(0.06)  # ~17 FPS for smooth rotation
                
        except KeyboardInterrupt:
            print(f"\n🔮 Kaleidoscope stopped")
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
        screensaver = Kaleidoscope()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()