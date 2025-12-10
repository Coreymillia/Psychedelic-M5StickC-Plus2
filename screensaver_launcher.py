#!/usr/bin/env python3
"""
Waveshare 1.44" LCD HAT Screensavers
A collection of 22 animated screensavers for the Waveshare 1.44" LCD HAT

Usage:
    python3 screensaver_launcher.py                    # Show menu
    python3 screensaver_launcher.py random             # Run random screensaver
    python3 screensaver_launcher.py <screensaver_name> # Run specific screensaver
    python3 screensaver_launcher.py list               # List all screensavers
"""

import sys
import random
import time
import subprocess
import os

class ScreensaverLauncher:
    def __init__(self):
        self.screensavers = {
            # Matrix/Rain Effects
            'glyph_rain1': {
                'file': 'glyph_rain1.py',
                'name': 'Classic Matrix Rain',
                'description': 'Green falling characters in Matrix style',
                'category': 'Matrix/Rain'
            },
            'glyph_rain2': {
                'file': 'glyph_rain2.py', 
                'name': 'Blue Matrix Rain',
                'description': 'Blue matrix theme with faster movement',
                'category': 'Matrix/Rain'
            },
            'glyph_rain3': {
                'file': 'glyph_rain3.py',
                'name': 'Rainbow Matrix Rain', 
                'description': 'Rainbow colored matrix with shifting hues',
                'category': 'Matrix/Rain'
            },
            'matrix_binary': {
                'file': 'matrix_binary.py',
                'name': 'Binary Matrix',
                'description': 'Matrix with 1s, 0s and Japanese symbols',
                'category': 'Matrix/Rain'
            },
            'neon_rain': {
                'file': 'neon_rain.py',
                'name': 'Neon Rain',
                'description': 'Tiny neon shapes in green and blue',
                'category': 'Matrix/Rain'
            },
            
            # Timer/Accumulation Effects
            'timer_medium': {
                'file': 'glyph_rain4_timer.py',
                'name': 'Medium Timer',
                'description': 'Characters accumulate over several hours',
                'category': 'Timer'
            },
            'timer_slow': {
                'file': 'glyph_rain5_slow.py',
                'name': 'All-Day Timer',
                'description': 'Very slow accumulation for 8+ hour periods',
                'category': 'Timer'
            },
            
            # Water Effects
            'raindrops': {
                'file': 'raindrops.py',
                'name': 'Raindrops',
                'description': 'Realistic rain with splashes and puddles',
                'category': 'Water'
            },
            'heavy_rain': {
                'file': 'heavy_rain.py',
                'name': 'Heavy Rain',
                'description': 'Intense downpour with flooding',
                'category': 'Water'
            },
            
            # Micro Particles
            'micro_dots': {
                'file': 'micro_dots.py',
                'name': 'Micro Dots',
                'description': 'Ultra-tiny pixel dots at maximum density',
                'category': 'Particles'
            },
            'micro_drip': {
                'file': 'micro_dots_dripping.py',
                'name': 'Dripping Dots',
                'description': 'Dots that accumulate and drip through bottom',
                'category': 'Particles'
            },
            
            # Fire Effects
            'simple_flames': {
                'file': 'simple_flames.py',
                'name': 'Simple Flames',
                'description': 'Simple stable flame effect',
                'category': 'Fire'
            },
            'campfire': {
                'file': 'campfire.py',
                'name': 'Campfire',
                'description': 'Cozy flickering campfire',
                'category': 'Fire'
            },
            
            # 1990s Retro
            'retro_geometry': {
                'file': 'retro_geometry.py',
                'name': 'Retro Geometry',
                'description': 'Classic 1990s geometric shapes',
                'category': 'Retro'
            },
            'plasma_field': {
                'file': 'plasma_field.py',
                'name': 'Plasma Field',
                'description': 'Mathematical plasma effect',
                'category': 'Retro'
            },
            'bouncing_balls': {
                'file': 'bouncing_balls.py',
                'name': 'Bouncing Balls',
                'description': 'Classic bouncing balls with trails',
                'category': 'Retro'
            },
            
            # Visual Effects
            'kaleidoscope': {
                'file': 'kaleidoscope.py',
                'name': 'Kaleidoscope',
                'description': 'Symmetrical rotating patterns',
                'category': 'Visual'
            },
            
            # Fractals
            'mandelbrot': {
                'file': 'mandelbrot.py',
                'name': 'Mandelbrot Set',
                'description': 'Classic fractal with zooming animation',
                'category': 'Fractals'
            },
            'julia_set': {
                'file': 'julia_set.py',
                'name': 'Julia Set',
                'description': 'Dynamic Julia sets with morphing parameters',
                'category': 'Fractals'
            },
            'sierpinski': {
                'file': 'sierpinski.py',
                'name': 'Sierpinski Triangle',
                'description': 'Fractal generation using chaos game',
                'category': 'Fractals'
            },
            'dragon_curve': {
                'file': 'dragon_curve.py',
                'name': 'Dragon Curve',
                'description': 'L-system fractal with growing complexity',
                'category': 'Fractals'
            }
        }
    
    def show_menu(self):
        """Display interactive menu"""
        print("\n" + "="*60)
        print("🖥️  WAVESHARE 1.44\" LCD HAT SCREENSAVERS")
        print("="*60)
        print(f"📊 Total screensavers available: {len(self.screensavers)}")
        print()
        
        # Group by category
        categories = {}
        for key, info in self.screensavers.items():
            cat = info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((key, info))
        
        # Display by category
        for category, items in categories.items():
            print(f"📁 {category.upper()}:")
            for key, info in items:
                print(f"   {key:<15} - {info['name']}")
            print()
        
        print("COMMANDS:")
        print("   random                    - Run random screensaver")
        print("   list                      - List all screensavers") 
        print("   <screensaver_name>        - Run specific screensaver")
        print("   help                      - Show this menu")
        print()
        
        while True:
            choice = input("Enter command or screensaver name (or 'quit'): ").strip().lower()
            
            if choice in ['quit', 'exit', 'q']:
                break
            elif choice == 'random':
                self.run_random()
                break
            elif choice == 'list':
                self.list_screensavers()
            elif choice == 'help':
                self.show_menu()
                break
            elif choice in self.screensavers:
                self.run_screensaver(choice)
                break
            else:
                print(f"❌ Unknown screensaver: {choice}")
                print("Type 'list' to see available screensavers")
    
    def list_screensavers(self):
        """List all available screensavers"""
        print("\n📋 AVAILABLE SCREENSAVERS:")
        print("-" * 50)
        
        for key, info in sorted(self.screensavers.items()):
            print(f"{key:<15} - {info['name']}")
            print(f"{'':>15}   {info['description']}")
            print()
    
    def run_random(self):
        """Run a random screensaver"""
        choice = random.choice(list(self.screensavers.keys()))
        print(f"🎲 Randomly selected: {choice}")
        self.run_screensaver(choice)
    
    def run_screensaver(self, name):
        """Run specific screensaver"""
        if name not in self.screensavers:
            print(f"❌ Screensaver '{name}' not found")
            return
        
        info = self.screensavers[name]
        filepath = info['file']
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return
        
        print(f"🚀 Starting: {info['name']}")
        print(f"📝 Description: {info['description']}")
        print(f"⏯️  Press Ctrl+C to stop the screensaver")
        print("-" * 50)
        
        try:
            subprocess.run(['python3', filepath])
        except KeyboardInterrupt:
            print(f"\n✅ Screensaver stopped")
        except Exception as e:
            print(f"❌ Error running screensaver: {e}")

def main():
    launcher = ScreensaverLauncher()
    
    if len(sys.argv) == 1:
        # No arguments - show menu
        launcher.show_menu()
    elif len(sys.argv) == 2:
        command = sys.argv[1].lower()
        
        if command == 'random':
            launcher.run_random()
        elif command == 'list':
            launcher.list_screensavers()
        elif command in ['help', '--help', '-h']:
            launcher.show_menu()
        elif command in launcher.screensavers:
            launcher.run_screensaver(command)
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'help' to see available commands")
    else:
        print("❌ Too many arguments")
        print("Usage: python3 screensaver_launcher.py [screensaver_name|random|list|help]")

if __name__ == "__main__":
    main()