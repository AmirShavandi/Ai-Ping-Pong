import cv2
import numpy as np

# --- GAME SETTINGS ---
WIDTH, HEIGHT = 600, 600
PADDLE_W, PADDLE_H = 100, 20
BALL_RADIUS = 10

# Initialize Game State
ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
ball_vel = np.array([5, 5], dtype=float)
player_x = WIDTH // 2
ai_x = WIDTH // 2
score_player = 0
score_ai = 0

cap = cv2.VideoCapture(0)
tracker = None
bbox = None
tracking = False

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # --- 1. TRACKER LOGIC (YOUR ORIGINAL LOGIC) ---
    if tracking and bbox is not None:
        ok, bbox = tracker.update(frame)
        if ok:
            x, y, bw, bh = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

            # Map tracker X to Game X
            center_x = x + bw // 2
            player_x = int(np.interp(center_x, [0, w], [0, WIDTH]))
        else:
            cv2.putText(frame, "STATUS: Lost (Press 'r')", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # --- 2. PONG GAME ENGINE ---
    ball_pos += ball_vel

    # AI Paddle (Perfect tracking)
    ai_x = int(ball_pos[0])

    # Wall Bounce (Left/Right)
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_vel[0] *= -1

    # Paddle Collision: Player (Bottom)
    if ball_pos[1] >= HEIGHT - PADDLE_H - 10:
        if player_x - PADDLE_W // 2 < ball_pos[0] < player_x + PADDLE_W // 2:
            ball_vel[1] *= -1.05  # Speed up ball on hit
            ball_pos[1] = HEIGHT - PADDLE_H - 11

    # Paddle Collision: AI (Top)
    if ball_pos[1] <= PADDLE_H + 10:
        if ai_x - PADDLE_W // 2 < ball_pos[0] < ai_x + PADDLE_W // 2:
            ball_vel[1] *= -1
            ball_pos[1] = PADDLE_H + 11

    # Scoring Logic
    if ball_pos[1] < 0:
        score_player += 1
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
        ball_vel = np.array([5, 5], dtype=float)
    elif ball_pos[1] > HEIGHT:
        score_ai += 1
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
        ball_vel = np.array([-5, -5], dtype=float)

    # --- 3. RENDERING ---
    # Create the game screen
    game_screen = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Draw Paddles
    cv2.rectangle(game_screen, (player_x - PADDLE_W // 2, HEIGHT - PADDLE_H - 5),
                  (player_x + PADDLE_W // 2, HEIGHT - 5), (0, 255, 0), -1)
    cv2.rectangle(game_screen, (ai_x - PADDLE_W // 2, 5),
                  (ai_x + PADDLE_W // 2, PADDLE_H + 5), (0, 0, 255), -1)

    # Draw Ball
    cv2.circle(game_screen, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS, (255, 255, 255), -1)

    # Show Scores
    cv2.putText(game_screen, f"AI: {score_ai}  YOU: {score_player}", (10, HEIGHT // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display Windows
    cv2.imshow("Object Tracker", frame)
    cv2.imshow("Pong Game", game_screen)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("r"):
        new_bbox = cv2.selectROI("Object Tracker", frame, fromCenter=False, showCrosshair=True)
        if new_bbox[2] > 0 and new_bbox[3] > 0:
            bbox = new_bbox
            tracker = cv2.legacy.TrackerMOSSE_create()
            tracker.init(frame, bbox)
            tracking = True

cap.release()
cv2.destroyAllWindows()