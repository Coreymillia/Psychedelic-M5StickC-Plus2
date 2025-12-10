#!/usr/bin/env python3
"""
Waveshare LCD Screensaver Manager
Complete management system for all screensavers with number selection
"""

import sys
import os
import subprocess
import time
import signal

class ScreensaverManager:
    def __init__(self):
        self.screensavers = {
            # Matrix/Rain Effects - Fixed and Original
            1: {
                'file': 'glyph_rain1_fixed.py',
                'name': 'Fixed Matrix Rain (Stable)',
                'description': 'Memory-leak-free classic matrix rain - RECOMMENDED',
                'category': 'Matrix/Rain',
                'stability': '🟢 STABLE'
            },
            2: {
                'file': 'glyph_rain1.py',
                'name': 'Classic Matrix Rain (Original)',
                'description': 'Original green falling characters - may have memory leaks',
                'category': 'Matrix/Rain',
                'stability': '🟡 ORIGINAL'
            },
            3: {
                'file': 'glyph_rain2.py', 
                'name': 'Blue Matrix Rain',
                'description': 'Blue matrix theme with faster movement',
                'category': 'Matrix/Rain',
                'stability': '🟡 ORIGINAL'
            },
            4: {
                'file': 'glyph_rain3.py',
                'name': 'Rainbow Matrix Rain', 
                'description': 'Rainbow colored matrix with shifting hues',
                'category': 'Matrix/Rain',
                'stability': '🟡 ORIGINAL'
            },
            5: {
                'file': 'matrix_binary.py',
                'name': 'Binary Matrix',
                'description': 'Matrix with 1s, 0s and Japanese symbols',
                'category': 'Matrix/Rain',
                'stability': '🟡 ORIGINAL'
            },
            6: {
                'file': 'neon_rain.py',
                'name': 'Neon Rain',
                'description': 'Tiny neon shapes in green and blue',
                'category': 'Matrix/Rain',
                'stability': '🟡 ORIGINAL'
            },
            
            # Timer/Accumulation Effects
            7: {
                'file': 'glyph_rain4_timer.py',
                'name': 'Medium Timer Rain',
                'description': 'Characters accumulate over several hours',
                'category': 'Timer',
                'stability': '🟡 ORIGINAL'
            },
            8: {
                'file': 'glyph_rain5_slow.py',
                'name': 'All-Day Timer Rain',
                'description': 'Very slow accumulation for 8+ hour periods',
                'category': 'Timer',
                'stability': '🟡 ORIGINAL'
            },
            
            # Water Effects
            9: {
                'file': 'raindrops.py',
                'name': 'Raindrops',
                'description': 'Realistic rain with splashes and puddles',
                'category': 'Water',
                'stability': '🟡 ORIGINAL'
            },
            10: {
                'file': 'heavy_rain.py',
                'name': 'Heavy Rain',
                'description': 'Intense downpour with flooding',
                'category': 'Water',
                'stability': '🟡 ORIGINAL'
            },
            
            # Micro Particles
            11: {
                'file': 'micro_dots.py',
                'name': 'Micro Dots',
                'description': 'Ultra-tiny pixel dots at maximum density',
                'category': 'Particles',
                'stability': '🟡 ORIGINAL'
            },
            12: {
                'file': 'micro_dots_dripping.py',
                'name': 'Dripping Dots',
                'description': 'Dots that accumulate and drip through bottom',
                'category': 'Particles',
                'stability': '🟡 ORIGINAL'
            },
            
            # Fire Effects
            13: {
                'file': 'simple_flames.py',
                'name': 'Simple Flames',
                'description': 'Simple stable flame effect',
                'category': 'Fire',
                'stability': '🟡 ORIGINAL'
            },
            14: {
                'file': 'campfire.py',
                'name': 'Campfire',
                'description': 'Cozy flickering campfire',
                'category': 'Fire',
                'stability': '🟡 ORIGINAL'
            },
            
            # 1990s Retro
            15: {
                'file': 'retro_geometry.py',
                'name': 'Retro Geometry',
                'description': 'Classic 1990s geometric shapes',
                'category': 'Retro',
                'stability': '🟡 ORIGINAL'
            },
            16: {
                'file': 'plasma_field.py',
                'name': 'Plasma Field',
                'description': 'Mathematical plasma effect',
                'category': 'Retro',
                'stability': '🟡 ORIGINAL'
            },
            17: {
                'file': 'bouncing_balls.py',
                'name': 'Bouncing Balls',
                'description': 'Classic bouncing balls with trails',
                'category': 'Retro',
                'stability': '🟡 ORIGINAL'
            },
            
            # Visual Effects
            18: {
                'file': 'kaleidoscope.py',
                'name': 'Kaleidoscope',
                'description': 'Symmetrical rotating patterns',
                'category': 'Visual',
                'stability': '🟡 ORIGINAL'
            },
            
            # Fractals
            19: {
                'file': 'mandelbrot.py',
                'name': 'Mandelbrot Set',
                'description': 'Classic fractal with zooming animation',
                'category': 'Fractals',
                'stability': '🟡 ORIGINAL'
            },
            20: {
                'file': 'julia_set.py',
                'name': 'Julia Set',
                'description': 'Dynamic Julia sets with morphing parameters',
                'category': 'Fractals',
                'stability': '🟡 ORIGINAL'
            },
            21: {
                'file': 'sierpinski.py',
                'name': 'Sierpinski Triangle',
                'description': 'Fractal generation using chaos game',
                'category': 'Fractals',
                'stability': '🟡 ORIGINAL'
            },
            22: {
                'file': 'dragon_curve.py',
                'name': 'Dragon Curve',
                'description': 'L-system fractal with growing complexity',
                'category': 'Fractals',
                'stability': '🟡 ORIGINAL'
            }
        }
        
        # Service management options
        self.service_options = {
            90: {
                'action': 'setup_stable_service',
                'name': 'Setup Stable Service (Recommended)',
                'description': 'Lock to fixed matrix rain with auto-restart protection'
            },
            91: {
                'action': 'setup_random_service',
                'name': 'Setup Random Service',
                'description': 'Rotate through different screensavers automatically'
            },
            92: {
                'action': 'disable_all_services',
                'name': 'Disable All Services',
                'description': 'Stop and disable all auto-start screensavers'
            },
            93: {
                'action': 'check_service_status',
                'name': 'Check Service Status',
                'description': 'Show current service and process status'
            },
            94: {
                'action': 'cleanup_gpio_standalone',
                'name': 'Fix GPIO Conflicts',
                'description': 'Stop all screensavers and clear GPIO locks'
            }
        }
        
        # Button control options
        self.button_options = {
            80: {
                'action': 'run_simple_button_switcher',
                'name': 'Simple Button Switcher (3 buttons)',
                'description': 'KEY1=Next, KEY2=Prev, KEY3=Exit - Easy!'
            },
            81: {
                'action': 'run_advanced_button_switcher', 
                'name': 'Advanced Button Switcher (All buttons)',
                'description': 'Full joystick + 3 keys - More features'
            },
            82: {
                'action': 'setup_button_service',
                'name': 'Auto-Start Button Switcher',
                'description': 'Start button switcher automatically on boot'
            }
        }
        
        # Background and boot options
        self.background_options = {
            50: {
                'action': 'run_background_launcher',
                'name': 'Background Mode',
                'description': 'Run screensavers in background (survive terminal closing)'
            },
            51: {
                'action': 'open_boot_manager', 
                'name': 'Boot Manager',
                'description': 'Set any screensaver to auto-start on boot'
            },
            52: {
                'action': 'run_background_buttons',
                'name': 'Background Button Switcher',
                'description': 'Run button switcher in background'
            }
        }

    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "="*80)
        print("🖥️  WAVESHARE 1.44\" LCD HAT SCREENSAVER MANAGER")
        print("="*80)
        print(f"📊 Total screensavers: {len(self.screensavers)} | Background/Boot: {len(self.background_options)} | Buttons: {len(self.button_options)} | Services: {len(self.service_options)}")
        print()
        
        # Group by category and display
        categories = {}
        for num, info in self.screensavers.items():
            cat = info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((num, info))
        
        for category, items in categories.items():
            print(f"📁 {category.upper()}:")
            for num, info in items:
                status_icon = "⭐" if "Fixed" in info['name'] else "  "
                print(f"   {status_icon} {num:2d}) {info['stability']} {info['name']}")
            print()
        
        print("🔄 BACKGROUND & BOOT:")
        for num, info in self.background_options.items():
            print(f"   {num}) {info['name']}")
        print()
        
        print("🕹️ BUTTON CONTROLS:")
        for num, info in self.button_options.items():
            print(f"   {num}) {info['name']}")
        print()
        
        print("🔧 SERVICE MANAGEMENT:")
        for num, info in self.service_options.items():
            print(f"   {num}) {info['name']}")
        print()
        
        print("📋 QUICK OPTIONS:")
        print("   99) Test screensaver for 30 seconds")
        print("    0) Exit")
        print()

    def show_detailed_info(self, choice):
        """Show detailed information about a screensaver"""
        if choice in self.screensavers:
            info = self.screensavers[choice]
            print(f"\n📄 SCREENSAVER #{choice}: {info['name']}")
            print("-" * 60)
            print(f"📁 Category: {info['category']}")
            print(f"🔧 Stability: {info['stability']}")
            print(f"📝 Description: {info['description']}")
            print(f"📄 File: {info['file']}")
            print(f"📍 Status: {'✅ Available' if os.path.exists(info['file']) else '❌ File missing'}")
            print()

    def cleanup_gpio_conflicts(self):
        """Clean up GPIO conflicts before starting screensavers"""
        print("🧹 Cleaning up GPIO conflicts...")
        
        # Get current process info to avoid killing ourselves
        current_pid = os.getpid()
        
        # Kill specific conflicting processes but avoid the manager
        processes = ['glyph_rain', 'matrix_', 'micro_dots', 'flames', 'plasma', 
                    'bouncing', 'kaleidoscope', 'raindrops', 'neon_rain', 'mandelbrot',
                    'julia_set', 'sierpinski', 'dragon_curve', 'campfire', 'retro_geometry',
                    'simple_button_switcher', 'button_screensaver']
        
        for process in processes:
            try:
                # Use pgrep to get PIDs first, then filter out our own process
                result = subprocess.run(['pgrep', '-f', process], 
                                      capture_output=True, text=True, timeout=5)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            if int(pid) != current_pid:  # Don't kill ourselves
                                subprocess.run(['kill', pid], capture_output=True, timeout=2)
                                print(f"  🔄 Stopped {process} (PID: {pid})")
                        except (ValueError, subprocess.TimeoutExpired):
                            pass
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass
        
        # Stop conflicting services  
        services = ['lcd-stable.service', 'lcd-glyph-locked.service', 
                   'lcd-button-switcher.service', 'lcd-random.service']
        
        for service in services:
            try:
                result = subprocess.run(['sudo', 'systemctl', 'stop', service], 
                                      capture_output=True, timeout=10)
                if result.returncode == 0:
                    print(f"  🛑 Stopped {service}")
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass
        
        # Wait for GPIO release
        time.sleep(1)
        print("✅ GPIO cleanup complete")

    def run_screensaver(self, choice, test_mode=False, duration=None):
        """Run a specific screensaver"""
        if choice not in self.screensavers:
            print(f"❌ Invalid screensaver number: {choice}")
            return False
        
        info = self.screensavers[choice]
        filepath = info['file']
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
        
        self.show_detailed_info(choice)
        
        # Clean up GPIO conflicts first
        self.cleanup_gpio_conflicts()
        
        if test_mode and duration:
            print(f"🧪 Testing for {duration} seconds...")
            print("⏯️  Test will auto-stop, or press Ctrl+C to stop early")
        else:
            print("🚀 Starting screensaver...")
            print("⏯️  Press Ctrl+C to stop")
        
        print("-" * 60)
        
        try:
            if test_mode and duration:
                # Use timeout for test mode
                result = subprocess.run(['timeout', f'{duration}s', 'python3', filepath], 
                                      capture_output=False)
                if result.returncode == 124:  # timeout exit code
                    print(f"\n✅ {duration}-second test completed successfully!")
                else:
                    print(f"\n⚠️  Test ended with exit code: {result.returncode}")
            else:
                # Normal run
                subprocess.run(['python3', filepath])
                
        except KeyboardInterrupt:
            print(f"\n✅ Screensaver stopped by user")
        except Exception as e:
            print(f"\n❌ Error running screensaver: {e}")
            return False
        
        return True

    def setup_stable_service(self):
        """Setup the stable fixed matrix rain service"""
        print("\n🔒 Setting up stable matrix rain service...")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        username = os.getenv('USER', 'pi')
        
        service_content = f"""[Unit]
Description=Waveshare LCD Stable Matrix Rain (Memory-Safe)
After=multi-user.target

[Service]
Type=simple
User={username}
Group={username}
WorkingDirectory={script_dir}
ExecStart=/usr/bin/python3 {script_dir}/glyph_rain1_fixed.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
MemoryMax=200M
CPUQuota=50%

[Install]
WantedBy=multi-user.target"""
        
        try:
            # Stop existing services
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-screensaver.service'], 
                         capture_output=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-glyph-locked.service'], 
                         capture_output=True)
            
            # Create new service file
            with open('/tmp/lcd-stable.service', 'w') as f:
                f.write(service_content)
            
            # Install service
            subprocess.run(['sudo', 'mv', '/tmp/lcd-stable.service', 
                          '/etc/systemd/system/lcd-stable.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'lcd-stable.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'lcd-stable.service'], check=True)
            
            print("✅ Stable matrix rain service installed and started!")
            print("   Features:")
            print("   - Memory leak protection")
            print("   - Auto-restart on failure")
            print("   - Resource limits (200MB RAM, 50% CPU)")
            print("   - Boot-time startup")
            print()
            print("   Management commands:")
            print("   sudo systemctl status lcd-stable")
            print("   sudo systemctl restart lcd-stable")
            print("   sudo systemctl stop lcd-stable")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup service: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def setup_random_service(self):
        """Setup random screensaver service"""
        print("\n🎲 Setting up random screensaver service...")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        username = os.getenv('USER', 'pi')
        
        service_content = f"""[Unit]
Description=Waveshare LCD Random Screensaver
After=multi-user.target

[Service]
Type=simple
User={username}
Group={username}
WorkingDirectory={script_dir}
ExecStart=/usr/bin/python3 {script_dir}/screensaver_launcher.py random
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target"""
        
        try:
            # Stop existing services
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-stable.service'], 
                         capture_output=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-glyph-locked.service'], 
                         capture_output=True)
            
            # Create service file
            with open('/tmp/lcd-random.service', 'w') as f:
                f.write(service_content)
            
            # Install service
            subprocess.run(['sudo', 'mv', '/tmp/lcd-random.service', 
                          '/etc/systemd/system/lcd-random.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'lcd-random.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'lcd-random.service'], check=True)
            
            print("✅ Random screensaver service installed and started!")
            print("   Note: May experience memory issues with some screensavers")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup service: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def disable_all_services(self):
        """Disable all screensaver services"""
        print("\n🛑 Disabling all screensaver services...")
        
        services = ['lcd-stable.service', 'lcd-random.service', 'lcd-screensaver.service', 
                   'lcd-glyph-locked.service']
        
        for service in services:
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', service], capture_output=True)
                subprocess.run(['sudo', 'systemctl', 'disable', service], capture_output=True)
            except:
                pass  # Service might not exist
        
        # Kill any running screensaver processes
        try:
            subprocess.run(['pkill', '-f', 'python3.*\.py'], capture_output=True)
        except:
            pass
        
        print("✅ All screensaver services disabled and processes stopped!")

    def check_service_status(self):
        """Check current service and process status"""
        print("\n📊 SCREENSAVER SERVICE STATUS")
        print("="*50)
        
        services = [
            ('lcd-stable.service', 'Stable Matrix Rain'),
            ('lcd-random.service', 'Random Screensaver'),
            ('lcd-screensaver.service', 'Legacy Random'),
            ('lcd-glyph-locked.service', 'Legacy Locked')
        ]
        
        active_services = []
        for service, description in services:
            try:
                result = subprocess.run(['systemctl', 'is-active', service], 
                                      capture_output=True, text=True)
                status = result.stdout.strip()
                enabled = subprocess.run(['systemctl', 'is-enabled', service], 
                                       capture_output=True, text=True).stdout.strip()
                
                if status == 'active':
                    print(f"🟢 {description}: RUNNING (enabled: {enabled})")
                    active_services.append(service)
                elif enabled == 'enabled':
                    print(f"🟡 {description}: ENABLED but not running")
                else:
                    print(f"⚫ {description}: DISABLED")
            except:
                print(f"⚫ {description}: NOT INSTALLED")
        
        print("\n📈 RUNNING PROCESSES:")
        try:
            result = subprocess.run(['pgrep', '-af', 'python3.*\.py'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    if 'screensaver' in line.lower() or any(name in line for name in ['glyph', 'matrix', 'rain']):
                        print(f"🟢 {line}")
            else:
                print("⚫ No Python screensavers running")
        except:
            print("❌ Could not check running processes")
        
        if active_services:
            print(f"\n✅ {len(active_services)} service(s) active")
        else:
            print("\n⚫ No screensaver services currently active")

    def run_simple_button_switcher(self):
        """Run the simple 3-button switcher"""
        print("\n🕹️ Starting Simple Button Switcher...")
        print("This will give you physical button control:")
        print("  KEY1 (Button 1): Next screensaver")
        print("  KEY2 (Button 2): Previous screensaver") 
        print("  KEY3 (Button 3): Exit switcher")
        print()
        
        # Clean up GPIO conflicts first
        self.cleanup_gpio_conflicts()
        
        try:
            subprocess.run(['python3', 'simple_button_switcher.py'])
        except KeyboardInterrupt:
            print("\n✅ Button switcher stopped")
        except Exception as e:
            print(f"❌ Error running button switcher: {e}")

    def run_advanced_button_switcher(self):
        """Run the advanced button switcher with joystick"""
        print("\n🕹️ Starting Advanced Button Switcher...")
        print("Full control with all buttons:")
        print("  KEY1: Next screensaver →")
        print("  KEY2: Previous screensaver ←")
        print("  KEY3: Pause/Resume ⏸️")
        print("  Joystick UP: Jump to favorites ⭐")
        print("  Joystick DOWN: Show info ℹ️")
        print("  Joystick PRESS: Exit 🚪")
        print()
        
        # Clean up GPIO conflicts first
        self.cleanup_gpio_conflicts()
        
        try:
            subprocess.run(['python3', 'button_screensaver.py'])
        except KeyboardInterrupt:
            print("\n✅ Advanced button switcher stopped")
        except Exception as e:
            print(f"❌ Error running advanced button switcher: {e}")

    def setup_button_service(self):
        """Setup button switcher to auto-start on boot"""
        print("\n🕹️ Setting up auto-start button switcher service...")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        username = os.getenv('USER', 'pi')
        
        service_content = f"""[Unit]
Description=Waveshare LCD Button Screensaver Switcher
After=multi-user.target

[Service]
Type=simple
User={username}
Group={username}
WorkingDirectory={script_dir}
ExecStart=/usr/bin/python3 {script_dir}/simple_button_switcher.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target"""
        
        try:
            # Stop existing services
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-stable.service'], 
                         capture_output=True)
            subprocess.run(['sudo', 'systemctl', 'stop', 'lcd-random.service'], 
                         capture_output=True)
            
            # Create service file
            with open('/tmp/lcd-button-switcher.service', 'w') as f:
                f.write(service_content)
            
            # Install service
            subprocess.run(['sudo', 'mv', '/tmp/lcd-button-switcher.service', 
                          '/etc/systemd/system/lcd-button-switcher.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'lcd-button-switcher.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'lcd-button-switcher.service'], check=True)
            
            print("✅ Button switcher service installed and started!")
            print("   Features:")
            print("   - Physical button control (KEY1=Next, KEY2=Prev, KEY3=Exit)")
            print("   - Auto-restart on failure")
            print("   - Boot-time startup")
            print("   - Cycles through 10 best screensavers")
            print()
            print("   Management commands:")
            print("   sudo systemctl status lcd-button-switcher")
            print("   sudo systemctl restart lcd-button-switcher")
            print("   sudo systemctl stop lcd-button-switcher")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup button service: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def cleanup_gpio_standalone(self):
        """Standalone GPIO cleanup command"""
        print("\n🧹 FIXING GPIO CONFLICTS")
        print("="*40)
        
        self.cleanup_gpio_conflicts()
        
        print("🔍 Checking remaining processes...")
        try:
            result = subprocess.run(['pgrep', '-af', 'python3.*screensaver'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("⚠️ Some processes may still be running:")
                for line in result.stdout.strip().split('\n'):
                    if 'screensaver_manager' not in line:
                        print(f"   {line}")
            else:
                print("✅ No conflicting processes found")
        except:
            print("✅ Process check complete")
        
        print("\n🔌 GPIO pins should now be available for new screensavers!")

    def run_background_launcher(self):
        """Show background launcher menu"""
        print("\n🔄 BACKGROUND MODE - Survive Terminal Closing")
        print("="*50)
        print("Choose a screensaver to run in background:")
        print("It will keep running even after you close the terminal!")
        print()
        
        # Show numbered options
        for i in range(1, 11):  # Show top 10 screensavers
            if i in self.screensavers:
                info = self.screensavers[i]
                status = "⭐" if i == 1 else "  " 
                print(f"   {status} {i:2d}) {info['name']}")
        
        print("\n🕹️ BUTTON CONTROLS:")
        print("      80) Simple Button Switcher")
        print("      81) Advanced Button Switcher")
        print()
        
        choice = input("Enter screensaver number to run in background (or 0 to cancel): ").strip()
        
        try:
            choice_num = int(choice)
            if choice_num == 0:
                return
            
            if choice_num in [1,2,3,4,5,6,7,8,9,10,80,81]:
                print(f"🚀 Launching screensaver #{choice_num} in background...")
                subprocess.run(['python3', 'background_launcher.py', str(choice_num)])
            else:
                print(f"❌ Invalid choice for background mode: {choice_num}")
                
        except ValueError:
            print("❌ Please enter a valid number")

    def open_boot_manager(self):
        """Open the boot manager"""
        print("\n🚀 Opening Boot Manager...")
        print("This lets you set any screensaver to auto-start on boot")
        print("and easily switch between different boot screensavers.")
        print()
        
        try:
            subprocess.run(['python3', 'boot_manager.py'])
        except KeyboardInterrupt:
            print("\n✅ Boot manager closed")
        except Exception as e:
            print(f"❌ Error opening boot manager: {e}")

    def run_background_buttons(self):
        """Run button switcher in background"""
        print("\n🕹️ Starting Button Switcher in Background...")
        print("Physical button controls will work even after closing terminal!")
        print()
        
        try:
            subprocess.run(['python3', 'background_launcher.py', '80'])
        except Exception as e:
            print(f"❌ Error starting background button switcher: {e}")

    def run_interactive_menu(self):
        """Main interactive menu loop"""
        while True:
            self.show_main_menu()
            
            try:
                choice = input("Enter your choice (number or 0 to exit): ").strip()
                
                if not choice:
                    continue
                    
                choice_num = int(choice)
                
                if choice_num == 0:
                    print("👋 Goodbye!")
                    break
                
                elif choice_num == 99:
                    # Test mode
                    print("\nSelect screensaver to test:")
                    test_choice = input("Enter screensaver number (1-22): ").strip()
                    if test_choice.isdigit():
                        self.run_screensaver(int(test_choice), test_mode=True, duration=30)
                    else:
                        print("❌ Invalid number")
                
                elif choice_num in self.screensavers:
                    # Run screensaver
                    self.run_screensaver(choice_num)
                
                elif choice_num == 90:
                    self.setup_stable_service()
                
                elif choice_num == 91:
                    self.setup_random_service()
                
                elif choice_num == 92:
                    self.disable_all_services()
                
                elif choice_num == 93:
                    self.check_service_status()
                
                elif choice_num == 80:
                    self.run_simple_button_switcher()
                
                elif choice_num == 81:
                    self.run_advanced_button_switcher()
                
                elif choice_num == 82:
                    self.setup_button_service()
                
                elif choice_num == 50:
                    self.run_background_launcher()
                
                elif choice_num == 51:
                    self.open_boot_manager()
                
                elif choice_num == 52:
                    self.run_background_buttons()
                
                elif choice_num == 94:
                    self.cleanup_gpio_standalone()
                
                else:
                    print(f"❌ Invalid choice: {choice_num}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
            
            if choice_num != 0:
                input("\nPress Enter to continue...")

def main():
    if len(sys.argv) > 1:
        # Command line mode
        manager = ScreensaverManager()
        
        if sys.argv[1].isdigit():
            choice = int(sys.argv[1])
            if choice in manager.screensavers:
                manager.run_screensaver(choice)
            else:
                print(f"❌ Invalid screensaver number: {choice}")
        else:
            print("Usage: python3 screensaver_manager.py [screensaver_number]")
    else:
        # Interactive mode
        manager = ScreensaverManager()
        manager.run_interactive_menu()

if __name__ == "__main__":
    main()