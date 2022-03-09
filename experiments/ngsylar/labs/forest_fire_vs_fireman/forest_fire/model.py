from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from datetime import datetime
from os import sep

from .agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, fman_groups=4):
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
        self.fman_groups = fman_groups
        self.fman_density = fman_groups * 0.0025

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine") + self.count_type(m, "Fireman"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Protected": lambda m: self.count_type(m, "Protected"),
            }
        )

        self.finetrees = 0
        self.datacollector_model = DataCollector(
            {
                "Forest Density": lambda m: self.density,
                "Number of fireman groups": lambda m: fman_groups,
                # "Finetrees": lambda m: self.finetrees,
                "Unaffected Vegetation": lambda m: self.count_type(m, "Fine") / (self.count_type(m, "Fine") + self.count_type(m, "Fireman") + self.count_type(m, "Protected") + self.count_type(m, "Burned Out")),
                "Saved Vegetation": lambda m: (self.count_type(m, "Protected") + self.count_type(m, "Fireman")) / (self.count_type(m, "Fine") + self.count_type(m, "Fireman") + self.count_type(m, "Protected") + self.count_type(m, "Burned Out")),
                "Wasted Vegetation": lambda m: self.count_type(m, "Burned Out") / (self.count_type(m, "Fine") + self.count_type(m, "Fireman") + self.count_type(m, "Protected") + self.count_type(m, "Burned Out")),
            }
        )

        self.st98 = []
        self.st94 = []
        self.st86 = []
        self.st70 = []
        self.st40 = []

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < self.fman_density:
                # Create a fireman
                new_fman = TreeCell((x, y), self)
                new_fman.condition = "Fireman"
                new_fman.strength = 0.92
                self.grid._place_agent((x, y), new_fman)
                self.schedule.add(new_fman)
                self.addStrength(x,y)

            elif self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                elif self.st98.count((x,y)):
                    new_tree.strength = 0.88
                elif self.st94.count((x,y)):
                    new_tree.strength = 0.84
                elif self.st86.count((x,y)):
                    new_tree.strength = 0.76
                elif self.st70.count((x,y)):
                    new_tree.strength = 0.6
                elif self.st40.count((x,y)):
                    new_tree.strength = 0.3

                self.grid._place_agent((x,y), new_tree)
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
            # self.count_clusters()

            now = str(datetime.now()).replace(":", "-")
            df_agent = self.datacollector.get_model_vars_dataframe()
            df_agent.to_csv("dataframe" + sep + "agent_data forest_density=" + str(self.density) + " fireman_groups=" + str(self.fman_groups) + " " + now + ".csv")
            
            self.datacollector_model.collect(self)
            df_model = self.datacollector_model.get_model_vars_dataframe()
            df_model.to_csv("dataframe" + sep + "model_data forest_density=" + str(self.density) + " fireman_groups=" + str(self.fman_groups) + " " + now + ".csv")


    def addStrength(self, x, y):
        self.st98.append((x+1,y-1))
        self.st98.append((x+1,y))
        self.st98.append((x+1,y+1))

        self.st98.append((x+2,y-2))
        self.st98.append((x+2,y-1))
        self.st98.append((x+2,y))
        self.st98.append((x+2,y+1))
        self.st98.append((x+2,y+2))

        self.st94.append((x+3,y-3))
        self.st94.append((x+3,y-2))
        self.st94.append((x+3,y-1))
        self.st94.append((x+3,y))
        self.st94.append((x+3,y+1))
        self.st94.append((x+3,y+2))
        self.st94.append((x+3,y+3))

        self.st94.append((x+4,y-4))
        self.st94.append((x+4,y-3))
        self.st94.append((x+4,y-2))
        self.st94.append((x+4,y-1))
        self.st94.append((x+4,y))
        self.st94.append((x+4,y+1))
        self.st94.append((x+4,y+2))
        self.st94.append((x+4,y+3))
        self.st94.append((x+4,y+4))
        
        self.st86.append((x+5,y-5))
        self.st86.append((x+5,y-4))
        self.st86.append((x+5,y-3))
        self.st86.append((x+5,y-2))
        self.st86.append((x+5,y-1))
        self.st86.append((x+5,y))
        self.st86.append((x+5,y+1))
        self.st86.append((x+5,y+2))
        self.st86.append((x+5,y+3))
        self.st86.append((x+5,y+5))

        self.st86.append((x+6,y-6))
        self.st86.append((x+6,y-5))
        self.st86.append((x+6,y-4))
        self.st86.append((x+6,y-3))
        self.st86.append((x+6,y-2))
        self.st86.append((x+6,y-1))
        self.st86.append((x+6,y))
        self.st86.append((x+6,y+1))
        self.st86.append((x+6,y+2))
        self.st86.append((x+6,y+3))
        self.st86.append((x+6,y+5))
        self.st86.append((x+6,y+6))

        self.st70.append((x+7,y-7))
        self.st70.append((x+7,y-6))
        self.st70.append((x+7,y-5))
        self.st70.append((x+7,y-4))
        self.st70.append((x+7,y-3))
        self.st70.append((x+7,y-2))
        self.st70.append((x+7,y-1))
        self.st70.append((x+7,y))
        self.st70.append((x+7,y+1))
        self.st70.append((x+7,y+2))
        self.st70.append((x+7,y+3))
        self.st70.append((x+7,y+5))
        self.st70.append((x+7,y+6))
        self.st70.append((x+7,y+7))

        self.st40.append((x+8,y-6))
        self.st40.append((x+8,y-5))
        self.st40.append((x+8,y-4))
        self.st40.append((x+8,y-3))
        self.st40.append((x+8,y-2))
        self.st40.append((x+8,y-1))
        self.st40.append((x+8,y))
        self.st40.append((x+8,y+1))
        self.st40.append((x+8,y+2))
        self.st40.append((x+8,y+3))
        self.st40.append((x+8,y+5))
        self.st40.append((x+8,y+6))

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