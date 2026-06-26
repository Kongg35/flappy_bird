import pygame
from config import YELLOW, BLACK, ORANGE, BIRD_SIZE


class BirdAppearanceMixin:
    """
    Mixin chịu trách nhiệm hiển thị con chim.
    Được "trộn" (mix) vào class Bird cùng với BirdPhysicsMixin của Người 3.
    """

    def _init_appearance(self):
        # Biến phục vụ hoạt ảnh vẫy cánh
        self.wing_timer = 0
        self.wing_state = 0  # 0: cánh giữa, 1: cánh lên, 2: cánh xuống

    def animate_wing(self):
        """Đổi trạng thái cánh sau mỗi vài khung hình để tạo hiệu ứng vẫy."""
        self.wing_timer += 1
        if self.wing_timer >= 5:
            self.wing_timer = 0
            self.wing_state = (self.wing_state + 1) % 3

    def draw(self, surface):
        """Vẽ con chim lên surface tại vị trí (self.x, self.y)."""
        self.animate_wing()

        x, y = int(self.x), int(self.y)
        r = BIRD_SIZE // 2

        # Thân chim
        pygame.draw.circle(surface, YELLOW, (x, y), r)
        pygame.draw.circle(surface, BLACK, (x, y), r, 2)

        # Mắt
        pygame.draw.circle(surface, BLACK, (x + 8, y - 6), 3)

        # Mỏ
        beak = [(x + r +10,y), (x + r -2, y - 3), (x + r - 2, y + 3)]
        pygame.draw.polygon(surface, ORANGE, beak)

        # Cánh (hoạt ảnh vẫy theo wing_state)
        wing_offset = [-6, -2, 4][self.wing_state]
        wing_rect = pygame.Rect(x - 12, y - 4 + wing_offset, 16, 10)
        pygame.draw.ellipse(surface, (230, 180, 0), wing_rect)
        pygame.draw.ellipse(surface, BLACK, wing_rect, 1)
