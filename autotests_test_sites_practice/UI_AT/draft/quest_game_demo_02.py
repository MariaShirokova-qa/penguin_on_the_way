import pygame

# Создаём окно
screen = pygame.display.set_mode((800, 600))

# Текст диалога
font = pygame.font.SysFont('Arial', 24)
text = font.render("Что ты хочешь сделать?", True, (255, 255, 255))

# Кнопки выбора
button1 = pygame.Rect(100, 200, 200, 50)
button2 = pygame.Rect(100, 300, 200, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                print("Выбран вариант 1")
            elif button2.collidepoint(event.pos):
                print("Выбран вариант 2")

    screen.fill((0, 0, 0))
    screen.blit(text, (100, 100))
    pygame.draw.rect(screen, (255, 0, 0), button1)
    pygame.draw.rect(screen, (0, 0, 255), button2)
    pygame.display.flip()

pygame.quit()