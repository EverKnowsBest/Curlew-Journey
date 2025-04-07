import pygame

class DialogueBox:
    def __init__(self, font, boxRect, padding=20):
        self.font = font
        self.boxRect = pygame.Rect(boxRect)
        self.padding = padding
        self.dialogue = []  # initialize empty list
        self.speaker = None # speaker name
        self.index = -1   # set -1 to inactive
        self.active = False

    def startDialogue(self, lines, speaker=None):
        self.dialogue = lines
        self.speaker = speaker
        self.index = 0
        self.active = True

    def advance(self):
        if self.active:
            self.index += 1
            if self.index >= len(self.dialogue):
                self.reset()

    def reset(self):
        self.index = -1
        self.dialogue = []
        self.speaker = None
        self.active = False

    def isActive(self):
        return self.active

    def handleClick(self):
        if self.active:
            self.advance()

    def draw(self, screen):
        if not self.active or self.index < 0:
            return

        # Box background
        pygame.draw.rect(screen, (222, 195, 142), self.boxRect)  # follows parchment style
        pygame.draw.rect(screen, (0, 0, 0), self.boxRect, 2)

        # Speaker name
        if self.speaker:
            nameText = self.font.render(f"{self.speaker}:", True, (80, 0, 0))
            screen.blit(nameText, (self.boxRect.x + self.padding, self.boxRect.y + 8))

        # Dialogue text
        line = self.dialogue[self.index]
        text = self.font.render(line, True, (0, 0, 0))
        yOffset = self.boxRect.y + 35 if self.speaker else self.boxRect.y + 20
        screen.blit(text, (self.boxRect.x + self.padding, yOffset))
