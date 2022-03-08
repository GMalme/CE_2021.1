from pickle import FALSE, TRUE
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

import csv

from .agent import TreeCell

def shield_trees_index(model): # arrumar para nao contar a mesma arvore mais de uma vez
    """
    Se uma arvore esta "Fine", mas sua vizinha "Burned Out", entao temos
    que a arvore sobreviveu ao fogodireto devido a resitencia da casca.
    Qual a porcentagem de arvores que impediram o avanco do fogo
    """

    count = 0
    for agent in model.schedule.agents:
        if agent.condition == "Fine":
            flag = TRUE
            for neighbor in agent.model.grid.neighbor_iter(agent.pos):
                if neighbor.condition == "Burned Out" and flag == TRUE:
                    count += 1
                    flag = FALSE    # evita contar a mesma arvore mais de uma vez


    dataframe_last_row = model.datacollector.get_model_vars_dataframe().tail(1)
    n_fine_tree = dataframe_last_row.iloc[:, 0].tolist()

    index = count/n_fine_tree[0] # index: das arvores "Fine" quais sobreviverao a fogo direto?

    return index


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, skin=5.0):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self, skin) # arvore tem parametro "skin"
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
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
            # dataframe para csv variaveis de agente
            self.datacollector.get_model_vars_dataframe().to_csv('agent_var.csv')
            # variavel de modelo
            res_index = shield_trees_index(self)

            fields = ['Shield Index']
            row = [res_index]

            # criando csv 
            with open('model_var.csv', 'w') as csvfile: 
                # writer object
                csvwriter = csv.writer(csvfile) 
                    
                # campos 
                csvwriter.writerow(fields) 
                    
                # linhas 
                csvwriter.writerow(row)

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
