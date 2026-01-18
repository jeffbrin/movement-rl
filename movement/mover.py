from abc import ABC
from .limb import Limb

class Mover(ABC):

    def __init__(self, torso_length: float):
        super().__init__()
        self.torso: Limb = Limb(torso_length)