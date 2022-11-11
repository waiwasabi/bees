import pandas as pd
from environment import Environment
from caste import Queen, Forager, Drone, Worker, Brood
import json
import os


class Hive:
    def __init__(self, config_dir):
        with open(os.path.join(config_dir, "global.json")) as f:
            self.global_config = json.load(f)

        headers = ["Q", "F", "D", "W", "B"]
        castes = [Queen, Forager, Drone, Worker, Brood]
        config = []

        for h in headers:
            f = open(os.path.join(config_dir, f"{h}.json"))
            config.append(json.load(f))
            f.close()

        self.k = {h: c(cfg) for h, c, cfg in zip(headers, castes, config)}
        self.population = pd.DataFrame(columns=headers)
        self.environment = Environment()
        self.time = 0

    # TODO: get environmental factors
    def get_factors(self):
        factors = {
            **{"temp": self.environment.temperature,
               "time": self.time,
               },
            **self.global_config
        }
        return factors

    def get_population(self):
        return [caste.get_population() for caste in self.k.values()]

    def step(self):
        # interact with environment
        # calculate survival and update caste states
        # increment time and store data

        factors = self.get_factors()  # get environmental/hive factors
        delta = self.k["Q"].produce(factors)  # queen lays eggs
        self.k["B"].promote(delta)  # add eggs to brood
        mature = self.k["B"].demote(factors)  # get number of brood that have matured

        for k, v in self.global_config["promotion_distribution"].items():  # promotion scheme is constant.
            self.k[k].promote(mature * v)

        # TODO: promotion/demotion between workers and foragers?

        for k in self.k.values():  # update caste states
            k.step(factors)

        self.population.loc[self.time] = self.get_population()
        self.time += 1
