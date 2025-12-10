#!/usr/bin/env python3
"""
Retro Geometry - 1990s Style Geometric Screensaver
Classic geometric shapes with retro colors and animations
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class RetroGeometry:
    def __init__(self):
        print("📺 Initializing Retro Geometry...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Classic 1990s color palette
        self.retro_colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
            (255, 0, 128),    # Hot pink
            (0, 128, 255),    # Blue
            (128, 255, 0),    # Lime
            (255, 128, 128),  # Light red
            (128, 255, 255),  # Light cyan
            (255, 255, 128),  # Light yellow
        ]
        
        # Geometric shapes
        self.shapes = []
        self.max_shapes = 15
        
        # Animation time
        self.time = 0
        
        print(f"📺 Retro geometry initialized")
    
    def create_random_shape(self):
        """Create a random geometric shape"""
        shape_type = random.choice(['circle', 'rectangle', 'triangle', 'line', 'polygon'])
        color = random.choice(self.retro_colors)
        
        # Random position
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        
        # Random size
        size = random.randint(5, 30)
        
        shape = {
            'type': shape_type,
            'x': x,
            'y': y,
            'size': size,
            'color': color,
            'angle': random.uniform(0, 2 * math.pi),
            'speed': random.uniform(0.5, 3.0),
            'rotation_speed': random.uniform(-0.1, 0.1),
            'direction': random.uniform(0, 2 * math.pi),
            'life': random.randint(100, 400),
            'max_life': random.randint(100, 400),
            'pulse_speed': random.uniform(0.05, 0.2),
            'width': random.randint(5, 25),
            'height': random.randint(5, 25)
        }
        
        return shape
    
    def update_shapes(self):
        """Update all geometric shapes"""
        self.time += 1
        
        # Remove old shapes
        self.shapes = [s for s in self.shapes if s['life'] > 0]
        
        # Add new shapes
        if len(self.shapes) < self.max_shapes and random.random() < 0.1:
            self.shapes.append(self.create_random_shape())
        
        # Update existing shapes
        for shape in self.shapes:
            # Move shape
            shape['x'] += math.cos(shape['direction']) * shape['speed']
            shape['y'] += math.sin(shape['direction']) * shape['speed']
            
            # Rotate
            shape['angle'] += shape['rotation_speed']
            
            # Bounce off edges
            if shape['x'] < 0 or shape['x'] > self.width:
                shape['direction'] = math.pi - shape['direction']
                shape['x'] = max(0, min(self.width, shape['x']))
            
            if shape['y'] < 0 or shape['y'] > self.height:
                shape['direction'] = -shape['direction']
                shape['y'] = max(0, min(self.height, shape['y']))
            
            # Pulse size
            pulse = 1.0 + 0.3 * math.sin(self.time * shape['pulse_speed'])
            shape['current_size'] = shape['size'] * pulse
            
            # Age
            shape['life'] -= 1
            
            # Fade color as shape ages
            age_factor = shape['life'] / shape['max_life']
            r, g, b = shape['color']
            shape['current_color'] = (
                int(r * age_factor),
                int(g * age_factor),
                int(b * age_factor)
            )
    
    def draw_shape(self, draw, shape):
        """Draw a single geometric shape"""
        x, y = int(shape['x']), int(shape['y'])
        size = int(shape['current_size'])
        color = shape['current_color']
        angle = shape['angle']
        
        if shape['type'] == 'circle':
            # Draw circle
            draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], 
                        outline=color, width=2)
            
        elif shape['type'] == 'rectangle':
            # Draw rotated rectangle (simplified as axis-aligned)
            w, h = shape['width'], shape['height']
            draw.rectangle([x - w//2, y - h//2, x + w//2, y + h//2], 
                          outline=color, width=2)
            
        elif shape['type'] == 'triangle':
            # Draw triangle
            points = []
            for i in range(3):
                px = x + size * math.cos(angle + i * 2 * math.pi / 3)
                py = y + size * math.sin(angle + i * 2 * math.pi / 3)
                points.append((int(px), int(py)))
            
            try:
                draw.polygon(points, outline=color, width=2)
            except:
                # Fallback to lines
                for i in range(3):
                    p1 = points[i]
                    p2 = points[(i + 1) % 3]
                    draw.line([p1, p2], fill=color, width=2)
                    
        elif shape['type'] == 'line':
            # Draw rotating line
            x1 = x + size * math.cos(angle)
            y1 = y + size * math.sin(angle)
            x2 = x - size * math.cos(angle)
            y2 = y - size * math.sin(angle)
            draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=color, width=3)
            
        elif shape['type'] == 'polygon':
            # Draw pentagon
            sides = 5
            points = []
            for i in range(sides):
                px = x + size * math.cos(angle + i * 2 * math.pi / sides)
                py = y + size * math.sin(angle + i * 2 * math.pi / sides)
                points.append((int(px), int(py)))
            
            try:
                draw.polygon(points, outline=color, width=2)
            except:
                # Fallback to lines
                for i in range(sides):
                    p1 = points[i]
                    p2 = points[(i + 1) % sides]
                    draw.line([p1, p2], fill=color, width=1)
    
    def draw_frame(self):
        """Draw the current frame"""
        # Classic 1990s dark background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Add some retro grid lines occasionally
        if self.time % 200 < 50:  # Show grid periodically
            grid_color = (32, 32, 32)  # Dark gray
            spacing = 20
            
            # Vertical lines
            for x in range(0, self.width, spacing):
                draw.line([(x, 0), (x, self.height)], fill=grid_color, width=1)
            
            # Horizontal lines
            for y in range(0, self.height, spacing):
                draw.line([(0, y), (self.width, y)], fill=grid_color, width=1)
        
        # Draw all shapes
        for shape in self.shapes:
            self.draw_shape(draw, shape)
        
        # Add some retro scan lines effect
        if random.random() < 0.1:
            for y in range(0, self.height, 4):
                if random.random() < 0.3:
                    scan_color = (20, 20, 20)
                    draw.line([(0, y), (self.width, y)], fill=scan_color, width=1)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("📺 Starting Retro Geometry...")
        print("   Classic 1990s geometric shapes and colors")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update_shapes()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update
                if frame % 400 == 0:
                    elapsed = time.time() - start_time
                    active_shapes = len(self.shapes)
                    print(f"📺 {elapsed:.1f}s: {active_shapes} geometric shapes active")
                
                time.sleep(0.06)  # ~17 FPS for classic feel
                
        except KeyboardInterrupt:
            print(f"\n📺 Retro geometry stopped")
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
        screensaver = RetroGeometry()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()