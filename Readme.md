# Flappy Bird with Hand Control

Control a minimalist Flappy Bird clone using your hand tracked via webcam. Hand motion (moving your palm upward) triggers the bird to flap. The game includes a start menu and a game‑over screen with a **Try Again** button.

[https://github.com/yourname/flappy-hand-flappy](https://github.com/yourname/flappy-hand-flappy) (replace with your repo URL if you publish)

---

## ✨ Features

* **Hand‑controlled flaps** using `cvzone.HandTrackingModule` (MediaPipe under the hood)
* **Live webcam feed** window for visual feedback
* **Start** and **Try Again** buttons (mouse clickable)
* Procedurally generated pipes with moving obstacles and scoring
* Simple, dependency‑light Python stack

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

   ```bash
   pip install --upgrade pip
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

* **Hand Detection** (OpenCV) — mirrored webcam feed with hand landmarks.
* **Flappy Bird with Hand Flap** (Pygame) — the actual game.

Press **`q`** in the **Hand Detection** window to exit immediately.

---

## 🎮 How to Play

* From the **menu**, click **Start**.
* **Flap** by **moving your palm upward** (hand’s center Y decreases). The game looks for a sudden upward motion of \~20 pixels to trigger a jump.
* **Avoid pipes**. You score as the bird passes pipe pairs.
* If you collide or go out of bounds, the **Game Over** screen appears. Click **Try Again** to restart.

---

## 🛠️ Configuration

Tweak these constants near the top of the script to change gameplay feel:

```python
WIDTH, HEIGHT = 400, 600  # Window size
bird_radius = 10          # Player size
gravity = 0.5             # Fall speed per frame
jump_strength = -8        # Flap impulse (more negative = stronger jump)
pipe_width = 70           # Pipe thickness
pipe_gap = 150            # Vertical gap between pipes
pipe_speed = 3            # Pipe horizontal speed
pygame.time.set_timer(spawn_pipe_event,timeinmilis)
```