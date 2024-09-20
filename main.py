# import car.py and cars.py
# create two car objects
# print the charging duration for each car object

import car


def main():
    car1 = car.Car(75000, 50000)
    car2 = car.Car(75000, 30000)

    print(car1.calculate_charging_duration(60000, 10000))
    print(car2.calculate_charging_duration(40000, 10000))




if __name__ == "__main__":
    main()
    