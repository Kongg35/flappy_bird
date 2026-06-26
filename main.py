import sys
import pygame
import asyncio

from config import WIDTH, HEIGHT, FPS
from bird import Bird
from pipe_manager import PipeManager
from collision import CollisionManager
from ui import UIManager


class Game:
    STATE_START = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird - Python")
        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = UIManager()
        self.best_score = 0
        self.replay_button_rect = None

        self.state = self.STATE_START
        self._new_round()

    def _new_round(self):
        self.bird = Bird(WIDTH // 2, HEIGHT // 2)

        # collision + pipe manager
        self.collision_manager = CollisionManager()
        self.pipe_manager = PipeManager(self.collision_manager)

    # ---------------- EVENTS ----------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._on_action()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_action(pygame.mouse.get_pos())

    def _on_action(self, mouse_pos=None):
        if self.state == self.STATE_START:
            self.state = self.STATE_PLAYING
            self.bird.jump()
            self.ui.play_jump_sound()

        elif self.state == self.STATE_PLAYING:
            self.bird.jump()
            self.ui.play_jump_sound()

        elif self.state == self.STATE_GAME_OVER:
            if mouse_pos is None or (
                self.replay_button_rect and
                self.replay_button_rect.collidepoint(mouse_pos)
            ):
                self._new_round()
                self.state = self.STATE_START

    # ---------------- UPDATE ----------------
    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        self.bird.update()
        self.pipe_manager.update()

        collided = self.collision_manager.check_collisions(
            self.bird, self.pipe_manager
        )

        self.collision_manager.update_score(self.bird, self.pipe_manager)

        if collided or not self.bird.alive:
            self.state = self.STATE_GAME_OVER
            self.ui.play_hit_sound()
            self.best_score = max(
                self.best_score,
                self.collision_manager.score
            )

    # ---------------- DRAW ----------------
    def draw(self):
        self.ui.draw_background(self.screen)
        self.pipe_manager.draw(self.screen)
        self.bird.draw(self.screen)

        if self.state == self.STATE_START:
            self.ui.draw_start_screen(self.screen)

        elif self.state == self.STATE_PLAYING:
            self.ui.draw_score(self.screen, self.collision_manager.score)

        elif self.state == self.STATE_GAME_OVER:
            self.ui.draw_score(self.screen, self.collision_manager.score)

            self.replay_button_rect = self.ui.draw_game_over_screen(
                self.screen,
                self.collision_manager.score,
                self.best_score
            )

        pygame.display.flip()

    # ---------------- MAIN LOOP (PYGBAG READY) ----------------
    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)
            await asyncio.sleep(0)   # QUAN TRỌNG cho pygbag

        pygame.quit()
        return


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())