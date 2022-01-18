from mesa.visualization.ModularVisualization import ModularServer
from .model import HumorAcademicoModel
from .model import Humor
from .model import Poliglota
from .model import Experiencia

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if (agent.humor == Humor.BEMHUMORADO) : #in {Humor.BEMHUMORADO}):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.8
    elif (agent.humor == Humor.NEUTRO): # in {Humor.NEUTRO}):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    else: # mal humorado
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    return portrayal

width_height = 10

grid = CanvasGrid(agent_portrayal, width_height, width_height, 500, 500)
chart = ChartModule(
    [{"Label": "Humor", "Color": "#0000FF"}], data_collector_name="datacollector"
)

model_params = {
    "N": UserSettableParameter(
        "slider",
        "Number of academics",
        100,
        500,
        5000,
        100,
        description="Choose how many academics are classifying journals",
    ),
    "width_height": width_height
}

server = ModularServer(HumorAcademicoModel, [grid, chart], "Modelando a variação de humor dos acadêmicos", model_params)
server.port = 8521
