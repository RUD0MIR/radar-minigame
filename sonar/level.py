from pytmx import load_pygame

from util.util import normalize_matrix


class Level:
    """
        Current level options
    """
    def __init__(
            self,
            player_spawn_pos,
            map_path,
    ):
        self.player_spawn_pos = player_spawn_pos
        self.matrix = normalize_matrix(load_pygame(map_path).layers[0].data)
        self.walls_layer = load_pygame(map_path).layers
