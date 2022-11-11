from environment import Environment
from hive import Hive


def main():
    hive = Hive("Config")
    env = Environment()

    for i in range(365):
        hive.step()
        hive.population.to_csv("output.csv")


if __name__ == "__main__":
    main()
