"""
Sugarscape Constant Growback Model
================================

Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import SsAgent, Sugar
from .schedule import RandomActivationByBreed


class SugarscapeCg(Model):
    """
    Sugarscape 2 Constant Growback
    """

    verbose = True  # Print-monitoring

    def __init__(
        self, height=50, width=50, initial_population=100,
        reproduce_prob=0.5, growback_factor=1,
    ):
        """
        Create a new Constant Growback model with the given parameters.

        Args:
            initial_population: Number of population to start with
            reproduce_prob: Probability that a given ant reproduces in some
                            step of the simulation
            growback_factor: Amount that every sugarcane grows by each step

        """

        # Set parameters
        self.height = height
        self.width = width
        self.initial_population = initial_population
        self.reproduce_prob = reproduce_prob
        self.growback_factor = growback_factor

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            model_reporters = {
                "SsAgent": lambda m: m.schedule.get_breed_count(SsAgent),
            },
        )


        self.children = []
        self.removals = []

        # Create sugar
        import numpy as np

        sugar_distribution = np.genfromtxt("src/sugar-map.txt")
        self.sugar_agent_at = np.ndarray((self.height, self.width), dtype=Sugar)
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.sugar_agent_at[x, y] = sugar
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            ssa = SsAgent((x, y), self, False, sugar, metabolism, vision, reproduce_prob)
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True
        self.datacollector.collect(self)

    def schedule_add_child(self, child):
        self.children.append(child)

    def schedule_removal(self, agent):
        self.removals.append(agent)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_breed_count(SsAgent)])

        for child in self.children:
            self.grid.place_agent(child, child.pos)
            self.schedule.add(child)

        for agent in self.removals:
            self.grid._remove_agent(agent.pos, agent)
            self.schedule.remove(agent)

        self.children = []
        self.removals = []

        if len(self.schedule.agents_by_breed[SsAgent]) == 0:
            self.running = False

    def run_model(self, step_count=200):

        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_breed_count(SsAgent),
            )

        for i in range(step_count):
            self.step()
            if not self.running:
                break

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_breed_count(SsAgent),
            )


def batch_run(
        rp=[0.0, 0.05, 0.10, 0.15, 0.5],
        gf=[0.0, 0.05, 0.10, 0.15, 0.5, 1.5, 2.5],
):
    from mesa.batchrunner import batch_run
    from datetime import datetime
    import numpy as np
    import pandas as pd
    import sys
    import os

    params = {
        "reproduce_prob": rp,
        "growback_factor": gf,
    }

    iterations = 2
    steps = 100

    results = batch_run(
        SugarscapeCg,
        params,
        iterations=iterations,
        max_steps=steps,
        number_processes=None,
        data_collection_period=1,
    )

    dataframe = pd.DataFrame(results)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Create csv filename
    fn = "data"
    if type(rp) != list:
        fn += "_rp{}".format(rp)
    if type(gf) != list:
        fn += "_gf{}".format(gf)
    fn += "_t{}.csv".format(timestamp)

    os.makedirs("csv", exist_ok=True)
    dataframe.to_csv(os.path.join("csv", fn))
