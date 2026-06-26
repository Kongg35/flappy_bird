import pygame
from config import GRAVITY, JUMP_STRENGTH, HEIGHT, GROUND_HEIGHT, BIRD_SIZE


class BirdPhysicsMixin:
    """
    Mixin chịu trách nhiệm vật lý & điều khiển con chim.
    Được "trộn" (mix) vào class Bird cùng với BirdAppearanceMixin của Người 2.
    """

    def _init_physics(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.alive = True

    def jump(self):
        """Khi người chơi nhấn SPACE / click -> chim bật lên."""
        if self.alive:
            self.velocity = JUMP_STRENGTH

    def update(self):
        """Áp dụng trọng lực, cập nhật vị trí, giới hạn không cho ra ngoài màn hình."""
        self.velocity += GRAVITY
        self.y += self.velocity

        # Giới hạn trên (không cho chim bay vượt mép trên màn hình)
        if self.y - BIRD_SIZE // 2 < 0:
            self.y = BIRD_SIZE // 2
            self.velocity = 0

        # Giới hạn dưới (mặt đất) -> coi như chạm đất, chim "chết"
        ground_y = HEIGHT - GROUND_HEIGHT
        if self.y + BIRD_SIZE // 2 >= ground_y:
            self.y = ground_y - BIRD_SIZE // 2
            self.velocity = 0
            self.alive = False

    def get_rect(self):
        """Trả về hitbox (pygame.Rect) của chim, dùng để kiểm tra va chạm."""
        half = BIRD_SIZE // 2
        return pygame.Rect(int(self.x - half), int(self.y - half), BIRD_SIZE, BIRD_SIZE)
