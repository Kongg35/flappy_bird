import os
import pygame
from config import WIDTH, HEIGHT, WHITE, BLACK, SKY_BLUE, GREEN, RED, GROUND_BROWN, GROUND_HEIGHT


class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font_big = pygame.font.SysFont("arial", 46, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.sound_enabled = False
        self.jump_sound = None
        self.hit_sound = None
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            base_dir = os.path.dirname(os.path.abspath(__file__))

            jump_path = os.path.join(base_dir, "assets", "jump.ogg")
            hit_path = os.path.join(base_dir, "assets", "hit.ogg")

            self.jump_sound = self._load_sound(jump_path)
            if self.jump_sound:
                self.jump_sound.set_volume(0.2)
            self.hit_sound = self._load_sound(hit_path)
        except pygame.error:
            self.sound_enabled = False
    
    @staticmethod
    def _load_sound(path):
        if os.path.exists(path):
            try:
                return pygame.mixer.Sound(path)
            except pygame.error:
                return None
        return None

    def play_jump_sound(self):
        if self.sound_enabled and self.jump_sound:
            self.jump_sound.play()

    def play_hit_sound(self):
        if self.sound_enabled and self.hit_sound:
            self.hit_sound.play()

    # --- Giao diện trong lúc chơi ---
    def draw_background(self, surface):
        surface.fill(SKY_BLUE)
        ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(surface, GROUND_BROWN, ground_rect)
        pygame.draw.rect(surface, BLACK, ground_rect, 2)

    def draw_score(self, surface, score):
        text = self.font_medium.render(str(score), True, WHITE)
        outline = self.font_medium.render(str(score), True, BLACK)
        x = WIDTH // 2 - text.get_width() // 2
        y = 30
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            surface.blit(outline, (x + dx, y + dy))
        surface.blit(text, (x, y))

    # --- Màn hình bắt đầu ---
    def draw_start_screen(self, surface):
        title = self.font_big.render("FLAPPY BIRD", True, BLACK)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        hint = self.font_small.render("Press SPACE or CLICK to start", True, BLACK)
        surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 3 + 150))

    # --- Màn hình Game Over ---
    def draw_game_over_screen(self, surface, score, best_score):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        title = self.font_big.render("GAME OVER", True, RED)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        score_text = self.font_medium.render(f"Diem: {score}", True, WHITE)
        surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4 + 70))

        best_text = self.font_medium.render(f"Cao nhat: {best_score}", True, WHITE)
        surface.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 4 + 110))

        # Nút chơi lại
        button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 4 + 160, 160, 50)
        pygame.draw.rect(surface, GREEN, button_rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, button_rect, 2, border_radius=10)
        btn_text = self.font_small.render("CHOI LAI", True, BLACK)
        surface.blit(
            btn_text,
            (button_rect.centerx - btn_text.get_width() // 2,
             button_rect.centery - btn_text.get_height() // 2),
        )
        return button_rect
import os

