import pygame
import random

# Inicializar o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Atirar em Aliens")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Jogador
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Projetil
bullet_width, bullet_height = 5, 10
bullet_speed = -7
bullets = []

# Alienígenas
alien_width, alien_height = 50, 40
alien_speed = 2
aliens = []

# Gerar aliens
def generate_aliens(num_aliens):
    for _ in range(num_aliens):
        x = random.randint(0, WIDTH - alien_width)
        y = random.randint(-100, -40)
        aliens.append(pygame.Rect(x, y, alien_width, alien_height))

generate_aliens(5)

# Função principal do jogo
def game_loop():
    global player_x, player_y
    running = True
    score = 0

    while running:
        screen.fill(BLACK)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimento do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:  # Atirar
            if len(bullets) < 3:  # Limite de balas na tela
                bullets.append(pygame.Rect(player_x + player_width // 2, player_y, bullet_width, bullet_height))

        # Atualizar balas
        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Atualizar aliens
        for alien in aliens[:]:
            alien.y += alien_speed
            if alien.y > HEIGHT:  # Alien chegou ao fundo
                running = False  # Fim do jogo
            for bullet in bullets[:]:
                if alien.colliderect(bullet):  # Verificar colisão
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    score += 1

        # Gerar novos aliens se todos forem destruídos
        if not aliens:
            generate_aliens(5)

        # Desenhar jogador
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Desenhar balas
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Desenhar aliens
        for alien in aliens:
            pygame.draw.rect(screen, RED, alien)

        # Mostrar pontuação
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(FPS)

    # Fim do jogo
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 36))
    pygame.display.flip()
    pygame.time.wait(3000)

# Executar o jogo
game_loop()
pygame.quit()
