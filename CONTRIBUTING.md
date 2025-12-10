# 🌈 Contributing to Psychedelic M5 Screensavers

Thank you for your interest in contributing! This project welcomes contributions from the community.

## 🎨 **How to Contribute**

### 🚀 **Adding New Screensavers**
1. **Fork** the repository
2. **Create** a new screensaver function following the existing pattern:
   ```cpp
   void drawYourScreensaver() {
     // Your amazing visualization code here
     // Use HSV colors for psychedelic effects
     // Optimize for M5StickC Plus2 performance
   }
   ```
3. **Add** your screensaver to the enum and switch statement
4. **Test** thoroughly on real hardware
5. **Submit** a pull request

### 📚 **Documentation**
- Improve README files
- Add screensaver descriptions
- Create tutorials
- Fix typos and grammar

### 🐛 **Bug Fixes**
- Report bugs with detailed descriptions
- Include hardware version and symptoms
- Test fixes on real M5StickC Plus2 devices

### ⚡ **Performance Improvements**
- Optimize existing screensavers
- Reduce memory usage
- Improve frame rates
- Better math algorithms

## 🎯 **Screensaver Guidelines**

### ✅ **Good Screensavers:**
- **Mathematical beauty** - fractals, curves, patterns
- **Psychedelic effects** - color cycling, flowing motion
- **Optimized performance** - smooth 60fps
- **Embedded-friendly** - integer math, lookup tables
- **Visually stunning** - mesmerizing and hypnotic

### ❌ **Avoid:**
- **Text-heavy** displays (this is visual art)
- **Static** images (needs animation)
- **Performance hogs** (keep it smooth)
- **Flashing** effects (seizure concerns)
- **Copyrighted** content

## 🛠️ **Development Setup**

### **Requirements:**
- **PlatformIO IDE** (VS Code recommended)
- **M5StickC Plus2** hardware for testing
- **Git** for version control

### **Quick Start:**
```bash
git clone [your-fork]
cd Psychedelic-M5-Screensavers
pio run --target upload
```

### **Testing:**
- Always test on real hardware
- Check all button controls work
- Verify smooth animation
- Test memory usage

## 🎨 **Code Style**

### **Naming:**
- Functions: `drawScreensaverName()`
- Variables: `camelCase`
- Constants: `UPPER_CASE`

### **Comments:**
- Explain mathematical concepts
- Document optimization tricks
- Credit inspiration sources

### **Performance:**
- Use integer math when possible
- Implement lookup tables for trigonometry
- Minimize dynamic memory allocation
- Profile memory usage

## 🌟 **Ideas for New Screensavers**

### 🔬 **Mathematical:**
- Lorenz attractors
- L-systems (plant growth)
- Cellular automata
- Fourier transforms
- Prime number visualizations

### 🎭 **Visual Effects:**
- Lissajous curves
- Möbius strips
- Hypocycles and epicycles
- Interference patterns
- Diffusion-limited aggregation

### 🌊 **Natural Phenomena:**
- Lightning simulation
- Galaxy formation
- Crystal growth
- Fluid dynamics
- Aurora borealis

## 📋 **Pull Request Process**

1. **Fork** and create feature branch
2. **Implement** your screensaver
3. **Test** thoroughly on hardware
4. **Document** your addition
5. **Submit** pull request with:
   - Clear description
   - Screenshots/videos if possible
   - Performance notes
   - Mathematical explanation (if applicable)

## 🎯 **Community Guidelines**

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** about embedded graphics
- **Celebrate creativity** in all forms
- **Keep it psychedelic** and fun!

## 🏆 **Recognition**

Contributors will be:
- Listed in README credits
- Featured in release notes
- Acknowledged in documentation
- Celebrated in the community

## 📞 **Get Help**

- **Issues tab** for bug reports
- **Discussions** for questions
- **Documentation** for guides
- **Code comments** for implementation details

---

**Together, let's create the most amazing screensaver collection for M5Stack!** 🌈✨

*Every contribution makes the psychedelic experience better for everyone!*