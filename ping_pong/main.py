import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 600, 600

pygame.init()

game_font = pygame.font.SysFont("comicsans", 40)

DELAY = 30

PADDLE_SPEED = 20

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

p1_x_pos = 10
p1_y_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2

p2_x_pos = WIDTH - PADDLE_WIDTH - 10
p2_y_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2

p1_score = 0
p2_score = 0

p1_up = False
p1_down = False
p2_up = False
p2_down = False

ball_x_pos = WIDTH // 2
ball_y_pos = HEIGHT // 2

ball_width = 8
ball_x_speed = -10
ball_y_speed = 0

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_object():
    pygame.draw.rect(WIN, WHITE, (p1_x_pos, p1_y_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (p2_x_pos, p2_y_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(WIN, WHITE, (ball_x_pos, ball_y_pos), ball_width)
    score = game_font.render(f"{p1_score} - {p2_score}", False, WHITE)
    WIN.blit(score, (WIDTH // 2 - score.get_width() // 2, 20))
    
def apply_player_movement():
    global p1_y_pos, p2_y_pos
    
    if p1_up:
        p1_y_pos = max(p1_y_pos - PADDLE_SPEED, 0)
    if p1_down:
        p1_y_pos = min(p1_y_pos + PADDLE_SPEED, HEIGHT - PADDLE_HEIGHT)
        
    if p2_up:
        p2_y_pos = max(p2_y_pos - PADDLE_SPEED, 0)
    if p2_down:
        p2_y_pos = min(p2_y_pos + PADDLE_SPEED, HEIGHT - PADDLE_HEIGHT)
        
def apply_ball_movement():
    global ball_x_pos, ball_y_pos, ball_x_speed, ball_y_speed, p1_score, p2_score
    
    if (
        (ball_x_pos + ball_x_speed < p1_x_pos + PADDLE_WIDTH) and
        (p1_y_pos < ball_y_pos + ball_y_speed < p1_y_pos + PADDLE_HEIGHT) 
        ):
        
        ball_x_speed = -ball_x_speed
        ball_y_speed = (p1_y_pos + PADDLE_HEIGHT // 2 - ball_y_pos) // 15
        ball_y_speed = -ball_y_speed
    elif ball_x_pos + ball_x_speed < 0:
        p2_score += 1
        ball_x_pos = WIDTH // 2
        ball_y_pos = HEIGHT // 2
        ball_x_speed = 10
        ball_y_speed = 0
    
    if (
        (ball_x_pos + ball_x_speed > p2_x_pos - PADDLE_WIDTH) and
        (p2_y_pos < ball_y_pos + ball_y_speed < p2_y_pos + PADDLE_HEIGHT)
    ):
        ball_x_speed = -ball_x_speed
        ball_y_speed = (p2_y_pos + PADDLE_HEIGHT // 2 - ball_y_pos) // 15
        ball_y_speed = -ball_y_speed
    elif ball_x_pos + ball_x_speed > HEIGHT:
        p1_score += 1
        ball_x_pos = WIDTH // 2
        ball_y_pos = HEIGHT // 2
        ball_x_speed = -10
        ball_y_speed = 0
        
    if ball_y_pos + ball_y_speed < 0 or ball_y_pos + ball_y_speed > HEIGHT:
        ball_y_speed = -ball_y_speed

    ball_x_pos += ball_x_speed
    ball_y_pos += ball_y_speed
    
pygame.display.set_caption("Ping Pong Game")
WIN.fill(BLACK)
pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                p1_up = True
            elif event.key == pygame.K_s:
                p1_down = True
            elif event.key == pygame.K_UP:
                p2_up = True
            elif event.key == pygame.K_DOWN:
                p2_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_up = False
            elif event.key == pygame.K_s:
                p1_down = False
            elif event.key == pygame.K_UP:
                p2_up = False
            elif event.key == pygame.K_DOWN:
                p2_down = False
    
    WIN.fill(BLACK)
    apply_player_movement()
    apply_ball_movement()
    draw_object()
    pygame.display.flip()
    pygame.time.wait(DELAY)