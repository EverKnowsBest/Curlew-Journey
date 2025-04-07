import pygame
import sys
from dialogueEngine import DialogueBox

pygame.init()
pygame.mixer.init()

# ==== CONFIG =====
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curlew Journey")

# Colors
BTN_COLOR = (139, 115, 85)
HOVER_COLOR = (100, 80, 60)
WHITE = (255, 255, 255)
PAPER = (222, 195, 142)

# Fonts & Sounds
font = pygame.font.SysFont("Papyrus", 22)
clickSound = pygame.mixer.Sound("click.wav")

# Load background image
bgImage = pygame.image.load("scene_bg.jpeg").convert()
bgImage = pygame.transform.scale(bgImage, (WIDTH, HEIGHT))

# ========== OBJECTS ==========

class Button:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False
        self.clicked = False

    def draw(self):
        color = HOVER_COLOR if self.hovered else BTN_COLOR
        rect = self.rect.inflate(10, 5) if self.clicked else self.rect
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)
        text = font.render(self.label, True, WHITE)
        textRect = text.get_rect(center=rect.center)
        screen.blit(text, textRect)

class Item:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.zooming = False
        self.zoomR = r
        self.darkOverlay = pygame.Surface((WIDTH, HEIGHT))
        self.darkOverlay.fill((0, 0, 0))
        self.darkOverlay.set_alpha(0)

    def draw(self):
        pygame.draw.circle(screen, (70, 70, 70), (self.x, self.y), self.zoomR)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.zoomR, 2)
        if self.zooming:
            screen.blit(self.darkOverlay, (0, 0))

    def update(self):
        if self.zooming and self.zoomR < 200:
            self.zoomR += 3
            self.darkOverlay.set_alpha(min(150, self.zoomR - 50))

    def isClicked(self, pos):
        dx, dy = pos[0] - self.x, pos[1] - self.y
        return dx * dx + dy * dy <= self.zoomR ** 2

# Create objects
buttons = [
    Button("Observe", 80, 500, 150, 50),
    Button("Approach", 300, 500, 150, 50),
    Button("Leave", 520, 500, 150, 50)
]
item = Item(WIDTH // 2, 250, 40)
dialogueBox = DialogueBox(font, (50, 400, 700, 100))

clock = pygame.time.Clock()

# ========== MAIN LOOP ==========
while True:
    screen.blit(bgImage, (0, 0))
    mousePos = pygame.mouse.get_pos()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            for b in buttons:
                b.hovered = b.rect.collidepoint(mousePos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dialogueBox.isActive():
                dialogueBox.handleClick()
                clickSound.play()
            else:
                for b in buttons:
                    if b.rect.collidepoint(mousePos):
                        b.clicked = True
                        clickSound.play()
                if item.isClicked(mousePos):
                    item.zooming = True
                    dialogueBox.startDialogue([
                        "You found an old binocular.",
                        "Through its cracked lens,",
                        "you see... something watching you.",
                        "It doesn’t blink."
                    ], speaker="Curlew")
                    clickSound.play()

        elif event.type == pygame.MOUSEBUTTONUP:
            for b in buttons:
                b.clicked = False

    # Update
    item.update()

    # Draw everything
    item.draw()
    for b in buttons:
        b.draw()
    dialogueBox.draw(screen)

    pygame.display.update()
    clock.tick(60)
