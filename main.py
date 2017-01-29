import visa
from drivers.LS350 import *


if __name__ == '__main__':
    rm = visa.ResourceManager('instruments.yaml@sim')
    driver = LS350(rm.open_resource('ASRL1::INSTR'))
    print(driver.resource)
    print(driver.resource.__class__)
    driver.clear_interface()
    print(driver.identification_query())
    print(driver.resource.query('SRDG? A; KRDG? B'))
    print(driver.get_temperature('A', Temperature.C))
