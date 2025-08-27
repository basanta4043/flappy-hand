import cv2
from cvzone.HandTrackingModule import HandDetector
import pygame
import random
import sys

# -----------------------------
# Hand Detector Setup (cvzone)
# -----------------------------
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

# -----------------------------
# Flappy Bird Game Setup
# -----------------------------
pygame.init()
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Hand Flap")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 48)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (200, 50, 50)

# Bird variables
bird_x = 50
bird_radius = 10
gravity = 0.5
jump_strength = -8

# Pipes
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 3000)

# Game State
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
state = STATE_MENU

# Variables that reset each game
def reset_game():
    global bird_y, bird_movement, pipes, score, last_y, flap_triggered
    bird_y = HEIGHT // 2
    bird_movement = 0
    pipes = []
    score = 0
    last_y = None
    flap_triggered = False

reset_game()

# -----------------------------
# Drawing helpers
# -----------------------------
def draw_window():
    win.fill(BLUE)

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(win, GREEN, pipe)

    # Draw bird
    pygame.draw.circle(win, WHITE, (bird_x, int(bird_y)), bird_radius)

    # Score
    score_text = font.render(str(int(score)), True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(win, hover_color, rect)
        if click[0] == 1:  # Left mouse click
            return True
    else:
        pygame.draw.rect(win, color, rect)

    label = font.render(text, True, WHITE)
    win.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return False

def draw_menu():
    win.fill(BLUE)
    title = big_font.render("Flappy Bird", True, WHITE)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    if draw_button("Start", WIDTH // 2 - 75, HEIGHT // 2, 150, 60, GREEN, (0, 255, 0)):
        return True

    pygame.display.update()
    return False

def draw_game_over():
    win.fill(BLUE)
    over_text = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)

    win.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 4))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))

    if draw_button("Try Again", WIDTH // 2 - 75, HEIGHT // 2, 150, 60, GREEN, (0, 255, 0)):
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
        last_y = center[1]

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

        # Pipe movement
        for pipe in pipes:
            pipe.x -= pipe_speed

        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Collision
        for pipe in pipes:
            if pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2).colliderect(pipe):
                state = STATE_GAME_OVER

        if bird_y > HEIGHT or bird_y < 0:
            state = STATE_GAME_OVER

        # Score update
        for pipe in pipes:
            if pipe.x + pipe.width == bird_x:
                score += 0.5

        draw_window()

    elif state == STATE_GAME_OVER:
        if draw_game_over():
            reset_game()
            state = STATE_PLAYING

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
