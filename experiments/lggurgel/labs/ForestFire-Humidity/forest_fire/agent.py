from mesa import Agent


class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model, has_humidity):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
            has_humidity: value of atmospheric moisture that surrounds the tree
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.has_humidity = has_humidity

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine" and not neighbor.has_humidity:
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"
