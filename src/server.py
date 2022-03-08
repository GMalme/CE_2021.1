from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .agents import SsAgent, Sugar
from .model import SugarscapeCg

# Linear interpolation from x0 to x1. t goes from 0 to 1
def lerp(x0, x1, t):
    return x0 * (1 - t) + x1 * t

def lerp_vec(it0, it1, t):
    return [lerp(x, y, t) for x, y in zip(it0, it1)]

def color(amount):
    color0 = [71, 23, 72]
    color1 = [141, 69, 34]
    [h, s, l] = lerp_vec(color0, color1, amount / 3)
    return "hsl({}, {}%, {}%)".format(h, s, l)

def SsAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is SsAgent:
        portrayal["Shape"] = "src/resources/ant.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sugar:
        portrayal["Color"] = color(agent.amount)
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "SsAgent", "Color": "#AA0000"}])

params = {
    "reproduce_prob": UserSettableParameter(
        param_type="slider",
        name="Ant Reproduce Probability",
        value=0.15,
        min_value=0.0,
        max_value=0.5,
        step=0.05,
        description="Probability that a given ant reproduces in some step of the simulation",
    ),
    "growback_factor": UserSettableParameter(
        param_type="slider",
        name="Growback Factor",
        value=0.1,
        min_value=0,
        max_value=3,
        step=0.05,
        description="Amount that every sugarcane grows by each step",
    ),
}

server = ModularServer(
    SugarscapeCg, [canvas_element, chart_element], "Sugarscape 2 Constant Growback", params
)
# server.launch()
