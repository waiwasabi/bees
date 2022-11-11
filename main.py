from hive import Hive


def main():
    hive = Hive("Config")

    for i in range(365):
        hive.step()
        hive.population.to_csv("output.csv")
        print(hive.environment.history)


if __name__ == "__main__":
    main()
