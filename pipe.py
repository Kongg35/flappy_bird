import random
import pygame
from config import PIPE_GAP, PIPE_WIDTH, HEIGHT, GROUND_HEIGHT, GREEN, BLACK


class Pipe:
    def __init__(self, x, copy_pipe=None):
        self.x = x
        self.width = PIPE_WIDTH
        self.passed = False

        if copy_pipe:
            self.top_height = copy_pipe.top_height
            self.bottom_y = copy_pipe.bottom_y
        else:
            self._generate_height()

    def _generate_height(self):
        """Sinh ngẫu nhiên chiều cao ống trên, từ đó suy ra vị trí ống dưới
        sao cho luôn có khoảng trống (PIPE_GAP) cố định giữa 2 ống."""
        min_height = 50
        max_height = HEIGHT - GROUND_HEIGHT - PIPE_GAP - min_height
        max_height = max(min_height, max_height)
        self.top_height = random.randint(min_height, max_height)
        self.bottom_y = self.top_height + PIPE_GAP

    def get_top_rect(self):
        return pygame.Rect(int(self.x), 0, self.width, self.top_height)

    def get_bottom_rect(self):
        ground_y = HEIGHT - GROUND_HEIGHT
        return pygame.Rect(int(self.x), self.bottom_y, self.width, ground_y - self.bottom_y)

    def draw(self, surface):
        top_rect = self.get_top_rect()
        bottom_rect = self.get_bottom_rect()

        pygame.draw.rect(surface, GREEN, top_rect)
        pygame.draw.rect(surface, BLACK, top_rect, 2)
        pygame.draw.rect(surface, GREEN, bottom_rect)
        pygame.draw.rect(surface, BLACK, bottom_rect, 2)

        # Viền (cap) ở miệng ống cho đẹp mắt
        cap_h = 20
        cap_top = pygame.Rect(self.x - 3, self.top_height - cap_h, self.width + 6, cap_h)
        cap_bottom = pygame.Rect(self.x - 3, self.bottom_y, self.width + 6, cap_h)
        pygame.draw.rect(surface, GREEN, cap_top)
        pygame.draw.rect(surface, BLACK, cap_top, 2)
        pygame.draw.rect(surface, GREEN, cap_bottom)
        pygame.draw.rect(surface, BLACK, cap_bottom, 2)
