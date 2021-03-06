from hashlib import new
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from datetime import datetime
from .agent import TreeCell
from os import sep


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, humidity=0.6):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        
        self.density = density
        self.humidity = humidity
        
        # acontece a cada passo
        self.datacollector = DataCollector(
            model_reporters={
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # acontece ao termino do ultimo passo
        self.datacollector_agent = DataCollector(
            agent_reporters={
                "Steps to fire up": lambda x: x.count_steps
                #"Count": lambda x: 
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                    new_tree.count_steps = 0
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            
            now = str(datetime.now()).replace(":", "-")
            df = self.datacollector.get_model_vars_dataframe()
            df.to_csv("spreadsheet" + sep + "model_data humi=" + str(self.humidity) + " dens=" + str(self.density) + " " + now + ".csv")

            self.datacollector_agent.collect(self)
            df2 = self.datacollector_agent.get_agent_vars_dataframe()
            df2.to_csv("spreadsheet" + sep + "agent_data humi=" + str(self.humidity) + " dens=" + str(self.density) + " " + now + ".csv")
        
        

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
