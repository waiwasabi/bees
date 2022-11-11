from tools import normalize, symlog


class Environment:
    def __init__(self, environment_data):
        self.temperature = None
        self.history = [environment_data["initial_plants"]]
        self.params = environment_data

    def step(self, factors):
        s = self.survival(factors)
        self.history = [h * s for h in self.history]
        p = round(sum(self.history))
        # add plants for the next time-step based on current data
        self.history.append(self.params["gamma"] * self.pollinate(self.get_mature_plants(), factors["num_foragers"]))

        return p

    def survival(self, factors):
        """
        calculates the plant population change after one time step.
        :param factors: dictionary of environmental/hive factors. Must contain temperature parameter.
        """
        temp = self.params["temp_sensitivity"]*(factors["temperature"]-self.params["optimal_temp"])
        return normalize(self.params["plant_base_survival"], symlog(temp))

    def get_mature_plants(self):
        """
        calculates the number of mature plants available for pollination.
        :return: the number of mature plants available for pollination.
        """
        if len(self.history) < self.params["mu"]:
            return 0
        else:
            return round(sum(self.history[:-self.params["mu"]]))

    def pollinate(self, x, y):
        """
        :param x: number of mature plants
        :param y: number of foragers
        :return: number of plants pollinated
        """
        return 0 if x == 0 else x - x*(1-((x-1)/x)**(self.params["phi"]*y))
