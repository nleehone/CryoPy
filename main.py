import visa
from drivers import LS350


if __name__ == '__main__':
    rm = visa.ResourceManager('instruments.yaml@sim')
    driver = LS350(rm.open_resource('ASRL1::INSTR'))
    print(driver.resource)
    print(driver.resource.__class__)
    driver.clear_interface()
    print(driver.identification_query())