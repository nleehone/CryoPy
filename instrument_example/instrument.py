import fcntl as F


class Instrument():
    def get_temperature(self):
        with open("temperature.dat") as file:
            val = file.readline()
            temperature = float(val)
            return temperature

    def set_temperature(self, T):
        with open("temperature.dat", "w") as file:
            file.write(str(T))
