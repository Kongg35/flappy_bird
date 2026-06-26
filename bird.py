from bird_appearance import BirdAppearanceMixin
from bird_physics import BirdPhysicsMixin


class Bird(BirdAppearanceMixin, BirdPhysicsMixin):
    def __init__(self, x, y):
        self._init_physics(x, y)      # phần của Người 3
        self._init_appearance()       # phần của Người 2
