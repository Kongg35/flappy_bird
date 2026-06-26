from config import HEIGHT, GROUND_HEIGHT


class CollisionManager:
    def __init__(self):
        self.score = 0

    def check_collisions(self, bird, pipe_manager):
        """Trả về True nếu chim va chạm (ống hoặc mặt đất) -> Game Over."""
        bird_rect = bird.get_rect()

        # Va chạm với mặt đất
        if bird_rect.bottom >= HEIGHT - GROUND_HEIGHT:
            return True

        # Chạm trần thì chặn lại, không tính là chết
        if bird_rect.top <= 0:
            bird.velocity = 0

        # Va chạm với ống (trên hoặc dưới)
        for pipe in pipe_manager.pipes:
            if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                return True

        return False

    def update_score(self, bird, pipe_manager):
        """Cộng điểm khi chim vượt qua hoàn toàn một cặp ống."""
        for pipe in pipe_manager.pipes:
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                self.score += 1

    def reset(self):
        self.score = 0
