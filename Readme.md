# Flappy Hand - Enhanced Edition

A beautiful, enhanced Flappy Bird clone controlled by hand gestures through your webcam. This enhanced version features flexible scaling, stunning visual effects, and an improved user experience.

---

## ✨ Enhanced Features

### 🎨 Visual Improvements
* **Dynamic screen scaling** - Automatically adapts to your screen resolution
* **Beautiful gradient backgrounds** with animated moving clouds
* **Enhanced bird design** with wing animations and gradient effects
* **3D-style pipes** with highlights and shadows
* **Particle effects** for flapping, scoring, and collisions
* **Modern UI** with shadowed buttons and glowing text effects
* **Smooth animations** throughout the game

### 🎮 Gameplay Enhancements
* **Hand-controlled flaps** using `cvzone.HandTrackingModule` (MediaPipe)
* **Live webcam feed** with enhanced visual feedback
* **Improved collision detection** with visual particle feedback
* **Better scoring system** with particle celebrations
* **Responsive controls** that adapt to screen size
* **Enhanced hand tracking indicators** in camera window

### 💻 Technical Improvements
* **Flexible resolution support** (600x400 to 1920x1080)
* **Scalable fonts and UI elements**
* **Better code organization** with type hints
* **Optimized performance** with efficient rendering

---

## 🧰 Tech Stack

* Python 3.8+
* [OpenCV](https://pypi.org/project/opencv-python/) for camera I/O and display
* [cvzone](https://pypi.org/project/cvzone/) + MediaPipe for hand tracking
* [Pygame](https://www.pygame.org/news) for the game loop, rendering, and UI

---

## 📦 Installation

> Tested on Windows 10/11. Should also work on macOS and Linux with a working webcam.

1. **Create and activate a virtual environment (recommended)**

   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # macOS/Linux (bash/zsh)
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**

   Using the requirements file:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install opencv-python cvzone mediapipe pygame
   ```

   If you have a headless/server environment, use `opencv-python-headless` instead of `opencv-python`.

3. **Save the game script** (e.g., `flappy_hand.py`) with the code in this repo.

---

## ▶️ Run

```bash
python flappy_hand.py
```

Two windows will appear:

* **Hand Detection** (OpenCV) — Enhanced webcam feed with hand tracking indicators, flap detection feedback, and game state display.
* **Flappy Hand - Enhanced Edition** (Pygame) — The beautifully rendered game with adaptive scaling.

Press **`q`** in the **Hand Detection** window to exit immediately.

---

## 🎮 How to Play

* From the **enhanced menu**, click **START GAME**.
* **Flap** by **moving your palm upward** quickly. You'll see visual feedback in the camera window.
* **Enjoy the visual effects** - particles appear when you flap, score, or collide.
* **Avoid the 3D-styled pipes** and watch your score with particle celebrations.
* The game automatically scales to your screen for the best experience.
* If you collide or go out of bounds, enjoy the enhanced **Game Over** screen and click **TRY AGAIN**.

---

## 🛠️ Configuration

The enhanced version automatically scales based on your screen size, but you can still tweak gameplay in the script:

```python
# The game now automatically calculates optimal resolution
DEFAULT_WIDTH, DEFAULT_HEIGHT = 800, 600  # Base resolution
MIN_WIDTH, MIN_HEIGHT = 600, 400          # Minimum supported
MAX_WIDTH, MAX_HEIGHT = 1920, 1080       # Maximum supported

# Gameplay variables (now scale automatically)
gravity = 0.4 * font_scale               # Adaptive gravity
jump_strength = -7 * font_scale           # Adaptive jump strength
pipe_gap = max(120, int(140 * font_scale)) # Adaptive pipe gap
pipe_speed = max(2, int(3 * font_scale))   # Adaptive speed
```

## 🎨 Visual Features

* **Gradient Sky**: Beautiful sky-to-horizon gradient background
* **Animated Clouds**: Parallax scrolling cloud effects
* **Enhanced Bird**: Wing animations with gradient coloring
* **3D Pipes**: Realistic pipe rendering with highlights and shadows
* **Particle Systems**: Flap particles, score celebrations, collision effects
* **Modern UI**: Shadowed buttons, glowing text, and responsive design
* **Adaptive Scaling**: Everything scales beautifully to your screen resolution

---

## 📋 Requirements

See `requirements.txt` for exact versions. The enhanced edition requires:
- Python 3.8+
- OpenCV for camera processing
- cvzone + MediaPipe for hand tracking
- Pygame for enhanced rendering and effects

---

## 🚀 What's New in Enhanced Edition

- ✅ Flexible screen scaling (600x400 to 1920x1080)
- ✅ Beautiful gradient backgrounds with animated clouds
- ✅ Enhanced bird with wing animations and effects
- ✅ 3D-style pipes with realistic rendering
- ✅ Particle effects for all interactions
- ✅ Modern UI with shadows and glowing effects
- ✅ Improved hand tracking feedback
- ✅ Better collision detection and visual feedback
- ✅ Scalable fonts and responsive design
- ✅ Performance optimizations