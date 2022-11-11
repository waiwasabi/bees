from hive import Hive
import matplotlib.pyplot as plt
import pandas as pd


def main():
    hive = Hive("Config")
    temp_data = pd.read_csv("Data/Anchorage_2019.csv")
    for i in range(365):
        hive.environment.temperature = temp_data["AvgTemperature"].iloc[i]
        hive.step()

    hive.population.to_csv("output.csv")
    hive.population.plot()
    plt.show()
    print(sum(hive.environment.history))
    print(hive.food)


if __name__ == "__main__":
    main()
