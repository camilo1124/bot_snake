from inicioMundo import setup
from agente import Agente
import numpy as np


if __name__ == "__main__":

    driver, actions = setup()
    underdog = Agente(driver)
    underdog.ejecutarRuta()
