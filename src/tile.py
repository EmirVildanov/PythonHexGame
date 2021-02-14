class Tile:
    def __init__(self, color, coordinates, neighbours_indices, border_indices):
        self.color = color
        self.coordinates = coordinates
        self.neighbours_indices = neighbours_indices
        self.border_indices = border_indices
