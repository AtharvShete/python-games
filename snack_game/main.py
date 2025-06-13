import pygame
import random

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Snack Game")

clock = pygame.time.Clock()

SNACK_SIZE = 10
SNACK_SPEED = 15

message_font = pygame.font.SysFont("comicsans", 40)
score_font = pygame.font.SysFont("comicsans", 30)

def print_score(score):
    text = score_font.render(f"Score: {score}", True, ORANGE)
    WIN.blit(text, (10, 10))
    
def draw_snack(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(WIN, WHITE, (pixel[0], pixel[1], snake_size, snake_size))

def main():
    
    game_over = False
    game_close = False
    
    x = WIDTH // 2
    y = HEIGHT // 2
    
    x_speed = 0
    y_speed = 0
    
    snake_pixels = []
    
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - SNACK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNACK_SIZE) / 10.0) * 10.0
    
    while not game_over:
        
        while game_close:
            WIN.fill(BLACK)
            game_over_message1 = message_font.render("Game Over!", True, RED)
            game_over_message2 = message_font.render("Press SPACE to Restart or ESC to Quit", True, RED)
            WIN.blit(game_over_message1, (WIDTH // 2 - game_over_message1.get_width() // 2, HEIGHT // 2 - 40))
            WIN.blit(game_over_message2, (WIDTH // 2 - game_over_message2.get_width() // 2, HEIGHT // 2 + 10))
            print_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        main()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_speed = -SNACK_SIZE
                    y_speed = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_speed = SNACK_SIZE
                    y_speed = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_speed = -SNACK_SIZE
                    x_speed = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_speed = SNACK_SIZE
                    x_speed = 0
                    
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        
        x += x_speed
        y += y_speed
        
        WIN.fill(BLACK)
        pygame.draw.rect(WIN, RED, (food_x, food_y, SNACK_SIZE, SNACK_SIZE))
        
        snake_pixels.append([x, y])
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True
        
        draw_snack(SNACK_SIZE, snake_pixels)
        print_score(snake_length - 1)
        
        pygame.display.update()
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNACK_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNACK_SIZE) / 10.0) * 10.0
            snake_length += 1
            
        clock.tick(SNACK_SPEED)
        
    pygame.quit()
    
if __name__ == "__main__":
    main()
    pygame.quit()
    quit()