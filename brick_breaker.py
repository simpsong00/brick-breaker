import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_SIZE = 15
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS = 5
BRICK_COLS = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_COLOR = (100, 100, 100)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 8

    def move(self, direction):
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(WIDTH - PADDLE_WIDTH, self.rect.x))

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

class Ball:
    def __init__(self):
        self.reset()
        self.color = WHITE

    def reset(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + 2) + 1
            y = (row + 2) * (BRICK_HEIGHT + 2) + 1
            color = random.choice(COLORS)
            bricks.append(Brick(x, y, color))
    return bricks

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    game_over = False
    score = 0  # Score system: 10 points per brick destroyed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    ball.reset()
                    bricks = create_bricks()
                    score = 0  # Reset score

        if not game_over:
            # Move paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-1)
            if keys[pygame.K_RIGHT]:
                paddle.move(1)

            # Move ball
            ball.move()

            # Paddle collision
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1
                # Change ball direction based on where it hits the paddle
                relative_intersect_x = (paddle.rect.centerx - ball.rect.centerx) / (PADDLE_WIDTH/2)
                ball.dx = -relative_intersect_x * 5

            # Brick collision
            for brick in bricks:
                if brick.active and ball.rect.colliderect(brick.rect):
                    brick.active = False
                    ball.dy *= -1
                    ball.color = brick.color
                    score += 10  # Add points for each brick
                    break

            # Check if ball is below paddle
            if ball.rect.top > HEIGHT:
                game_over = True

            # Check if all bricks are destroyed
            if all(not brick.active for brick in bricks):
                game_over = True

        # Draw everything
        screen.fill(BLACK)
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 