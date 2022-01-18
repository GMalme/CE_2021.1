
import math
from enum import Enum
import networkx as nx
from random import randint, random, choices

from mesa import Agent, Model, agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import DirectedNetworkGrid
from networkx.algorithms.communicability_alg import communicability
from numpy.core.arrayprint import get_printoptions
from BrazilianPopulationalPyramid import BrazilianPopulationalPyramid
from mesa.batchrunner import BatchRunner
from datetime import datetime
from numpy import arange

class CommercialExchangeState(Enum):
    AVAILABLE = 0
    TRADING = 1
    RESISTANT = 2

class SoilState(Enum): # Sistema Brasileiro de Classificação de Solos EMBRAPA 2018
    Argissolo = 0
    Cambissolo = 1
    Chernossolo = 2
    Espodossolo = 3
    Gleissolo = 4
    Latossolo = 5
    Luvissolo = 6
    Neossolo = 7
    Nitossolo = 8
    Organossolo = 9
    Planossolo = 10
    Plintossolo = 11
    Vertissolo = 12

# https://en.wikipedia.org/wiki/K%C3%B6ppen_climate_classification
class climateState(Enum):
#2 Group A: Tropical/megathermal_climates
    Af_Tropical_rainforest_climate = 0
    Am_Tropical_monsoon_climate = 1
    Aw_Tropical_savanna_climate_with_dry_winter_characteristics = 2
    As_Tropical_savanna_climate_with_dry_summer_characteristics = 3
#3 Group B: Dry (desert and semi-arid)_climates
    BW_Arid_climate = 4
    BW_Arid_climate_Hot_desert = 5
    BW_Arid_climate_Cold_desert = 6
    BS_Semi_arid_steppe_climate = 7
    BS_Semi_arid_steppe_climate_Hot_semi_arid = 8
    BS_Semi_arid_steppe_climate_Cold_semi_arid = 9
#4 Group C: Temperate/mesothermal_climates
    Csa_Mediterranean_hot_summer_climates = 10
    Csb_Mediterranean_warm_cool_summer_climates = 11
    Csc_Mediterranean_cold_summer_climates = 12
    Cfa_Humid_subtropical_climates = 13
    Cfb_Oceanic_climate_Marine_west_coast_climate = 14
    Cfb_Oceanic_climate_Subtropical_highland_climate_with_uniform_rainfall = 15
    Cfc_Subpolar_oceanic_climate = 16
    Cwa_Dry_winter_humid_subtropical_climate = 17
    Cwb_Dry_winter_subtropical_highland_climate = 18
    Cwc_Dry_winter_cold_subtropical_highland_climate = 19
#5 Group D: Continental/microthermal_climates
    Dfa_Dwa_Dsa_Hot_summer_continental_climates = 20
    Dfb_Dwb_Dsb_Warm_summer_continental_or_hemiboreal_climates = 21
    Dfc_Dwc_Dsc_Subarctic_or_boreal_climates = 22
    Dfd_Dwd_Dsd_Subarctic_or_boreal_climates_with_severe_winters = 23
#6 Group E: Polar_climates
    ET_Tundra_climate = 24
    EF_Ice_cap_climate = 25

def number_commercial_state(model, state):
    return sum([1 for a in model.grid.get_all_cell_contents() if a.state is state])

def alpha(model):
    return model.alpha

def beta(model):
    return model.beta

def gamma(model):
    return model.gamma

def number_trading(model):
    return number_commercial_state(model, CommercialExchangeState.TRADING)

def number_available(model):
    return number_commercial_state(model, CommercialExchangeState.AVAILABLE)

def number_resistant(model):
    return number_commercial_state(model, CommercialExchangeState.RESISTANT)

def model_population(model):
    return int(sum(model.get_population()))

def model_initial_population(model):
    return model.initial_population

def network_eccentricity(model):
    return nx.eccentricity(model.G)

def network_diameter(model):
    return nx.diameter(model.G)
    
def network_number_strongly_connected_components(model):
    return nx.number_strongly_connected_components(model.G)

def network_number_strongly_connected_components_not_unitary(model):
    components = nx.strongly_connected_components(model.G)
    component_sizes_bigger_than_one = [len(x) for x in components if len(x) > 1]
    return len(component_sizes_bigger_than_one)

def network_number_weakly_connected_components(model):
    return nx.number_weakly_connected_components(model.G)

def network_transitivity(model):
    return nx.transitivity(model.G)

def network_channels_deceased_rate(model):
    if model.simulation_step == 0:
        return 0
    return model.channels_deceased_counter / model.simulation_step 

from scipy.stats import expon
import copy

class NetworkOfTerritories(Model):
    """A model to simulate territories apt for scientific knowledge production"""

    def __init__(
        self,
        num_nodes=10,
        fraction_of_brazilian_population=1,
        alpha=0.41,
        beta=0.54,
        gamma=0.05,
        delta_in=0.02,
        delta_out=0.0,
        initial_trading_perc=1,
        trading_spread_chance=0.4,
        trading_control_frequency=0.4,
        trading_recovery_chance=0.3,
        trading_resistance_chance=0.5,
        non_trading_decay=0.1,
        trading_revigoration = 0.2,
        visualizing=True,
        seed=None
    ):
        
        self.num_nodes = num_nodes
        self.visualizing = visualizing
        self.trading_revigoration = trading_revigoration
        self.non_trading_decay = non_trading_decay
        self.running = True
        #prob = avg_node_degree / self.num_nodes

        # Cria um grafo inicial, do tipo livre de escala 
        self.seed = seed # colocar um número fixo, para estabilizar a visualização da rede inicial
        # ajusta parâmetros de alfa, beta e gamma
        if (alpha+gamma+beta) != 1:
            if (alpha >= 0.9):
                alpha = 0.8
                beta = 0.1
                gamma = 0.1
            elif (alpha+gamma >= 1):
                gamma = 1 - alpha - 0.1
                beta = 0.1
            else:
                beta = 1 - (alpha+gamma)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta_in = delta_in
        self.delta_out = delta_out
        grafo = nx.scale_free_graph(n=self.num_nodes,alpha=self.alpha, beta=self.beta, gamma=self.gamma, 
                                delta_in=self.delta_in, delta_out=self.delta_out, create_using=None, seed=self.seed)
        # converte de multigrafo para grafo dirigido, com pesos variáveis
        grafo_digirido = nx.DiGraph()
        for u, v, key in grafo.edges:
            if (u == v):
                continue # descarta os ciclos
            elif grafo_digirido.has_edge(u,v):
                edge_weight = grafo_digirido.get_edge_data(u,v)['weight']
                edge_weight = edge_weight + 1
                grafo_digirido.edges[u,v]["weight"] = edge_weight
            else:
                grafo_digirido.add_edge(u,v,weight=1)
        # O grafo é a representação matemática do modelo da simulação 
        self.G = grafo_digirido

        # inicializa a taxa de uso dos canais e o sistema de cores para representá-lo
        for u, v in self.G.edges:
            self.G.edges[u,v]["usage"] = 100 # 100% de uso, na inicialização.
        self.channels_deceased_counter = 0
        self.simulation_step = 0
                
        self.grid = DirectedNetworkGrid(self.G)
        self.schedule = RandomActivation(self)

        # Inicialmente apenas uma fração dos territórios estará comercializando
        self.initial_traders_size=math.floor(num_nodes*initial_trading_perc)

        # Essa é chance de que a ideia das trocas comerciais seja adotada por um território
        self.trading_spread_chance = trading_spread_chance

        # Esse parâmetro representa quantas vezes será investigado se o território está comercializando
        self.trading_control_frequency = trading_control_frequency

        # Essa é a chance do território deixar de fazer trocas comerciais, mesmo que momentânea
        self.trading_recovery_chance = trading_recovery_chance

        # Essa é a chance do território deixar de fazer trocas comerciais permanentemente
        self.trading_resistance_chance = trading_resistance_chance

        self.initial_population = 0

        # Cria-se um coletor de dados básico, sobre o estado geral dos territórios
        self.datacollector = DataCollector(
            model_reporters = {
                "Trading": number_trading,
                "Available": number_available,
                "Resistant": number_resistant,
                "TotalPopulation": model_population,
                "StrongComponentsGT1": network_number_strongly_connected_components_not_unitary,
                "Weakcomponents": network_number_weakly_connected_components,
                "Transitivity": network_transitivity
            },
            agent_reporters = {
                "Population": territory_population,
                "EconomicComplexity": territory_economic_complexity,
                "State": territory_state,
                "QtyImporters": territory_out_degree,
                "QtyExporters": territory_in_degree
            }
        )

        # gera uma lista de percentuais de população, obtidas de uma curva exponencial, 
        # para modelar as populações das cidades brasileiras
        distr_populacoes = expon.rvs(scale=1/self.num_nodes,loc=0,size=self.num_nodes)
        # ordena a lista da maior para a menor população
        distr_populacoes_decresc = sorted(distr_populacoes, reverse=True)

        # busca cada um dos vértices do grafo, ordenados do maior para a menor grau total  
        nos_classificados = sorted(self.G.degree(weight="weight"), key=lambda x: x[1], reverse=True)

        network_base_population = BrazilianPopulationalPyramid().change_pyramid(fraction_of_brazilian_population-1)
        # Create agents
        i = 0
        for node, weighted_degree in nos_classificados:
            perc_popul = distr_populacoes_decresc[i] # population of the territory in relation to brazil's population
            a = TerritoryAgent(
                unique_id=node,
                model=self,
                initial_state=CommercialExchangeState.AVAILABLE,
                trading_spread_chance=self.trading_spread_chance,
                trading_control_frequency=self.trading_control_frequency,
                trading_recovery_chance=self.trading_recovery_chance,
                trading_resistance_chance=self.trading_resistance_chance,
                populational_pyramid=copy.deepcopy(network_base_population).change_pyramid(perc_popul-1),
                visualizing = self.visualizing
            )
            self.schedule.add(a)
            # Add the territory to the graph's node
            self.grid.place_agent(a, node)
            i = i + 1

        # Infect some nodes
        new_trader_nodes = self.random.sample(self.G.nodes(), self.initial_traders_size)
        for a in self.grid.get_cell_list_contents(new_trader_nodes):
            a.state = CommercialExchangeState.TRADING

        self.update_population()
        self.initial_population = sum(self.get_population())

        if (self.visualizing):
            for a in self.G.nodes():
                self.G.nodes[a]["agent"][0].update_node_size() #node size is based on the population of the territory

        self.datacollector.collect(self)

    def resistant_available_ratio(self):
        try:
            return number_commercial_state(self, CommercialExchangeState.RESISTANT) / number_commercial_state(
                self, CommercialExchangeState.AVAILABLE
            )
        except ZeroDivisionError:
            return math.inf

    def update_population(self):
        self.population = [a.get_population() for a in self.grid.get_all_cell_contents()]

    def get_population(self):
        return self.population

    # when a channel dries up it is necessary to choose a new channel do another territory
    def choose_new_target(self, source, excluded):
        sorted_nodes = sorted(self.G.degree(weight="weight"), key=lambda x: x[1], reverse=True)
        weight = [weight for v, weight in sorted_nodes]
        vertexes = [v for v, weight in sorted_nodes]
        for v in choices(vertexes, weights=weight, k = len(weight)):
            if (v != source and v != excluded and not self.G.has_edge(source,v)):
                return v
        return excluded # se não encontrou nenhum outro para substituir fica com o original        

    def decrease_channel_usage_rate(self):
        for u, v in self.G.edges:
            usage_rate = self.G.edges[u,v]["usage"]
            self.G.edges[u,v]["usage"] = self.G.edges[u,v]["usage"] - self.non_trading_decay
            if (self.G.edges[u,v]["usage"] < 0): # channel is dead. Remove and create new channel with the same previous weight
                weight = self.G.edges[u,v]["weight"]
                self.G.remove_edge(u,v)
                self.channels_deceased_counter = self.channels_deceased_counter + 1
                new_target = self.choose_new_target(u, v)
                self.G.add_edge(u, new_target, weight=weight, usage=100)

    def get_channel_usage_rate(self, u, v):
        usage_rate = self.G.edges[u,v]["usage"]
        return usage_rate

    def increase_channel_usage_rate(self, u, v):
        usage_rate = self.G.edges[u,v]["usage"]
        self.G.edges[u,v]["usage"] = self.G.edges[u,v]["usage"] + self.trading_revigoration
        if (self.G.edges[u,v]["usage"] > 100):
            self.G.edges[u,v]["usage"] = 100

    def step(self):
        # simulate one year of elapsed time 
        self.simulation_step = self.simulation_step + 1
        self.decrease_channel_usage_rate() # all  channels have their usage rate decreased by default
        self.schedule.step() # make interactions among the agents
        self.update_population() #  update global state at the level of the model
        self.datacollector.collect(self) # collect data  

    # realiza um experimento de simulação, por n passos (anos), a duração default desse experimento é de um século
    def run_model(self, n=100):
        for i in range(n):
            self.step()

    
def territory_population(territory):
    return "{:,}".format(int(territory.get_population()))

def territory_economic_complexity(territory):
    return territory.economic_complexity

def territory_state(territory):
    return {CommercialExchangeState.TRADING: "Trading", CommercialExchangeState.AVAILABLE: "Available"}.get(
            territory.state, "Resistant")

def territory_out_degree(territory):
    return territory.model.G.out_degree(territory.pos)

def territory_in_degree(territory):
    return territory.model.G.in_degree(territory.pos)

class TerritoryAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        initial_state,
        trading_spread_chance,
        trading_control_frequency,
        trading_recovery_chance,
        trading_resistance_chance,
        populational_pyramid,
        visualizing=True
    ):
        super().__init__(unique_id, model)

        self.state = initial_state
        self.visualizing = visualizing # if visualizing simulation, then the node size is updated each step
        self.size = 1 

        self.trading_spread_chance = trading_spread_chance
        self.trading_control_frequency = trading_control_frequency
        self.trading_recovery_chance = trading_recovery_chance
        self.trading_resistance_chance = trading_resistance_chance
        self.populational_pyramid = populational_pyramid
        self.population = self.get_population() 

        self.soil = randint(0,13)
        self.climate = randint(0,25)
        self.economic_complexity = random()

    def internalPopulationalGrowth(self):
        self.populational_pyramid.step()

    def get_population(self):
        self.population = self.populational_pyramid.pop_total()
        return self.population

    def trade_export_to(self, importer):
        # Trade and fertility in the developing world: the impact of trade and trade structure
        # https://www.jstor.org/stable/44289700
        channel_usage_rate = self.model.get_channel_usage_rate(self.pos, importer.pos)
        fertility_economic_change = randint(0,channel_usage_rate)/10000 # between 0 and 100% change in current fertility tax
        if (self.economic_complexity > 0.75): # complex economy exporting services or goods
            self.populational_pyramid.change_total_fecundity_rate(-fertility_economic_change)
            if (importer.economic_complexity < 0.25): # to a lower complexity economy
                 importer.economic_complexity = max(0.001,importer.economic_complexity - fertility_economic_change)
        elif (self.economic_complexity < 0.25): # simple economy exporting services or goods
            self.populational_pyramid.change_total_fecundity_rate(+fertility_economic_change)
            if (importer.economic_complexity > 0.75): # to a higher complexity economy
                 importer.economic_complexity = min(1,importer.economic_complexity + fertility_economic_change)
        self.model.increase_channel_usage_rate(self.pos, importer.pos) 

    def try_to_trade_with_neighbors(self):
        # exportação
        potential_nodes_to_export_to = self.model.grid.get_successors(self.pos)#, include_center=False)
        available_nodes_to_export_to = [
            territory
            for territory in self.model.grid.get_cell_list_contents(potential_nodes_to_export_to)
            if territory.state in {CommercialExchangeState.AVAILABLE,CommercialExchangeState.TRADING}
        ]
        for importer in available_nodes_to_export_to:
            if importer.state == CommercialExchangeState.TRADING:
                self.trade_export_to(importer)
            elif self.random.random() < self.trading_spread_chance:
                 # há uma chance de comercializar?
                importer.state = CommercialExchangeState.TRADING # vamos comercializar - eu exporto - o outro importa
                self.trade_export_to(importer)
        # importação
        potential_nodes_to_import_from = self.model.grid.get_predecessors(self.pos)#, include_center=False)
        available_nodes_to_import_from = [
            territory
            for territory in self.model.grid.get_cell_list_contents(potential_nodes_to_import_from)
            if territory.state in {CommercialExchangeState.AVAILABLE,CommercialExchangeState.TRADING}
        ]
        for exporter in available_nodes_to_import_from:
            if exporter.state == CommercialExchangeState.TRADING:
                exporter.trade_export_to(self)
            elif self.random.random() < self.trading_spread_chance: # há uma chance de comercializar
                exporter.state = CommercialExchangeState.TRADING #contamina o vizinho com a prática do comércio
                exporter.trade_export_to(self)
        

    def try_gain_resistance(self):
        if self.random.random() < self.trading_resistance_chance:
            self.state = CommercialExchangeState.RESISTANT

    def try_to_recover(self):
        # Try to recover availability to trade
        if self.random.random() < self.trading_recovery_chance:
            # Success
            self.state = CommercialExchangeState.AVAILABLE

    def try_remove_infection(self):
        # Try to remove
        if self.random.random() < self.trading_recovery_chance:
            # Success
            self.state = CommercialExchangeState.AVAILABLE
            self.try_gain_resistance()
        else:
            # Failed to remove trading behavior
            self.state = CommercialExchangeState.TRADING

    def try_check_situation(self):
        if self.random.random() < self.trading_control_frequency:
            # Checking
            if self.state is CommercialExchangeState.TRADING:
                self.try_remove_infection()

    def update_node_size(self):
        max_size = 6
        self.size = int (math.ceil(self.get_population()*max_size/max(self.model.get_population())))
        return self.size

    def step(self):
        self.internalPopulationalGrowth()
        if self.state is CommercialExchangeState.TRADING:
            self.try_to_trade_with_neighbors()
        elif self.state is CommercialExchangeState.RESISTANT:
            self.try_to_recover()
        self.try_check_situation()
        if (self.visualizing):
            self.update_node_size()



def batch_run():
    fraction = 30000000/211000000 ## inicia com populacao brasileira aproximada, de 1919 (https://seculoxx.ibge.gov.br/images/seculoxx/seculoxx.pdf),
    fixed_params = {
        "fraction_of_brazilian_population": fraction,  
#       "alpha": 0.41, 
#       "gamma": 0.05, 
#       "beta": 0.54, 
        "delta_in": 0.02, 
        "delta_out": 0.02, 
#       "initial_trading_perc": 0.3,
        "trading_spread_chance": 0.5,
        "trading_control_frequency": 0.2,
        "trading_recovery_chance": 0.25,
        "trading_resistance_chance": 0.2,
        "non_trading_decay": 20,
#       "trading_revigoration": 80,
        "visualizing": False
    }

    variable_params = {
        "num_nodes": [10, 20, 40, 80],#, 80, 100, 200, 300, 500],    # 10x - reverte para executar primeiro as simulações mais longas
        "alpha": [0.31, 0.41, 0.51], 
        "beta": [0.31, 0.54, 0.61],
        "gamma": [0.02, 0.05, 0.1], 
        "initial_trading_perc": [0.1, 0.2, 0.4, 0.8], # 2x 
#       "trading_spread_chance": arange(0.1,0.61,0.5), # 2x
#       "trading_control_frequency": arange(0.1,0.61,0.5),
#       "trading_recovery_chance": arange(0.1,0.61,0.5),
#       "trading_resistance_chance": arange(0.1,0.61,0.5), # 2x
#       "non_trading_decay": arange(1,22,20), # 2x
        "trading_revigoration": [20, 40, 80] # 3x
    }

    experiments_per_parameter_configuration = 10
    max_steps_per_simulation = 10
    # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
    batch_run = BatchRunner(
        NetworkOfTerritories,
        variable_params,
        fixed_params,
        iterations=experiments_per_parameter_configuration,#executa cinco vezes a mesma simulacao
        max_steps=max_steps_per_simulation,#simula cem anos de evolucao do territorio
        model_reporters = {
                "AlphaAjuste": alpha,
                "BetaAjuste": beta,
                "GammaAjuste": gamma,
                "InitialPopulation": model_initial_population,
                "FinalPopulation": model_population,
                "Trading": number_trading,
                "Available": number_available,
                "Resistant": number_resistant,
                "StrongComponentsGT1": network_number_strongly_connected_components_not_unitary,
                "Weakcomponents": network_number_weakly_connected_components,
                "Transitivity": network_transitivity,
                "ChannelsDeceasedRate": network_channels_deceased_rate
 #               "Diameter": network_diameter,
 #               "Exccentricity": network_eccentricity
        },
        agent_reporters = {
                "Economic complexity": "economic_complexity",
                "Population": "population",
#                "Size": "size",
                "Trading state": "state"
        }
    )
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.now())
    file_name_suffix =  ("_iter_"+str(experiments_per_parameter_configuration)+
                        "_steps_"+str(max_steps_per_simulation)+"_"+
                        now)
    run_model_data.to_csv("model_data"+file_name_suffix+".csv")
    run_agent_data.to_csv("agent_data"+file_name_suffix+".csv")
    