import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fast Boy Runner")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.w = 40
        self.h = 60
        self.x = 100
        self.y = HEIGHT - 100 - self.h
        self.vel_y = 0
        self.jumping = False
        self.gravity = 1
        self.jump_power = -18
        
    def jump(self):
        if not self.jumping:
            self.vel_y = self.jump_power
            self.jumping = True
    
    def update(self):
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Ground collision
        if self.y >= HEIGHT - 100 - self.h:
            self.y = HEIGHT - 100 - self.h
            self.vel_y = 0
            self.jumping = False
    
    def draw(self, surface):
        # Body
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.w, self.h))
        # Head
        pygame.draw.circle(surface, YELLOW, (self.x + self.w//2, self.y), 15)
        # Eyes
        pygame.draw.circle(surface, BLACK, (self.x + self.w//2 - 5, self.y - 2), 3)
        pygame.draw.circle(surface, BLACK, (self.x + self.w//2 + 5, self.y - 2), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Obstacle:
    def __init__(self):
        self.w = random.randint(30, 50)
        self.h = random.randint(40, 80)
        self.x = WIDTH
        self.y = HEIGHT - 100 - self.h
        self.speed = 7
        
    def update(self):
        self.x -= self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.w, self.h))
        # Add spikes on top
        for i in range(0, self.w, 10):
            pts = [(self.x + i, self.y), 
                   (self.x + i + 5, self.y - 10), 
                   (self.x + i + 10, self.y)]
            pygame.draw.polygon(surface, (200, 0, 0), pts)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
    
    def off_screen(self):
        return self.x < -self.w

class Coin:
    def __init__(self):
        self.r = 15
        self.x = WIDTH
        self.y = random.randint(150, HEIGHT - 150)
        self.speed = 7
        
    def update(self):
        self.x -= self.speed
    
    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.r)
        pygame.draw.circle(surface, (255, 215, 0), (self.x, self.y), self.r - 5)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
    
    def off_screen(self):
        return self.x < -self.r * 2

def draw_ground(surface):
    pygame.draw.rect(surface, GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # Add grass details
    for i in range(0, WIDTH, 20):
        pygame.draw.line(surface, (0, 200, 0), (i, HEIGHT - 100), (i, HEIGHT - 95), 2)

def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    player = Player()
    obstacles = []
    coins = []
    score = 0
    coin_count = 0
    obstacle_timer = 0
    coin_timer = 0
    game_over = False
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    # Restart game
                    player = Player()
                    obstacles = []
                    coins = []
                    score = 0
                    coin_count = 0
                    obstacle_timer = 0
                    coin_timer = 0
                    game_over = False
        
        if not game_over:
            # Update player
            player.update()
            
            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer > random.randint(60, 120):
                obstacles.append(Obstacle())
                obstacle_timer = 0
            
            # Spawn coins
            coin_timer += 1
            if coin_timer > random.randint(90, 150):
                coins.append(Coin())
                coin_timer = 0
            
            # Update obstacles
            for obs in obstacles[:]:
                obs.update()
                if obs.off_screen():
                    obstacles.remove(obs)
                    score += 10
                
                # Collision detection
                if player.get_rect().colliderect(obs.get_rect()):
                    game_over = True
            
            # Update coins
            for coin in coins[:]:
                coin.update()
                if coin.off_screen():
                    coins.remove(coin)
                
                # Coin collection
                if player.get_rect().colliderect(coin.get_rect()):
                    coins.remove(coin)
                    coin_count += 1
                    score += 5
        
        # Draw everything
        screen.fill(BLUE if not game_over else (150, 150, 150))
        draw_ground(screen)
        
        player.draw(screen)
        
        for obs in obstacles:
            obs.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
        
        # Draw score
        draw_text(screen, f"Score: {score}", 36, WIDTH // 2, 10)
        draw_text(screen, f"Coins: {coin_count}", 36, 100, 10)
        
        # Game over screen
        if game_over:
            draw_text(screen, "GAME OVER!", 72, WIDTH // 2, HEIGHT // 2 - 50, RED)
            draw_text(screen, f"Final Score: {score}", 48, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text(screen, "Press R to Restart", 36, WIDTH // 2, HEIGHT // 2 + 70)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
