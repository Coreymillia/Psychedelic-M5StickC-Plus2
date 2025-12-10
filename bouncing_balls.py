#!/usr/bin/env python3
"""
Bouncing Balls - Classic 1990s Bouncing Ball Screensaver
Colorful balls bouncing around the screen with trails
"""

import LCD_1in44
import time
import random
import math
from PIL import Image, ImageDraw

class BouncingBalls:
    def __init__(self):
        print("⚽ Initializing Bouncing Balls...")
        
        # Initialize LCD
        self.LCD = LCD_1in44.LCD()
        print("**********Init LCD**********")
        Lcd_ScanDir = LCD_1in44.U2D_L2R
        self.LCD.LCD_Init(Lcd_ScanDir)
        self.LCD.LCD_Clear()
        print("✅ LCD initialized successfully!")
        
        self.width = self.LCD.width
        self.height = self.LCD.height
        
        # Classic neon colors
        self.ball_colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
            (255, 0, 128),    # Hot pink
            (0, 128, 255),    # Blue
            (128, 255, 0),    # Lime
            (255, 255, 255),  # White
        ]
        
        # Create bouncing balls
        self.balls = []
        self.num_balls = 8
        
        for _ in range(self.num_balls):
            self.balls.append(self.create_ball())
        
        # Trail system for retro effect
        self.trails = []
        self.max_trail_length = 15
        
        print(f"⚽ Created {self.num_balls} bouncing balls")
    
    def create_ball(self):
        """Create a bouncing ball"""
        return {
            'x': random.uniform(10, self.width - 10),
            'y': random.uniform(10, self.height - 10),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-3, 3),
            'radius': random.randint(3, 8),
            'color': random.choice(self.ball_colors),
            'trail': [],
            'bounce_count': 0,
            'glow_phase': random.uniform(0, 2 * math.pi)
        }
    
    def update_balls(self):
        """Update ball positions and handle bouncing"""
        for ball in self.balls:
            # Store previous position for trail
            ball['trail'].append((int(ball['x']), int(ball['y'])))
            if len(ball['trail']) > self.max_trail_length:
                ball['trail'].pop(0)
            
            # Update position
            ball['x'] += ball['vx']
            ball['y'] += ball['vy']
            
            # Bounce off walls
            if ball['x'] - ball['radius'] <= 0:
                ball['x'] = ball['radius']
                ball['vx'] = abs(ball['vx'])
                ball['bounce_count'] += 1
                self.create_bounce_effect(ball)
                
            elif ball['x'] + ball['radius'] >= self.width:
                ball['x'] = self.width - ball['radius']
                ball['vx'] = -abs(ball['vx'])
                ball['bounce_count'] += 1
                self.create_bounce_effect(ball)
            
            if ball['y'] - ball['radius'] <= 0:
                ball['y'] = ball['radius']
                ball['vy'] = abs(ball['vy'])
                ball['bounce_count'] += 1
                self.create_bounce_effect(ball)
                
            elif ball['y'] + ball['radius'] >= self.height:
                ball['y'] = self.height - ball['radius']
                ball['vy'] = -abs(ball['vy'])
                ball['bounce_count'] += 1
                self.create_bounce_effect(ball)
            
            # Update glow phase
            ball['glow_phase'] += 0.1
            
            # Occasionally change color after many bounces
            if ball['bounce_count'] > 0 and ball['bounce_count'] % 20 == 0:
                ball['color'] = random.choice(self.ball_colors)
                ball['bounce_count'] = 0
    
    def create_bounce_effect(self, ball):
        """Create visual effect when ball bounces"""
        # Add some sparkle particles
        for _ in range(3):
            sparkle = {
                'x': ball['x'] + random.uniform(-5, 5),
                'y': ball['y'] + random.uniform(-5, 5),
                'life': 10,
                'color': ball['color']
            }
            self.trails.append(sparkle)
    
    def update_effects(self):
        """Update trail and sparkle effects"""
        # Update sparkles
        for effect in self.trails[:]:
            effect['life'] -= 1
            if effect['life'] <= 0:
                self.trails.remove(effect)
    
    def draw_frame(self):
        """Draw the bouncing balls with trails"""
        # Classic black background
        image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw ball trails
        for ball in self.balls:
            for i, (tx, ty) in enumerate(ball['trail']):
                if i > 0:
                    # Fade trail
                    fade = i / len(ball['trail'])
                    r, g, b = ball['color']
                    trail_color = (
                        int(r * fade * 0.5),
                        int(g * fade * 0.5),
                        int(b * fade * 0.5)
                    )
                    
                    # Draw trail segment
                    trail_size = max(1, int(ball['radius'] * fade * 0.7))
                    draw.ellipse([
                        tx - trail_size, ty - trail_size,
                        tx + trail_size, ty + trail_size
                    ], fill=trail_color)
        
        # Draw sparkle effects
        for effect in self.trails:
            fade = effect['life'] / 10.0
            r, g, b = effect['color']
            sparkle_color = (
                int(r * fade),
                int(g * fade),
                int(b * fade)
            )
            
            # Draw small sparkle
            sx, sy = int(effect['x']), int(effect['y'])
            if 0 <= sx < self.width and 0 <= sy < self.height:
                image.putpixel((sx, sy), sparkle_color)
                # Add + shape
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    px, py = sx + dx, sy + dy
                    if 0 <= px < self.width and 0 <= py < self.height:
                        image.putpixel((px, py), sparkle_color)
        
        # Draw balls with glow effect
        for ball in self.balls:
            x, y = int(ball['x']), int(ball['y'])
            radius = ball['radius']
            
            # Pulsing glow
            glow_intensity = 0.5 + 0.5 * math.sin(ball['glow_phase'])
            
            # Draw outer glow
            for glow_r in range(radius + 3, radius, -1):
                glow_fade = (radius + 3 - glow_r) / 3.0 * glow_intensity
                r, g, b = ball['color']
                glow_color = (
                    int(r * glow_fade * 0.3),
                    int(g * glow_fade * 0.3),
                    int(b * glow_fade * 0.3)
                )
                
                if glow_color != (0, 0, 0):
                    draw.ellipse([
                        x - glow_r, y - glow_r,
                        x + glow_r, y + glow_r
                    ], outline=glow_color)
            
            # Draw main ball
            draw.ellipse([
                x - radius, y - radius,
                x + radius, y + radius
            ], fill=ball['color'], outline=(255, 255, 255))
            
            # Add highlight for 3D effect
            highlight_x = x - radius // 3
            highlight_y = y - radius // 3
            highlight_size = max(1, radius // 3)
            
            r, g, b = ball['color']
            highlight_color = (
                min(255, r + 100),
                min(255, g + 100),
                min(255, b + 100)
            )
            
            draw.ellipse([
                highlight_x - highlight_size, highlight_y - highlight_size,
                highlight_x + highlight_size, highlight_y + highlight_size
            ], fill=highlight_color)
        
        return image
    
    def run(self):
        """Main animation loop"""
        print("⚽ Starting Bouncing Balls...")
        print("   Classic bouncing balls with trails and glow effects")
        print("   Press Ctrl+C to stop")
        
        frame = 0
        start_time = time.time()
        
        try:
            while True:
                self.update_balls()
                self.update_effects()
                image = self.draw_frame()
                self.LCD.LCD_ShowImage(image, 0, 0)
                
                frame += 1
                
                # Status update
                if frame % 400 == 0:
                    elapsed = time.time() - start_time
                    total_bounces = sum(ball['bounce_count'] for ball in self.balls)
                    print(f"⚽ {elapsed:.1f}s: {total_bounces} total bounces")
                
                time.sleep(0.05)  # 20 FPS
                
        except KeyboardInterrupt:
            print(f"\n⚽ Bouncing balls stopped")
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
        screensaver = BouncingBalls()
        screensaver.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()