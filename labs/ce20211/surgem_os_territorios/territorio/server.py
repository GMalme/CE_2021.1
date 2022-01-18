import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from model import NetworkOfTerritories, CommercialExchangeState, number_trading, network_channels_deceased_rate, model_initial_population
import seaborn as sns
import statistics

def territory_network_portrayal(G):
    # The model ensures there is always 1 territory per node

    def node_color(territory):
        return {CommercialExchangeState.TRADING: "#FF0000", CommercialExchangeState.AVAILABLE: "#008000"}.get(
            territory.state, "#808080"
        )

    def node_size(territory):
        return territory.size

    def edge_color(territory1, territory2):
        usage_palette = sns.color_palette("crest",100).as_hex()
        edge_data = G.get_edge_data(territory1.unique_id , territory2.unique_id)
        if (edge_data is None):
            print("Arco ["+territory1.unique_id+""+territory2.unique_id+" Inexiste!")
            return 1
        else:
            usage_rate = edge_data['usage']
            return usage_palette[usage_rate-1]

    def edge_width(territory1, territory2):
        edge_data = G.get_edge_data(territory1.unique_id , territory2.unique_id)
        if (edge_data is None):
            print("Arco ["+territory1.unique_id+""+territory2.unique_id+" Inexiste!")
            return 1
        else:
            return edge_data['weight']

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    def get_agent_id(agent):
        n = G.nodes[agent]
        o = n["agent"]
        p = o[0]
        q = p.unique_id
        return G.nodes[agent]["agent"][0].unique_id

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": agent[0].size,
            "color": node_color(agent[0]),
            "tooltip": ("id: {}<br>Trading state: {} <br>Population: {}<br>Economic complexity:{}<br>{}".format(
                agent[0].unique_id, 
                agent[0].state.name, 
                "{:,}".format(round(agent[0].populational_pyramid.pop_total())),
                round(agent[0].economic_complexity,3),
                "".join([str(l)+"<br>" for l in agent[0].populational_pyramid.to_string()])
            )
            ),
        }
        for (_, agent) in sorted(G.nodes.data("agent"))
    ]

    portrayal["edges"] = [
        {
            "source": get_agent_id(source),
            "target": get_agent_id(target),
            "color": edge_color(*get_agents(get_agent_id(source), get_agent_id(target))),
            "width": edge_width(*get_agents(get_agent_id(source), get_agent_id(target))),
            "directed": True,
            "tooltip": "from source: {} to target: {}<br>width: {}".format(
                get_agent_id(source), get_agent_id(target), edge_width(*get_agents(get_agent_id(source), get_agent_id(target))))
        }
        for (source, target) in G.edges
    ]

    return portrayal


network = NetworkModule(territory_network_portrayal, 500, 500, library="directed_d3")
chart = ChartModule(
    [
        {"Label": "Trading", "Color": "#FF0000"},
        {"Label": "Available", "Color": "#008000"},
        {"Label": "Resistant", "Color": "#808080"},
        {"Label": "StrongComponentsGT1", "Color": "#0000FF"},
        {"Label": "Weakcomponents", "Color": "#00FFFF"}
    ]
)


class MyTextElement(TextElement):
    def render(self, model):
        ratio = model.resistant_available_ratio()
        ratio_text = "&infin;" if ratio is math.inf else "{0:.2f}".format(ratio)
        infected_text = str(number_trading(model))
        population_list = model.get_population()
        initial_population = model_initial_population(model)
        deceased_rate = network_channels_deceased_rate(model) 
        return ("Initial Network Population: {}<br>"+
            "Total Network Population: {}<br>"+
            "Median Territory Population: {}<br>"+
            "Max Territory Population: {}<br>"+
            "Min Territory Population: {}<br>"+
            "Average Territory Population: {}<br>"+
            "StdDev Territory Population: {}<br>"+
            "Ratio Resistants/Available: {}<br>"+
            "Trading: {}<br>"+
            "Channels deceased/step: {}").format(
                "{:,}".format(int(initial_population)), 
                "{:,}".format(int(sum(population_list))), 
                "{:,}".format(int(statistics.median(population_list))), 
                "{:,}".format(int(max(population_list))), 
                "{:,}".format(int(min(population_list))), 
                "{:,}".format(int(statistics.mean(population_list))), 
                "{:,}".format(int(statistics.stdev(population_list))), 
                ratio_text, 
                infected_text,
                deceased_rate
        )


model_params = {
    "num_nodes": UserSettableParameter(
        "slider",
        "# of Base-Territories",
        10,
        10,
        5010,
        100,
        description="Choose how many territories create",
    ),
    "fraction_of_brazilian_population": UserSettableParameter(
        "slider",
        "Fraction of Brazílian Population",
        30/211, # Brazil's population in 2019
        0.01,
        50,
        0.01,
        description="Chose the initial population of the network, relative to Brazil's 2019 population",
    ),
    "alpha": UserSettableParameter(
        "slider", 
        "Alpha (links from new nodes biased to importers).",
        0.41, 
        0.00, 
        1, 
        0.01, 
        description=("Alpha: Probability for adding a new node connected to an existing node "+
            "chosen randomly according to the in-degree distribution.")
    ),
    "gamma": UserSettableParameter(
        "slider", 
        "Gamma (links from new nodes biased to exporters).", 
        0.05, 
        0.00, 
        1, 
        0.01, 
        description=("Gamma: Probability for adding a new node connected to an existing node "+
        "chosen randomly according to the out-degree distribution.")
    ),
    "beta": UserSettableParameter(
        "slider", 
        "Beta (links between old nodes biased by import-export).", 
        0.54, 
        0.00, 
        1, 
        0.01, 
        description=("Beta: Probability for adding an edge between two existing nodes."+
        " One existing node is chosen randomly according the in-degree distribution "+
        "and the other chosen randomly according to the out-degree distribution.")
    ),
    "delta_in": UserSettableParameter(
        "slider", 
        "delta_in (choose territories biased by import strength).", 
        0.02, 
        0.00, 
        1, 
        0.01, 
        description=("delta_in: Bias for choosing nodes from in-degree distribution.")
    ),
    "delta_out": UserSettableParameter(
        "slider", 
        "delta_out (choose territories biased by export strength).", 
        0.00, 
        0.00, 
        1, 
        0.01, 
        description=("delta_out: Bias for choosing nodes from out-degree distribution.")
    ),
    "initial_trading_perc": UserSettableParameter(
        "slider",
        "% of initial territories that are trading",
        0.5,
        0.0,
        1,
        0.1,
        description="% Territories Trading",
    ),
    "trading_spread_chance": UserSettableParameter(
        "slider",
        "Trading practices spread chance",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Probability that susceptible neighbor will be trading",
    ),
    "trading_control_frequency": UserSettableParameter(
        "slider",
        "Trading control frequency (state regulation)",
        0.4,
        0.0,
        1.0,
        0.1,
        description="Frequency the state check whether the territory is trading",
    ),
    "trading_recovery_chance": UserSettableParameter(
        "slider",
        "Trading recovery chance (after being contamined by trade ideas)",
        0.3,
        0.0,
        1.0,
        0.1,
        description="Probability that the territory will return to trading practices",
    ),
    "trading_resistance_chance": UserSettableParameter(
        "slider",
        "Trading resistance chance (territorry refuses to trade)",
        0.5,
        0.0,
        1.0,
        0.1,
        description="Probability that a recovered territory will refuse further trading",
    ),
    "non_trading_decay": UserSettableParameter(
        "slider",
        "Non-trading channel decay",
        20,
        1,
        100,
        1,
        description="Percent of decay for channel not used in a step",
    ),
    "trading_revigoration": UserSettableParameter(
        "slider",
        "Revigoration of channel for usage",
        50,
        1,
        100,
        1,
        description="Percent of revigoration that a channel receives for being used for trading",
    ),
    "visualizing": True,
    "seed": 1
}

server = ModularServer(
    NetworkOfTerritories, [network, MyTextElement(), chart], "Modeling Territories of Knowledge Production", model_params
)
server.port = 8521
