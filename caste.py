from tools import normalize, symlog
import math


class Caste:
    def __init__(self, caste_data, name):
        """
        :param caste_data: a dictionary of variables to initialize a caste
        """
        self.hist_time = 0  # keeps track of oldest entry in population history
        self.history = [caste_data[f"{name}_initial_population"]]
        self.params = caste_data
        self.s = caste_data[f"{name}_base_survival"]

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        return normalize(self.params["base_survival"], 1)  # this will be normalized

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
        # print(p)
        self.history.append(p)

    def demote(self, factors):
        self.hist_time += 1
        return self.history.pop(0)


class Queen(Caste):
    def __init__(self, params, name):
        super().__init__(params, name)

    def produce(self, factors):
        """
        calculates the amount of eggs laid by the queen in a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors for the current time step
        :return: number of eggs laid in the time step
        """
        return self.params["birth_rate"]

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        x = factors["food_const"] * symlog(factors["food"]-factors["population"]+factors["num_foragers"]) + \
            factors["temp_const"] * (factors["temperature"] - factors["optimal_hive_temp"])
        return normalize(self.s, x)


class Forager(Caste):
    def __init__(self, params, name):
        super().__init__(params, name)

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        x = factors["temp_const"] * symlog(factors["temperature"] - factors["optimal_hive_temp"])
        x = x if factors["num_foragers"] == 0 \
            else x + factors["forage_const"] * symlog(factors["num_plants"]/factors["num_foragers"])
        return normalize(self.s, x)


class Drone(Caste):
    def __init__(self, params, name):
        super().__init__(params, name)

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        x = factors["food_const"] * symlog(factors["food"]-factors["population"]+factors["num_foragers"]) + \
            factors["temp_const"] * symlog(factors["temperature"] - factors["optimal_hive_temp"])
        return normalize(self.s, x)


class Worker(Caste):
    def __init__(self, params, name):
        super().__init__(params, name)

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        x = factors["food_const"] * symlog(factors["food"]-factors["population"]+factors["num_foragers"]) + \
            factors["temp_const"] * symlog(factors["temperature"] - factors["optimal_hive_temp"])

        return normalize(self.s, x)


class Brood(Caste):
    def __init__(self, params, name):
        super().__init__(params, name)

    def survival(self, factors):
        """
        calculates a caste's survival rate for a time step given environmental/hive factors
        :param factors: dictionary of environmental/hive factors
        :return: survival rate <= 1
        """
        x = factors["food_const"] * symlog(factors["food"]-factors["population"]+factors["num_foragers"]) + \
            factors["temp_const"] * symlog(factors["temperature"] - factors["optimal_hive_temp"]) + \
            factors["nurse_const"] * symlog((factors["num_workers"] - factors["num_brood"]))

        return normalize(self.s, x)

    def demote(self, factors):
        if factors["time"] - self.hist_time >= factors["brood_mature_age"]:
            return super().demote(factors)
        else:
            return 0
