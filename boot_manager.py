#!/usr/bin/env python3
"""
Boot Manager - Set any screensaver to auto-start on boot
Allows easy switching between different boot screensavers
"""

import subprocess
import os
import sys

class BootManager:
    def __init__(self):
        self.screensavers = {
            1: {'file': 'glyph_rain1_fixed.py', 'name': 'Fixed Matrix Rain (Stable)', 'stability': '🟢'},
            2: {'file': 'glyph_rain1.py', 'name': 'Classic Matrix Rain', 'stability': '🟡'},
            3: {'file': 'glyph_rain2.py', 'name': 'Blue Matrix Rain', 'stability': '🟡'},
            4: {'file': 'glyph_rain3.py', 'name': 'Rainbow Matrix Rain', 'stability': '🟡'},
            5: {'file': 'matrix_binary.py', 'name': 'Binary Matrix', 'stability': '🟡'},
            6: {'file': 'neon_rain.py', 'name': 'Neon Rain', 'stability': '🟡'},
            7: {'file': 'glyph_rain4_timer.py', 'name': 'Medium Timer Rain', 'stability': '🟡'},
            8: {'file': 'glyph_rain5_slow.py', 'name': 'All-Day Timer Rain', 'stability': '🟡'},
            9: {'file': 'raindrops.py', 'name': 'Raindrops', 'stability': '🟡'},
            10: {'file': 'heavy_rain.py', 'name': 'Heavy Rain', 'stability': '🟡'},
            11: {'file': 'micro_dots.py', 'name': 'Micro Dots', 'stability': '🟡'},
            12: {'file': 'micro_dots_dripping.py', 'name': 'Dripping Dots', 'stability': '🟡'},
            13: {'file': 'simple_flames.py', 'name': 'Simple Flames', 'stability': '🟡'},
            14: {'file': 'campfire.py', 'name': 'Campfire', 'stability': '🟡'},
            15: {'file': 'retro_geometry.py', 'name': 'Retro Geometry', 'stability': '🟡'},
            16: {'file': 'plasma_field.py', 'name': 'Plasma Field', 'stability': '🟡'},
            17: {'file': 'bouncing_balls.py', 'name': 'Bouncing Balls', 'stability': '🟡'},
            18: {'file': 'kaleidoscope.py', 'name': 'Kaleidoscope', 'stability': '🟡'},
            19: {'file': 'mandelbrot.py', 'name': 'Mandelbrot Set', 'stability': '🟡'},
            20: {'file': 'julia_set.py', 'name': 'Julia Set', 'stability': '🟡'},
            21: {'file': 'sierpinski.py', 'name': 'Sierpinski Triangle', 'stability': '🟡'},
            22: {'file': 'dragon_curve.py', 'name': 'Dragon Curve', 'stability': '🟡'},
            80: {'file': 'simple_button_switcher.py', 'name': 'Button Switcher (3 buttons)', 'stability': '🕹️'},
            81: {'file': 'button_screensaver.py', 'name': 'Advanced Button Switcher', 'stability': '🕹️'}
        }
        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.username = os.getenv('USER', 'pi')

    def show_menu(self):
        """Show boot manager menu"""
        print("\n" + "="*70)
        print("🚀 BOOT SCREENSAVER MANAGER")  
        print("="*70)
        print("Set any screensaver to start automatically on boot!")
        print()
        
        # Show current boot screensaver
        current = self.get_current_boot_screensaver()
        if current:
            print(f"🔄 Currently set to boot: {current}")
        else:
            print("⚫ No screensaver set to auto-boot")
        print()
        
        # Show screensaver options in groups
        print("📱 MATRIX/RAIN SCREENSAVERS:")
        for i in range(1, 7):
            info = self.screensavers[i]
            status = "⭐" if i == 1 else "  "
            print(f"   {status} {i:2d}) {info['stability']} {info['name']}")
        
        print("\n🌊 OTHER SCREENSAVERS:")
        for i in range(7, 23):
            info = self.screensavers[i]
            print(f"      {i:2d}) {info['stability']} {info['name']}")
        
        print("\n🕹️ BUTTON CONTROLS:")
        for i in [80, 81]:
            info = self.screensavers[i]
            print(f"      {i:2d}) {info['stability']} {info['name']}")
            
        print("\n🔧 BOOT MANAGEMENT:")
        print("      95) Check Current Boot Status")
        print("      96) Disable All Auto-Boot")
        print("      97) Show Boot Service Logs")
        print("       0) Exit")
        print()

    def get_current_boot_screensaver(self):
        """Check what screensaver is currently set to boot"""
        try:
            # Check if any of our services are enabled
            services = [
                ('lcd-boot-screensaver.service', 'Custom Boot Screensaver'),
                ('lcd-stable.service', 'Stable Matrix Rain'),
                ('lcd-button-switcher.service', 'Button Switcher'),
                ('lcd-glyph-locked.service', 'Legacy Glyph Rain')
            ]
            
            for service, desc in services:
                result = subprocess.run(['systemctl', 'is-enabled', service], 
                                      capture_output=True, text=True)
                if result.stdout.strip() == 'enabled':
                    return f"{desc} ({service})"
            
            return None
        except:
            return None

    def create_boot_service(self, screensaver_num):
        """Create systemd service for specific screensaver"""
        if screensaver_num not in self.screensavers:
            print(f"❌ Invalid screensaver number: {screensaver_num}")
            return False
        
        info = self.screensavers[screensaver_num]
        filepath = info['file']
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
        
        service_content = f"""[Unit]
Description=LCD Boot Screensaver #{screensaver_num}: {info['name']}
After=multi-user.target
Wants=multi-user.target

[Service]
Type=simple
User={self.username}
Group={self.username}
WorkingDirectory={self.script_dir}
ExecStart=/usr/bin/python3 {self.script_dir}/{filepath}
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits to prevent system issues
MemoryMax=250M
CPUQuota=75%

# Environment
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target"""
        
        try:
            print(f"🔧 Setting up boot service for #{screensaver_num}: {info['name']}")
            
            # Stop and disable all existing LCD services
            existing_services = [
                'lcd-boot-screensaver.service',
                'lcd-stable.service', 
                'lcd-glyph-locked.service',
                'lcd-button-switcher.service',
                'lcd-random.service'
            ]
            
            for service in existing_services:
                subprocess.run(['sudo', 'systemctl', 'stop', service], capture_output=True)
                subprocess.run(['sudo', 'systemctl', 'disable', service], capture_output=True)
            
            # Create new service file
            with open('/tmp/lcd-boot-screensaver.service', 'w') as f:
                f.write(service_content)
            
            # Install and enable new service
            subprocess.run(['sudo', 'mv', '/tmp/lcd-boot-screensaver.service', 
                          '/etc/systemd/system/lcd-boot-screensaver.service'], check=True)
            subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'lcd-boot-screensaver.service'], check=True)
            
            print("✅ Boot service created and enabled!")
            print(f"   Screensaver #{screensaver_num} will start on every boot")
            print("   Features:")
            print("   - Survives terminal closing")
            print("   - Auto-restart on crash")
            print("   - Resource limits for system safety")
            print("   - Starts after system is ready")
            print()
            print("   Management commands:")
            print("   sudo systemctl status lcd-boot-screensaver")
            print("   sudo systemctl restart lcd-boot-screensaver")
            print("   sudo systemctl stop lcd-boot-screensaver")
            print()
            
            # Ask if they want to start it now
            start_now = input("🚀 Start the screensaver now? (y/n): ").lower().strip()
            if start_now in ['y', 'yes']:
                result = subprocess.run(['sudo', 'systemctl', 'start', 'lcd-boot-screensaver.service'])
                if result.returncode == 0:
                    print("✅ Screensaver started! Check your LCD display.")
                else:
                    print("⚠️ Service enabled but may need a restart to start properly")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create boot service: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def check_boot_status(self):
        """Show detailed boot status"""
        print("\n🔍 BOOT SERVICE STATUS")
        print("="*50)
        
        services = [
            'lcd-boot-screensaver.service',
            'lcd-stable.service', 
            'lcd-glyph-locked.service',
            'lcd-button-switcher.service',
            'lcd-random.service'
        ]
        
        active_found = False
        
        for service in services:
            try:
                # Check if enabled
                enabled_result = subprocess.run(['systemctl', 'is-enabled', service], 
                                              capture_output=True, text=True)
                enabled = enabled_result.stdout.strip()
                
                # Check if active
                active_result = subprocess.run(['systemctl', 'is-active', service], 
                                             capture_output=True, text=True)
                active = active_result.stdout.strip()
                
                if enabled == 'enabled' or active == 'active':
                    status_icon = "🟢" if active == 'active' else "🟡"
                    print(f"{status_icon} {service}")
                    print(f"   Enabled: {enabled} | Active: {active}")
                    active_found = True
                    
                    if service == 'lcd-boot-screensaver.service' and active == 'active':
                        # Get more details about our custom service
                        try:
                            desc_result = subprocess.run(['systemctl', 'show', '-p', 'Description', service],
                                                       capture_output=True, text=True)
                            if desc_result.stdout:
                                desc = desc_result.stdout.split('=', 1)[1].strip()
                                print(f"   Description: {desc}")
                        except:
                            pass
            except:
                pass
        
        if not active_found:
            print("⚫ No LCD screensaver services are active or enabled")
        
        # Check running processes
        print("\n📱 RUNNING SCREENSAVER PROCESSES:")
        try:
            result = subprocess.run(['pgrep', '-af', 'python3.*\.py'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                screensaver_procs = [line for line in lines if any(name in line for name in 
                    ['glyph', 'matrix', 'rain', 'flame', 'plasma', 'dots', 'button'])]
                
                if screensaver_procs:
                    for proc in screensaver_procs:
                        print(f"🟢 {proc}")
                else:
                    print("⚫ No screensaver processes running")
            else:
                print("⚫ No Python processes found")
        except:
            print("❌ Could not check processes")

    def disable_all_boot(self):
        """Disable all auto-boot screensavers"""
        print("\n🛑 Disabling all auto-boot screensavers...")
        
        services = [
            'lcd-boot-screensaver.service',
            'lcd-stable.service', 
            'lcd-glyph-locked.service',
            'lcd-button-switcher.service',
            'lcd-random.service'
        ]
        
        stopped_count = 0
        for service in services:
            try:
                stop_result = subprocess.run(['sudo', 'systemctl', 'stop', service], capture_output=True)
                disable_result = subprocess.run(['sudo', 'systemctl', 'disable', service], capture_output=True)
                
                if stop_result.returncode == 0 or disable_result.returncode == 0:
                    print(f"  🛑 Disabled: {service}")
                    stopped_count += 1
            except:
                pass
        
        # Kill running screensaver processes
        try:
            subprocess.run(['pkill', '-f', 'glyph_rain'], capture_output=True)
            subprocess.run(['pkill', '-f', 'button_switcher'], capture_output=True) 
            subprocess.run(['pkill', '-f', 'screensaver'], capture_output=True)
            print("  🔄 Stopped running screensaver processes")
        except:
            pass
        
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
        
        print(f"✅ Disabled {stopped_count} services")
        print("   No screensavers will auto-start on boot")

    def show_service_logs(self):
        """Show recent service logs"""
        print("\n📋 RECENT SERVICE LOGS")
        print("="*40)
        
        try:
            result = subprocess.run(['sudo', 'journalctl', '-u', 'lcd-boot-screensaver.service', 
                                   '--no-pager', '-n', '10'], capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            else:
                print("No logs found for lcd-boot-screensaver.service")
        except Exception as e:
            print(f"Could not retrieve logs: {e}")

def main():
    manager = BootManager()
    
    while True:
        manager.show_menu()
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if not choice:
                continue
            
            choice_num = int(choice)
            
            if choice_num == 0:
                print("👋 Goodbye!")
                break
            
            elif choice_num == 95:
                manager.check_boot_status()
            
            elif choice_num == 96:
                manager.disable_all_boot()
            
            elif choice_num == 97:
                manager.show_service_logs()
            
            elif choice_num in manager.screensavers:
                manager.create_boot_service(choice_num)
            
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

if __name__ == "__main__":
    main()