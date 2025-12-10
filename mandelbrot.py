#!/usr/bin/env python3
"""
Mandelbrot Set - Classic Fractal
Animated Mandelbrot set with zooming and color cycling
"""

import LCD_1in44
import time
import random
import math
from PIL import Image

class MandelbrotSet:
    def __init__(self):
        print("🌀 Initializing Mandelbrot Set...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Mandelbrot parameters
        self.zoom = 1.0
        self.zoom_speed = 1.02
        self.center_x = -0.5
        self.center_y = 0.0
        self.max_iter = 30
        
        # Color palette
        self.colors = []
        for i in range(256):
            t = i / 255.0
            r = int(255 * (0.5 + 0.5 * math.sin(t * 6.28 + 0)))
            g = int(255 * (0.5 + 0.5 * math.sin(t * 6.28 + 2.09)))
            b = int(255 * (0.5 + 0.5 * math.sin(t * 6.28 + 4.18)))
            self.colors.append((r, g, b))
        
        self.color_offset = 0
        print(f"🌀 Mandelbrot set ready")
    
    def mandelbrot(self, c):
        """Calculate Mandelbrot iterations for complex number c"""
        z = 0
        for n in range(self.max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return self.max_iter
    
    def draw_frame(self):
        """Draw Mandelbrot set"""
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Calculate bounds
        aspect = self.width / self.height
        half_width = 2.0 / self.zoom
        half_height = half_width / aspect
        
        for y in range(self.height):
            for x in range(self.width):
                # Map pixel to complex plane
                real = self.center_x + (x - self.width/2) * half_width / (self.width/2)
                imag = self.center_y + (y - self.height/2) * half_height / (self.height/2)
                
                c = complex(real, imag)
                iterations = self.mandelbrot(c)
                
                if iterations == self.max_iter:
                    color = (0, 0, 0)  # Inside set = black
                else:
                    # Color based on iterations
                    color_index = (iterations + self.color_offset) % len(self.colors)
                    color = self.colors[color_index]
                
                image.putpixel((x, y), color)
        
        return image
    
    def update(self):
        """Update fractal parameters"""
        # Slow zoom into interesting areas
        self.zoom *= self.zoom_speed
        self.color_offset = (self.color_offset + 1) % len(self.colors)
        
        # Reset zoom and move to new area when too zoomed
        if self.zoom > 50:
            self.zoom = 1.0
            # Move to interesting Mandelbrot coordinates
            interesting_points = [
                (-0.5, 0.0),      # Main bulb
                (-0.75, 0.1),     # Edge detail
                (-0.235125, 0.827215),  # Spiral area
                (-0.8, 0.156),    # Tendril
                (-0.74529, 0.11307),  # Mini Mandelbrot
            ]
            self.center_x, self.center_y = random.choice(interesting_points)
    
    def run(self):
        """Main animation loop"""
        print("🌀 Starting Mandelbrot Set...")
        print("   Classic fractal with zooming animation")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                self.update()
                
                frame += 1
                
                if frame % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"🌀 {elapsed:.1f}s: zoom={self.zoom:.2f}, center=({self.center_x:.3f}, {self.center_y:.3f})")
                
                time.sleep(0.1)  # 10 FPS (fractal calculation is intensive)
                
        except KeyboardInterrupt:
            print(f"\n🌀 Mandelbrot set stopped")
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
        screensaver = MandelbrotSet()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()