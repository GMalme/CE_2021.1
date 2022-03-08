from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .portrayal import portrayCell
from .model import ConwaysGameOfLife
from mesa.visualization.modules import ChartModule

# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 250, 250)

neighborhood_map = ChartModule(
    [
        {"Label": "Density", "Color": "#FF3C33"}, #RED
    ]
)

server = ModularServer(
    ConwaysGameOfLife, 
    [canvas_element, neighborhood_map], 
    "Game of Life", 
    {
        "height": 50, 
        "width": 50, 
        "density": UserSettableParameter(
            "slider",
            "Chance of initiating alive",
            0.1,
            0.01,
            1,
            0.01,
            description="Choose chance of each cell being alive",),
        "revival": UserSettableParameter(
            "slider",
            "Chance of reviving",
            0.1,
            0.01,
            1,
            0.01,
            description="Choose chance of dead cells coming randomly to life",)
    }
)
