import numpy as np
from datetime import datetime

from mesa.batchrunner import BatchRunner

from forest_fire.model import ForestFire

FIXED_PARAMS = dict(height=100, width=100)
VARIABLE_PARAMS = dict(
    # density = range()
    density=np.linspace(0, 1, 101)[1:],
    relative_humidity = range(1, 101, 1)
    # relative_humidity = np.linspace(0, 100, 101)[1:],
)

EXPERIMENTS_PER_PARAMETER_CONFIG = 1
MAX_STEPS_PER_SIMULATIONS = 1

MODEL_REPORTER = {
    "BurnedOut": lambda m: (
        ForestFire.count_type(m, "Burned Out") / m.schedule.get_agent_count()
    )
}

def simulation():
    results = BatchRunner(
        ForestFire,
        fixed_parameters=FIXED_PARAMS,
        variable_parameters=VARIABLE_PARAMS,
        model_reporters=MODEL_REPORTER,
        iterations=EXPERIMENTS_PER_PARAMETER_CONFIG,
        max_steps=MAX_STEPS_PER_SIMULATIONS,
        display_progress=True,
    )

    results.run_all()

    model_data = results.get_model_vars_dataframe()
    # agent_data = results.get_agent_vars_dataframe()

    now = str(datetime.now())
    file_name_suffix = (
        "_iter_" + str(EXPERIMENTS_PER_PARAMETER_CONFIG) +
        "_steps_" + str(MAX_STEPS_PER_SIMULATIONS) + "_" + now
    )

    model_data.to_csv("model_data" + file_name_suffix + ".csv")
    # agent_data.to_csv("agent_data" + file_name_suffix + ".csv")


if __name__ == "__main__":
    simulation()
