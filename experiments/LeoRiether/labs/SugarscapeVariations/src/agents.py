import math

from mesa import Agent


def get_distance(pos_1, pos_2):
    """Get the distance between two point

    Args:
        pos_1, pos_2: Coordinate tuples for both points.

    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.hypot(dx, dy)

class SsAgent(Agent):
    uid = 0

    def __init__(self, pos, model, moore=False, sugar=0, metabolism=0, vision=0, repr_prob=0):
        SsAgent.uid += 1
        super().__init__(SsAgent.uid, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.repr_prob = repr_prob

    def get_sugar(self, pos):
        return self.model.sugar_agent_at[pos[0], pos[1]]

    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return len(this_cell) > 1

    def move(self):
        # Get neighborhood within vision
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vision
            )
            if not self.is_occupied(i)
        ]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max(self.get_sugar(pos).amount for pos in neighbors)
        candidates = [
            pos for pos in neighbors if self.get_sugar(pos).amount == max_sugar
        ]
        # Narrow down to the nearest ones
        min_dist = min(get_distance(self.pos, pos) for pos in candidates)
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0

    def reproduce(self):
        if self.sugar >= 1.5 and self.random.random() <= self.repr_prob:
            child = SsAgent(
                self.pos, self.model, False,
                self.sugar / 2, self.metabolism,
                self.vision, self.repr_prob,
            )
            self.sugar -= child.sugar # parent and child each get a portion of the sugar
            self.model.schedule_add_child(child)

    def step(self):
        # print(self.sugar, self.metabolism, self.get_sugar(self.pos).amount)
        self.move()
        self.eat()
        self.reproduce()
        if self.sugar < 1:
            self.model.schedule_removal(self)

class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.growback_factor = model.growback_factor

    def step(self):
        self.amount = min(self.max_sugar, self.amount + self.growback_factor)
