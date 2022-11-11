from hive import Hive
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
from datetime import datetime


def main(global_config, plot=False):
    hive = Hive(global_config)
    temp_data1 = pd.read_csv("Data/DesMoines_2019.csv")
    temp_data2 = pd.read_csv("Data/DesMoines_2018.csv")
    temp_data = pd.concat([temp_data2, temp_data1], ignore_index=True)
    print(temp_data.size)

    time_window = 365 * 2
    for i in range(time_window):
        hive.environment.temperature = temp_data["AvgTemperature"].iloc[i]
        hive.step()

    df = hive.population
    if plot:
        # Saving data
        now = datetime.now().strftime("%H-%M-%S")

        df["Plant"] = hive.environment.population[:time_window]
        df["Temperature"] = temp_data
        df.to_csv(f"Out/Tables/{now}.csv")
        df[["Q", "F", "D", "W", "B", "Plant"]].plot()
        plt.legend(frameon=False)
        plt.savefig(f"Out/Images/{now}.svg")

        with open(f"Out/Params/{now}.json", "w") as f:
            json.dump(global_config, f)

    return round(df.mean().mean())


if __name__ == "__main__":
    with open("Config/global.json") as f:
        global_config = json.load(f)

    #for i in range(1000):
        #delta = -2

    main(global_config, True)
