import random
from deap import base, creator, tools, algorithms
import numpy as np
import requests
import json


class FlowOptimizer:
    def __init__(self, output_goal, num_of_controls, floor, ceiling):
        self.output_goal = output_goal
        self.floor = floor
        self.ceiling = ceiling
        self.timestamp = ""
        self.headwater = 0
        self.tailwater = 0
        self.timeseries_name = ""

        # Set creation parameters
        creator.create(name="FitnessMax", base=base.Fitness, weights=(-1.0,))
        creator.create(name="Individual", base=list, fitness=creator.FitnessMax)

        # Create toolbox for creating individuals
        self.toolbox = base.Toolbox()

        # Register create value
        self.toolbox.register(alias="attr_value", function=self.__create_value)

        # Register individual creation
        self.toolbox.register("individual", tools.initRepeat,
                              creator.Individual, self.toolbox.attr_value,
                              n=num_of_controls)

        # Register population creation
        self.toolbox.register("population", tools.initRepeat,
                              list, self.toolbox.individual)

        # Register evaluation, mutation, and other algorithm functions
        self.toolbox.register("evaluate", self.get_fitness)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self.__mutate, indpb=1 / num_of_controls)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    # Run simulation and return the fittest individual
    def optimize(self, timestamp, headwater, tailwater, timeseries_name):
        self.timestamp = timestamp
        self.headwater = headwater
        self.tailwater = tailwater
        self.timeseries_name = timeseries_name

        # Create population
        pop = self.toolbox.population(n=10)

        # Create hall of fame
        hof = tools.HallOfFame(1)

        # Register statistical tools
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)

        # Run algorithm
        algorithms.eaSimple(pop, self.toolbox,
                            cxpb=0.5, mutpb=0.5,
                            ngen=50, stats=stats,
                            halloffame=hof, verbose=True)

        # Return fittest individual
        return hof[0]

    # Create random initial values
    def __create_value(self):
        return random.uniform(self.floor, self.ceiling)

    # Score individual fitness
    def get_fitness(self, individual):

        # Get the output value
        output_value = self.get_output(self.timestamp, self.headwater,
                                       self.tailwater, individual,
                                       self.timeseries_name)

        # Get fitness
        fitness = abs(output_value - self.output_goal)
        return fitness,

    # Get the output value
    def get_output(self, timestamp, headwater, tailwater, individual, timeseries_name):

        # Build control values
        controls = []
        for i, value in enumerate(individual):
            controls.append({'value': value,
                             'tag': '',
                             'number': i})

        # Build request url, headers, and payload
        url = "http://api.sfwmd.gov/flow/calc"
        headers = {'Accept': 'application/vnd.gov.sfwmd.StationIDFlowResult-v2+json',
                   'Content-Type': 'application/vnd.gov.sfwmd.StationIDInputRecord-v2+json'}
        payload = {
            "gov.sfwmd.StationIDInputRecord-v2": {
                "timestamp": timestamp,
                "hw": headwater,
                "hwTag": "",
                "tw": tailwater,
                "twTag": "",
                "controls": {
                    "control": controls
                },
                "timeSeriesName": timeseries_name
            }
        }

        # Send request and get json response
        r = requests.post(url=url, headers=headers, data=json.dumps(payload))
        json_response = r.json()

        # Get the flow value
        flow_results = json_response.get('gov.sfwmd.StationIDFlowResult-v2');
        flow_value = float(flow_results.get('value'))
        return flow_value

    # Mutate genes
    def __mutate(self, individual, indpb):
        for i in range(len(individual)):
            if random.random() <= indpb:
                individual[i] = self.__create_value()
        return individual,
