import cv2
from cvzone.HandTrackingModule import HandDetector
import pygame
import random
import sys
import math
from typing import List, Tuple

# -----------------------------
# Hand Detector Setup (cvzone)
# -----------------------------
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

# -----------------------------
# Flappy Bird Game Setup
# -----------------------------
pygame.init()

# Flexible resolution support
DEFAULT_WIDTH, DEFAULT_HEIGHT = 800, 600
MIN_WIDTH, MIN_HEIGHT = 600, 400
MAX_WIDTH, MAX_HEIGHT = 1920, 1080

# Get monitor resolution for scaling
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Calculate optimal resolution
scale_factor = min(screen_width / DEFAULT_WIDTH, screen_height / DEFAULT_HEIGHT) * 0.8
WIDTH = int(DEFAULT_WIDTH * scale_factor)
HEIGHT = int(DEFAULT_HEIGHT * scale_factor)

# Ensure minimum resolution
WIDTH = max(MIN_WIDTH, min(MAX_WIDTH, WIDTH))
HEIGHT = max(MIN_HEIGHT, min(MAX_HEIGHT, HEIGHT))

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Hand - Enhanced Edition")

clock = pygame.time.Clock()

# Scalable fonts
font_scale = min(WIDTH, HEIGHT) / 600
font_size_small = max(16, int(20 * font_scale))
font_size_medium = max(24, int(32 * font_scale))
font_size_large = max(32, int(48 * font_scale))
font_size_xlarge = max(48, int(64 * font_scale))

font_small = pygame.font.SysFont("Arial", font_size_small)
font = pygame.font.SysFont("Arial", font_size_medium)
big_font = pygame.font.SysFont("Arial", font_size_large)
title_font = pygame.font.SysFont("Arial", font_size_xlarge, bold=True)

# Enhanced color palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
DEEP_BLUE = (70, 130, 180)
SUN_YELLOW = (255, 215, 0)
CLOUD_WHITE = (248, 248, 255)
GREEN_LIGHT = (144, 238, 144)
GREEN_DARK = (34, 139, 34)
PIPE_GREEN = (46, 125, 50)
PIPE_HIGHLIGHT = (76, 175, 80)
BIRD_YELLOW = (255, 193, 7)
BIRD_ORANGE = (255, 152, 0)
RED = (244, 67, 54)
BUTTON_PRIMARY = (33, 150, 243)
BUTTON_HOVER = (21, 101, 192)
SHADOW = (0, 0, 0, 80)
PARTICLE_COLORS = [(255, 215, 0), (255, 140, 0), (255, 69, 0), (255, 20, 147)]

# Scalable game variables
bird_x = WIDTH * 0.15
bird_radius = max(8, int(12 * font_scale))
gravity = 0.4 * font_scale
jump_strength = -7 * font_scale

# Pipes (scalable)
pipe_width = max(50, int(70 * font_scale))
pipe_gap = max(200, int(140 * font_scale))
pipe_speed = max(2, int(3 * font_scale))
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 4500)

# Animation and effects
frame_count = 0
background_offset = 0
clouds = []
particles = []
for i in range(3):
    clouds.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(50, HEIGHT // 3),
        'size': random.randint(30, 80) * font_scale,
        'speed': random.uniform(0.2, 0.8) * font_scale
    })

# Game State
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
state = STATE_MENU

# Initialize game variables
bird_y = HEIGHT // 2
bird_movement = 0
pipes = []
score = 0
last_y = None
flap_triggered = False

# Variables that reset each game
def reset_game():
    global bird_y, bird_movement, pipes, score, last_y, flap_triggered, particles
    bird_y = HEIGHT // 2
    bird_movement = 0
    pipes = []
    score = 0
    last_y = None
    flap_triggered = False
    particles = []

# Initialize the game
reset_game()

# -----------------------------
# Enhanced Drawing Helpers
# -----------------------------
def create_gradient_surface(width: int, height: int, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> pygame.Surface:
    """Create a vertical gradient surface"""
    gradient = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(gradient, (r, g, b), (0, y), (width, y))
    return gradient

def draw_cloud(surface: pygame.Surface, x: int, y: int, size: float) -> None:
    """Draw an animated cloud"""
    cloud_color = CLOUD_WHITE
    shadow_color = (200, 200, 200)
    
    # Shadow
    pygame.draw.circle(surface, shadow_color, (int(x + 2), int(y + 2)), int(size * 0.6))
    pygame.draw.circle(surface, shadow_color, (int(x + size * 0.8 + 2), int(y + 2)), int(size * 0.5))
    pygame.draw.circle(surface, shadow_color, (int(x + size * 1.2 + 2), int(y + size * 0.3 + 2)), int(size * 0.4))
    
    # Cloud
    pygame.draw.circle(surface, cloud_color, (int(x), int(y)), int(size * 0.6))
    pygame.draw.circle(surface, cloud_color, (int(x + size * 0.8), int(y)), int(size * 0.5))
    pygame.draw.circle(surface, cloud_color, (int(x + size * 1.2), int(y + size * 0.3)), int(size * 0.4))

def draw_bird_enhanced(surface: pygame.Surface, x: int, y: int, radius: int, flap_offset: float = 0) -> None:
    """Draw an enhanced bird with wing animation"""
    # Bird body (gradient effect)
    body_color1 = BIRD_YELLOW
    body_color2 = BIRD_ORANGE
    
    # Draw body shadow
    pygame.draw.circle(surface, (0, 0, 0, 50), (int(x + 2), int(y + 2)), radius)
    
    # Draw body with gradient effect
    for i in range(radius):
        ratio = i / radius
        r = int(body_color1[0] * (1 - ratio) + body_color2[0] * ratio)
        g = int(body_color1[1] * (1 - ratio) + body_color2[1] * ratio)
        b = int(body_color1[2] * (1 - ratio) + body_color2[2] * ratio)
        pygame.draw.circle(surface, (r, g, b), (int(x), int(y)), radius - i)
    
    # Draw wings (animated)
    wing_offset = math.sin(flap_offset) * 3
    wing_color = (255, 165, 0)
    
    # Left wing
    wing_points = [
        (x - radius//2, y - radius//3 + wing_offset),
        (x - radius*1.5, y - radius + wing_offset),
        (x - radius, y + wing_offset),
        (x - radius//3, y + radius//3 + wing_offset)
    ]
    pygame.draw.polygon(surface, wing_color, wing_points)
    
    # Right wing
    wing_points_r = [
        (x + radius//2, y - radius//3 + wing_offset),
        (x + radius*1.5, y - radius + wing_offset),
        (x + radius, y + wing_offset),
        (x + radius//3, y + radius//3 + wing_offset)
    ]
    pygame.draw.polygon(surface, wing_color, wing_points_r)
    
    # Draw beak
    beak_points = [
        (x + radius, y),
        (x + radius * 1.5, y - radius//4),
        (x + radius * 1.5, y + radius//4)
    ]
    pygame.draw.polygon(surface, BIRD_ORANGE, beak_points)
    
    # Draw eye
    eye_x = x + radius//3
    eye_y = y - radius//3
    pygame.draw.circle(surface, WHITE, (int(eye_x), int(eye_y)), radius//3)
    pygame.draw.circle(surface, BLACK, (int(eye_x + radius//6), int(eye_y)), radius//6)

def draw_pipe_enhanced(surface: pygame.Surface, pipe_rect: pygame.Rect) -> None:
    """Draw an enhanced pipe with 3D effect"""
    # Main pipe body
    pygame.draw.rect(surface, PIPE_GREEN, pipe_rect)
    
    # Highlight (left side)
    highlight_rect = pygame.Rect(pipe_rect.x, pipe_rect.y, pipe_rect.width // 4, pipe_rect.height)
    pygame.draw.rect(surface, PIPE_HIGHLIGHT, highlight_rect)
    
    # Shadow (right side)
    shadow_rect = pygame.Rect(pipe_rect.x + pipe_rect.width * 3//4, pipe_rect.y, pipe_rect.width // 4, pipe_rect.height)
    pygame.draw.rect(surface, (20, 69, 24), shadow_rect)
    
    # Pipe cap (if it's the top or bottom of screen)
    if pipe_rect.y == 0:  # Top pipe
        cap_rect = pygame.Rect(pipe_rect.x - 5, pipe_rect.bottom - 20, pipe_rect.width + 10, 20)
        pygame.draw.rect(surface, PIPE_HIGHLIGHT, cap_rect)
        pygame.draw.rect(surface, (20, 69, 24), pygame.Rect(cap_rect.x + cap_rect.width * 3//4, cap_rect.y, cap_rect.width // 4, cap_rect.height))
    elif pipe_rect.bottom >= HEIGHT - 10:  # Bottom pipe
        cap_rect = pygame.Rect(pipe_rect.x - 5, pipe_rect.y, pipe_rect.width + 10, 20)
        pygame.draw.rect(surface, PIPE_HIGHLIGHT, cap_rect)
        pygame.draw.rect(surface, (20, 69, 24), pygame.Rect(cap_rect.x + cap_rect.width * 3//4, cap_rect.y, cap_rect.width // 4, cap_rect.height))

def update_particles() -> None:
    """Update particle effects"""
    global particles
    
    # Update existing particles
    for particle in particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.1  # gravity
        particle['life'] -= 1
        particle['size'] = max(0, particle['size'] - 0.1)
        
        if particle['life'] <= 0 or particle['size'] <= 0:
            particles.remove(particle)

def add_flap_particles(x: int, y: int) -> None:
    """Add particles when bird flaps"""
    for _ in range(8):
        particles.append({
            'x': x + random.randint(-5, 5),
            'y': y + random.randint(-5, 5),
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-3, -1),
            'color': random.choice(PARTICLE_COLORS),
            'size': random.uniform(2, 5),
            'life': random.randint(20, 40)
        })

def draw_particles(surface: pygame.Surface) -> None:
    """Draw particle effects"""
    for particle in particles:
        alpha = min(255, particle['life'] * 8)
        color = (*particle['color'], alpha)
        pos = (int(particle['x']), int(particle['y']))
        size = max(1, int(particle['size']))
        
        # Create a surface with per-pixel alpha
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, color, (size, size), size)
        surface.blit(particle_surf, (pos[0] - size, pos[1] - size))

def draw_background() -> None:
    """Draw animated background with gradient and clouds"""
    global background_offset, clouds, frame_count
    
    # Sky gradient
    gradient = create_gradient_surface(WIDTH, HEIGHT, SKY_BLUE, DEEP_BLUE)
    win.blit(gradient, (0, 0))
    
    # Animated clouds
    for cloud in clouds:
        cloud['x'] -= cloud['speed']
        if cloud['x'] < -cloud['size'] * 2:
            cloud['x'] = WIDTH + cloud['size']
            cloud['y'] = random.randint(50, HEIGHT // 3)
        
        draw_cloud(win, cloud['x'], cloud['y'], cloud['size'])
    
    # Simple ground
    ground_height = 30
    ground_rect = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)
    pygame.draw.rect(win, GREEN_DARK, ground_rect)
    pygame.draw.rect(win, GREEN_LIGHT, pygame.Rect(0, HEIGHT - ground_height, WIDTH, 5))
    
    frame_count += 1
def draw_window():
    draw_background()
    
    # Update and draw particles
    update_particles()
    draw_particles(win)
    
    # Draw pipes with enhanced design
    for pipe in pipes:
        draw_pipe_enhanced(win, pipe)
    
    # Draw bird with animation
    flap_animation = frame_count * 0.3
    draw_bird_enhanced(win, int(bird_x), int(bird_y), bird_radius, flap_animation)
    
    # Draw score with shadow effect
    score_text = big_font.render(str(int(score)), True, WHITE)
    shadow_text = big_font.render(str(int(score)), True, BLACK)
    
    score_x = WIDTH // 2 - score_text.get_width() // 2
    score_y = 30
    
    # Draw shadow
    win.blit(shadow_text, (score_x + 2, score_y + 2))
    # Draw main text
    win.blit(score_text, (score_x, score_y))
    
    pygame.display.update()

def draw_button(text: str, x: int, y: int, w: int, h: int, color: Tuple[int, int, int], hover_color: Tuple[int, int, int]) -> bool:
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    
    # Button shadow
    shadow_rect = pygame.Rect(x + 3, y + 3, w, h)
    pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect)
    
    # Button background
    if rect.collidepoint(mouse):
        pygame.draw.rect(win, hover_color, rect)
        pygame.draw.rect(win, WHITE, rect, 3)  # Hover border
        if click[0] == 1:  # Left mouse click
            return True
    else:
        pygame.draw.rect(win, color, rect)
        pygame.draw.rect(win, (200, 200, 200), rect, 2)  # Normal border
    
    # Button text with shadow
    label = font.render(text, True, BLACK)
    shadow_label = font.render(text, True, (100, 100, 100))
    
    text_x = x + (w - label.get_width()) // 2
    text_y = y + (h - label.get_height()) // 2
    
    win.blit(shadow_label, (text_x + 1, text_y + 1))
    win.blit(label, (text_x, text_y))
    
    return False

def draw_menu():
    draw_background()
    
    # Title with glow effect
    title_text = "Flappy Hand"
    subtitle_text = "Enhanced Edition"
    
    # Title shadow/glow
    for offset in [(4, 4), (2, 2), (0, 0)]:
        color = BLACK if offset == (4, 4) else (100, 100, 100) if offset == (2, 2) else WHITE
        title = title_font.render(title_text, True, color)
        title_x = WIDTH // 2 - title.get_width() // 2 + offset[0]
        title_y = HEIGHT // 4 + offset[1]
        win.blit(title, (title_x, title_y))
    
    # Subtitle
    subtitle = font.render(subtitle_text, True, SUN_YELLOW)
    subtitle_x = WIDTH // 2 - subtitle.get_width() // 2
    subtitle_y = HEIGHT // 4 + title_font.get_height() + 10
    win.blit(subtitle, (subtitle_x, subtitle_y))
    
    # Instructions
    instructions = [
        "Move your hand UP to flap!",
        "Make sure your webcam is working",
        "Press 'q' in camera window to quit"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font_small.render(instruction, True, WHITE)
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - 60 + i * 25
        win.blit(text, (text_x, text_y))
    
    # Start button
    button_width = max(150, int(200 * font_scale))
    button_height = max(50, int(70 * font_scale))
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 50
    
    if draw_button("START GAME", button_x, button_y, button_width, button_height, BUTTON_PRIMARY, BUTTON_HOVER):
        return True
    
    pygame.display.update()
    return False

def draw_game_over():
    draw_background()
    
    # Game over text with effects
    over_text = "GAME OVER"
    
    # Text shadow/glow effect
    for offset in [(3, 3), (1, 1), (0, 0)]:
        color = BLACK if offset == (3, 3) else RED if offset == (1, 1) else WHITE
        text = big_font.render(over_text, True, color)
        text_x = WIDTH // 2 - text.get_width() // 2 + offset[0]
        text_y = HEIGHT // 4 + offset[1]
        win.blit(text, (text_x, text_y))
    
    # Score display
    score_display = f"Your Score: {int(score)}"
    score_text = font.render(score_display, True, SUN_YELLOW)
    score_x = WIDTH // 2 - score_text.get_width() // 2
    score_y = HEIGHT // 2 - 60
    win.blit(score_text, (score_x, score_y))
    
    # High score (placeholder for future enhancement)
    high_score_text = font_small.render("Keep practicing to improve!", True, WHITE)
    high_score_x = WIDTH // 2 - high_score_text.get_width() // 2
    high_score_y = score_y + 40
    win.blit(high_score_text, (high_score_x, high_score_y))
    
    # Try again button
    button_width = max(150, int(200 * font_scale))
    button_height = max(50, int(70 * font_scale))
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 40
    
    if draw_button("TRY AGAIN", button_x, button_y, button_width, button_height, BUTTON_PRIMARY, BUTTON_HOVER):
        return True
    
    pygame.display.update()
    return False

# -----------------------------
# Main Loop
# -----------------------------
running = True
while running:
    clock.tick(30)

    # ---------------- Camera Hand Detection ----------------
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if state == STATE_PLAYING and hands:
        hand = hands[0]
        center = hand["center"]

        if last_y is not None:
            if last_y - center[1] > 20:  # palm moved UP
                flap_triggered = True
                # Visual feedback on hand detection window
                cv2.circle(img, center, 20, (0, 255, 0), 3)
                cv2.putText(img, "FLAP!", (center[0] - 30, center[1] - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        last_y = center[1]
        
        # Draw hand tracking indicator
        cv2.circle(img, center, 10, (255, 0, 0), -1)
        cv2.putText(img, f"Hand Y: {center[1]}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Add game state indicator on camera feed
    state_text = f"State: {state.upper()}"
    score_text = f"Score: {int(score)}"
    cv2.putText(img, state_text, (10, img.shape[0] - 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(img, score_text, (10, img.shape[0] - 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Hand Detection", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # ---------------- Pygame Events ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == spawn_pipe_event and state == STATE_PLAYING:
            height = random.randint(100, 400)
            pipes.append(pygame.Rect(WIDTH, 0, pipe_width, height))
            pipes.append(pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap))

    # ---------------- Game States ----------------
    if state == STATE_MENU:
        if draw_menu():
            reset_game()
            state = STATE_PLAYING

    elif state == STATE_PLAYING:
        # Bird movement
        bird_movement += gravity
        bird_y += bird_movement

        if flap_triggered:
            bird_movement = jump_strength
            flap_triggered = False
            # Add particle effect when flapping
            add_flap_particles(int(bird_x), int(bird_y))

        # Pipe movement
        for pipe in pipes:
            pipe.x -= pipe_speed

        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Collision detection with better visual feedback
        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
        collision_detected = False
        
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                collision_detected = True
                # Add collision particles
                for _ in range(15):
                    particles.append({
                        'x': bird_x + random.randint(-10, 10),
                        'y': bird_y + random.randint(-10, 10),
                        'vx': random.uniform(-4, 4),
                        'vy': random.uniform(-4, 4),
                        'color': RED,
                        'size': random.uniform(3, 8),
                        'life': random.randint(30, 60)
                    })
                break
        
        if collision_detected or bird_y > HEIGHT - 30 or bird_y < 0:
            state = STATE_GAME_OVER

        # Score update with better detection
        for pipe in pipes:
            if pipe.x + pipe.width < bird_x and pipe.x + pipe.width + pipe_speed >= bird_x:
                if pipe.y == 0:  # Only count top pipes to avoid double counting
                    score += 1
                    # Add score particles
                    for _ in range(5):
                        particles.append({
                            'x': bird_x + random.randint(-5, 5),
                            'y': bird_y + random.randint(-15, -5),
                            'vx': random.uniform(-1, 1),
                            'vy': random.uniform(-2, -1),
                            'color': SUN_YELLOW,
                            'size': random.uniform(4, 7),
                            'life': random.randint(40, 80)
                        })

        draw_window()

    elif state == STATE_GAME_OVER:
        if draw_game_over():
            reset_game()
            state = STATE_PLAYING

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
