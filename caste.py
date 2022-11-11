

class Caste:
    def __init__(self, caste_data):
        """
        :param caste_data: a dictionary of variables to initialize a caste
        """
        self.hist_time = 0  # keeps track of oldest entry in population history
        self.history = [caste_data["initial_population"]]
        self.params = caste_data

    # TODO: implement model for survival rate
    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        return self.params["base_survival"] * 1  # this will be normalized

    def get_population(self):
        return round(sum(self.history))

    def step(self, factors):
        """
        configures the population change in a caste after one time step.
        :param factors: dictionary of environmental/hive factors
        """
        s = self.survival(factors)
        self.history = [h * s for h in self.history]

    def promote(self, p):
        self.history.append(p)

    def demote(self, factors):
        self.hist_time += 1
        return self.history.pop(0)


class Queen(Caste):
    def __init__(self, queen_params):
        super().__init__(queen_params)

    # TODO: implement model for egg production
    def produce(self, factors):
        """
        calculates the amount of eggs laid by the queen in a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors for the current time step
        :return: number of eggs laid in the time step
        """
        return self.params["birth_rate"]


class Forager(Caste):
    def __init__(self, forager_params):
        super().__init__(forager_params)


class Drone(Caste):
    def __init__(self, drone_params):
        super().__init__(drone_params)


class Worker(Caste):
    def __init__(self, worker_params):
        super().__init__(worker_params)


class Brood(Caste):
    def __init__(self, brood_params):
        super().__init__(brood_params)

    def demote(self, factors):
        if factors["time"] - self.hist_time >= factors["brood_mature_age"]:
            return super().demote(factors)
        else:
            return 0
