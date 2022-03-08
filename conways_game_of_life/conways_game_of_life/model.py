from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from .cell import Cell

def it_len(it):
    return sum(1 for _ in it)

def neighborhood_mean(model):
    return  sum([sum(1 for y in x.neighbors if y.isAlive) for x in model.schedule.agents if x.isAlive])/len([x for x in model.schedule.agents if x.isAlive])

class ConwaysGameOfLife(Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """

    def __init__(self, width=50, height=50, density=0.1, revival=0.1):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)
        # Use a simple grid, where edges wrap around.
        self.grid = Grid(width, height, torus=True)
        self.datacollector = DataCollector(
            model_reporters={
                "Density": neighborhood_mean,
            },
            agent_reporters={
                "Alive": lambda x: sum(1 for y in x.neighbors if y.isAlive) if x.isAlive else -1,
            },
        )

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self, revival=revival)
            if self.random.random() < density:
                cell.state = cell.ALIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.running = True
        self.datacollector.collect(self)
        

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        self.datacollector.collect(self)
        if self.schedule.steps % 15 == 0:
            l_agent = self.datacollector.get_agent_vars_dataframe()
            l_model = self.datacollector.get_model_vars_dataframe()
            l_agent.to_csv('agent.csv')
            l_model.to_csv('model.csv')