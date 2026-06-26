from os import pipe
import random
import pygame

from pipe import Pipe
from config import GROUND_HEIGHT, HEIGHT, PIPE_GAP, PIPE_WIDTH, WIDTH, PIPE_SPEED

class PipeManager:
    def __init__(self, collision_manager):
        self.pipes = []
        self.last_spawn_time = pygame.time.get_ticks()
        self._spawn_first_pipe()

        # Dùng chung đối tượng điểm số với Game
        self.collision_manager = collision_manager

    def _spawn_first_pipe(self):
        self.pipes.append(Pipe(WIDTH + 100))

    def update(self):
        now = pygame.time.get_ticks()

        # 1. Di chuyển toàn bộ ống sang trái
        for pipe in self.pipes:
            if self.collision_manager.score >= 10:
                pipe.x -= PIPE_SPEED
            else:
                pipe.x -= (PIPE_SPEED -1 )

        # 2. Xóa ống đã đi hết ra khỏi màn hình (tối ưu, tránh list phình to)
        self.pipes = [p for p in self.pipes if p.x + p.width > -50]

        # 3. Sinh ống mới theo vị trí ống cuối
        if self.pipes[-1].x < WIDTH - 120:
            pipe1 = Pipe(WIDTH + 120)
            self.pipes.append(pipe1)
            count = 1
            if self.collision_manager.score >= 20:
                count = 2
            if self.collision_manager.score >= 60:
                count = 3
            if self.collision_manager.score == 120:
                count = 50
            if self.collision_manager.score > 120:
                count = random.choice([1, 2, 3, 5,])
            prev_pipe = pipe1

            for i in range(1, count):
                pipe = Pipe(
                    WIDTH + 120 + i * (PIPE_WIDTH + 25),
                    copy_pipe=prev_pipe
                )

                offset = random.randint(-35, 35)

                new_top = pipe.top_height + offset

                min_top = 50
                max_top = HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50

                new_top = max(min_top, min(new_top, max_top))

                pipe.top_height = new_top
                pipe.bottom_y = new_top + PIPE_GAP

                self.pipes.append(pipe)
                prev_pipe = pipe
  
    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)

    def reset(self):
        self.pipes.clear()
        self.last_spawn_time = pygame.time.get_ticks()
        self._spawn_first_pipe()
