from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from enum import Enum
import statistics

class Humor(Enum):
    BEMHUMORADO = 0
    NEUTRO = 1
    MALHUMORADO = 2

class Poliglota(Enum):
    PORTUGUES = 0
    INGLES =  1
    VARIOS =  2

class Experiencia(Enum):
    BAIXA =  0
    MEDIA =  1
    ALTA =  2

class Qualis(Enum):
    C =  0
    B5 =  1
    B4 =  2
    B3 =  3
    B2 =  4
    B1 =  5
    A2 =  6
    A1 =  7

# exemplo de como apresentam um dado geral do modelo
def compute_humor(model):
    agent_humor = [agent.humor for agent in model.schedule.agents]
    try:
        mode = statistics.mode(agent_humor)
        mode_numeric = {Humor.BEMHUMORADO: 0, Humor.NEUTRO: 1}.get(mode, 2)
    except:
        mode_numeric = 1
    return mode_numeric

# Modela uma revista científica que precisa ser classificada
class Revista:
    def __init__(self, titulo=None, lingua=None, issn=None):
        self.titulo = titulo
        self.lingua = lingua
        self.issn = issn
        self.lista_avaliacoes = {(0,Qualis["C"]),(1,Qualis["C"]),(2,Qualis["C"]),(3,Qualis["C"])}
        
class HumorAcademicoModel(Model):
    """Um modelo multiagente simples que demonstra como usar um grid para montar um esquema de 
    variação de humor de agentes acadêmicos envolvidos na classificação de um conjunto de revistas 
    da CAPES, no modelo Qualis, desenvolvido durante aula de computação experimental, 
    baseado em modificação do código do exemplo do Boltzmann Wealth Model, por Jorge H C Fernandes
    """

    def __init__(self, N=100, width_height=10):
        self.num_agents = N
        self.width = width_height
        self.height = width_height
        self.revistas = [Revista(),Revista(),Revista(),Revista(),Revista(),Revista()] # busca excel
        self.revista_em_avaliacao = 0 
        self.grid = MultiGrid(width_height, width_height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={"Humor": compute_humor}, 
            agent_reporters={"Poliglota": "poliglota", 
            "Humor": "humor",
            "Experiência": "experiencia"}
        )
        # Create agents
        for i in range(self.num_agents):
            a = AcademicAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n): # para cada um dos agentes do modelo
            self.step()
        self.revista_em_avaliacao = self.revista_em_avaliacao + 1

import random

class AcademicAgent(Agent):
    """ An agent acadêmico que possui um estado de humor, um grau de multilinguísmo e experiência acadêmica."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.humor = random.choice(list(Humor))
        self.poliglota = random.choice(list(Poliglota))
        self.experiencia = random.choice(list(Experiencia))

    def move(self): # mobilidde academica - muda de área
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    # o objetivo é classificar uma revista - implementada apenas a variação de humor
    def classify(self, revista_em_avaliacao):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 10:
            self.humor = Humor.BEMHUMORADO 
        elif len(cellmates) < 5:
            self.humor = Humor.MALHUMORADO 
        else:
            self.humor = Humor.NEUTRO 

    # a cada passo da simulação um acadêmico recebe ums revista para avaliar
    def step(self):
        self.move() # muda de grupo acadêmico
        revista_em_avaliacao = self.model.revistas[self.model.revista_em_avaliacao] # recebe uma revista para avaliar
        if self.humor == Humor.BEMHUMORADO:
            self.classify(revista_em_avaliacao) # classificar se tiver bem humrado
        elif self.humor == Humor.NEUTRO:
            self.classify(revista_em_avaliacao) # clasificar baseado em parâmetros objetivos
            self.humor = Humor.BEMHUMORADO # fica bem humorado. de qualquer modo
        else: # O QUE FAZER ?
            self.humor = Humor.MALHUMORADO

# Código para realização de vários experimentos de simulação
from mesa.batchrunner import BatchRunner

def batch_run():

    fixed_params = {

    }

    variable_params = {"N": range(100, 2500, 500), "width_height": [5, 10, 15, 20, 25]}
    # 100 adademicos em um grid de 5 x 5
    # 100 adademicos em um grid de 10 x 10
    # 100 adademicos em um grid de 15 x 15
    # 100 adademicos em um grid de 20 x 20
    # 100 adademicos em um grid de 25 x 25
    # 600 adademicos em um grid de 5 x 5
    # 600 adademicos em um grid de 10 x 10
    # 600 adademicos em um grid de 15 x 15
    # 600 adademicos em um grid de 20 x 20
    # 600 adademicos em um grid de 25 x 25
    # etc...

    # quantos experimentos (simulações) realizar?
    experiments = 10
    # quantos passos vai durar a simulação?
    max_steps = 10

    # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
    batch_run = BatchRunner(
        HumorAcademicoModel,
        variable_params,
        fixed_params,
        iterations=experiments,
        max_steps=max_steps,
        model_reporters={"Humor": compute_humor}
    )

    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()

    run_model_data.to_csv("HumorAcademicoModel_eh_a_densid_academicos_em_grid_determinante_do_Humor_do_Academico"+
        "_iter_"+str(experiments)+
        "_steps_"+str(max_steps)+
        "_.csv")
