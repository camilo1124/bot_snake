from capturas import estado
import numpy as np
import cv2
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from queue import PriorityQueue


# from generador_rutas import ruta


class Agente:
    def __init__(self, driver):
        # percepcionInicial = self.sensor()
        self.head_f = 8
        self.head_c = 4
        self.tail_f = 8
        self.tail_c = 2
        self.ruta = np.zeros((17, 19))
        self.inicio = False
        self.objetivo = True
        self.ultimoEstado = None
        self.accionador = ActionChains(driver)
        self.accionPasada = None
        self.celdaObj = None
        self.fase = 1
        self.puntaje = 0

    def generarRuta(self, filaObj=0, columnaObj=0):
        if self.inicio == False:
            self.ruta[self.head_f][self.head_c] = -1
            self.ruta[self.head_f][self.head_c + 1:15] = list(range(1, 11))
            self.inicio = True
        elif self.fase == 1:
            inicio = (self.head_f, self.head_c)
            # puntaje g - costo en paso desde el inicia a una celda
            puntaje_g = {(x, y): float('inf') for x in range(17) for y in range(19)}
            puntaje_f = {(x, y): float('inf') for x in range(17) for y in range(19)}
            puntaje_g[inicio] = 0
            puntaje_f[inicio] = self.h(inicio, self.celdaObj)

            disponibles = PriorityQueue()
            disponibles.put((self.h(inicio, self.celdaObj), self.h(inicio, self.celdaObj), inicio))

            # Estructuración del path o camino

            camino = {}

            while not disponibles.empty():
                celdaActual = disponibles.get()[2]
                if celdaActual == self.celdaObj:
                    break
                coor_f = 25 + (16 + (32 * (celdaActual[0] - 1)))
                coor_c = 28 + (16 + (32 * (celdaActual[1] - 1)))
                unidad_f = 32
                unidad_c = 32
                for d in 'ESNW':
                    if ((100 > self.ultimoEstado[coor_f][coor_c + unidad_c] > 55) or \
                        (0 < self.ultimoEstado[coor_f][coor_c + unidad_c] < 45)) and \
                            d == 'E':
                        celdaVecina = (celdaActual[0], celdaActual[1] + 1)
                        temp_puntaje_g = puntaje_g[celdaActual] + 1
                        temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, self.celdaObj)
                        if temp_puntaje_f < puntaje_f[celdaVecina]:
                            puntaje_g[celdaVecina] = temp_puntaje_g
                            puntaje_f[celdaVecina] = temp_puntaje_f
                            disponibles.put((temp_puntaje_f, self.h(celdaVecina, self.celdaObj), celdaVecina))
                            camino[celdaVecina] = celdaActual
                    if ((100 > self.ultimoEstado[coor_f][coor_c - unidad_c] > 55) or \
                        (0 < self.ultimoEstado[coor_f][coor_c - unidad_c] < 45)) and \
                            d == 'W':
                        celdaVecina = (celdaActual[0], celdaActual[1] - 1)
                        temp_puntaje_g = puntaje_g[celdaActual] + 1
                        temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, self.celdaObj)
                        if temp_puntaje_f < puntaje_f[celdaVecina]:
                            puntaje_g[celdaVecina] = temp_puntaje_g
                            puntaje_f[celdaVecina] = temp_puntaje_f
                            disponibles.put((temp_puntaje_f, self.h(celdaVecina, self.celdaObj), celdaVecina))
                            camino[celdaVecina] = celdaActual
                    if ((100 > self.ultimoEstado[coor_f - unidad_f][coor_c] > 55) or \
                        (0 < self.ultimoEstado[coor_f - unidad_f][coor_c] < 45)) and \
                            d == 'N':
                        celdaVecina = (celdaActual[0] - 1, celdaActual[1])
                        temp_puntaje_g = puntaje_g[celdaActual] + 1
                        temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, self.celdaObj)
                        if temp_puntaje_f < puntaje_f[celdaVecina]:
                            puntaje_g[celdaVecina] = temp_puntaje_g
                            puntaje_f[celdaVecina] = temp_puntaje_f
                            disponibles.put((temp_puntaje_f, self.h(celdaVecina, self.celdaObj), celdaVecina))
                            camino[celdaVecina] = celdaActual
                    if ((100 > self.ultimoEstado[coor_f + unidad_f][coor_c] > 55) or \
                        (0 < self.ultimoEstado[coor_f + unidad_f][coor_c] < 45)) and \
                            d == 'S':
                        celdaVecina = (celdaActual[0] + 1, celdaActual[1])
                        temp_puntaje_g = puntaje_g[celdaActual] + 1
                        temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, self.celdaObj)
                        if temp_puntaje_f < puntaje_f[celdaVecina]:
                            puntaje_g[celdaVecina] = temp_puntaje_g
                            puntaje_f[celdaVecina] = temp_puntaje_f
                            disponibles.put((temp_puntaje_f, self.h(celdaVecina, self.celdaObj), celdaVecina))
                            camino[celdaVecina] = celdaActual



            caminoDelante = {}
            celda = self.celdaObj
            if self.celdaObj in camino:
                while celda != inicio:
                    self.ruta[celda[0]][celda[1]] = puntaje_g[celda]
                    #caminoDelante[camino[celda]] = celda
                    celda = camino[celda]
            else:
                print('mov adicional')
                self.movAdicional()


    def h(self, celda1, celda2):
        x1, y1 = celda1
        x2, y2 = celda2

        return abs(x1 - x2) + abs(y1 - y2)

    def ejecutarRuta(self):
        if self.inicio == False:
            self.generarRuta()
        marca = 1
        hecho = False

        while hecho == False:

            ajuste = self.checkarCambio()

            if ajuste == True:
                #self.imprimir_estado()
                #self.actualizar_cola()
                if self.ruta[self.head_f][self.head_c - 1] == marca:

                    if self.accionPasada != 'ARROW_LEFT':
                        self.accionPasada = 'ARROW_LEFT'
                        self.accionador.send_keys(Keys.ARROW_LEFT)
                        self.accionador.perform()

                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c -= 1
                    self.ruta[self.head_f][self.head_c] = (-1)
                    marca += 1


                elif self.ruta[self.head_f][self.head_c + 1] == marca:

                    if self.accionPasada != 'ARROW_RIGHT':
                        self.accionPasada = 'ARROW_RIGHT'
                        self.accionador.send_keys(Keys.ARROW_RIGHT)
                        self.accionador.perform()
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c += 1
                    self.ruta[self.head_f][self.head_c] = (-1)
                    marca += 1



                elif self.ruta[self.head_f + 1][self.head_c] == marca:
                    if self.accionPasada != 'ARROW_DOWN':
                        self.accionPasada = 'ARROW_DOWN'
                        self.accionador.send_keys(Keys.ARROW_DOWN)
                        self.accionador.perform()

                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f += 1
                    self.ruta[self.head_f][self.head_c] = (-1)
                    marca += 1


                elif self.ruta[self.head_f - 1][self.head_c] == marca:
                    if self.accionPasada != 'ARROW_UP':
                        self.accionPasada = 'ARROW_UP'
                        self.accionador.send_keys(Keys.ARROW_UP)
                        self.accionador.perform()
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f -= 1
                    self.ruta[self.head_f][self.head_c] = (-1)
                    marca += 1


                else:

                    #fila, columna = self.busquedaLineal(matriz)
                    fila, columna = self.busquedaLineal()
                    if fila != -1:
                        self.celdaObj = (fila, columna)
                        self.generarRuta(fila, columna)
                        self.objetivo = False
                        marca = 1
                    else:
                        self.movAdicional()
                        marca = 1

    def checkarCambio(self):

        if self.objetivo:
            estado()
            imagen = cv2.imread("frames\prueba.bmp")

            #matriz_colores = cv2.resize(imagen, None, fx=0.031, fy=0.0315)
            #self.ultimoEstado = matriz_colores[:, :, 0]

            self.ultimoEstado = imagen[:,:,0]
            coor_f = 25 + (16 + (32 * (self.head_f - 1)))
            coor_c = 28 + (16 + (32 * (self.head_c - 1)))

            if self.ultimoEstado[coor_f][coor_c] >= 245:
                    return True
            else:
                return False
        else:
            self.objetivo = True
            return True

    def busquedaLineal(self):

        for fila in range(1, 16):
            for columna in range(1, 18):
                coor_f = 25 + (16 + (32 * (fila - 1)))
                coor_c = 28 + (16 + (32 * (columna - 1)))
                if self.ultimoEstado[coor_f][coor_c] <= 35:
                    return fila, columna
        return -1, -1

    def movAdicional(self):
        mitadHor = 8
        mitadVer = 9
        coor_f = 25 + (16 + (32 * (self.head_f - 1)))
        coor_c = 28 + (16 + (32 * (self.head_c - 1)))
        unidad_f = 32
        unidad_c = 32
        if self.accionPasada == 'ARROW_UP' or self.accionPasada == 'ARROW_DOWN':
            if self.head_c < mitadVer:
                if self.ultimoEstado[coor_f][coor_c + unidad_c] == 81 or \
                        self.ultimoEstado[coor_f][coor_c + unidad_c] == 73:
                    self.accionador.send_keys(Keys.ARROW_RIGHT)
                    self.accionador.perform()
                    self.accionPasada = 'ARROW_RIGHT'
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c += 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_UP':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_DOWN':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f += 1
                    self.ruta[self.head_f][self.head_c] = -1

            elif self.head_c >= mitadVer:
                if self.ultimoEstado[coor_f][coor_c - unidad_c] == 81 or \
                        self.ultimoEstado[coor_f][self.head_c - 1] == 73:
                    self.accionador.send_keys(Keys.ARROW_LEFT)
                    self.accionador.perform()
                    self.accionPasada = 'ARROW_LEFT'
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_UP':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_DOWN':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f += 1
                    self.ruta[self.head_f][self.head_c] = -1

            return

        elif self.accionPasada == 'ARROW_RIGHT' or self.accionPasada == 'ARROW_LEFT':
            if self.head_f < mitadHor:
                if self.ultimoEstado[coor_f + unidad_f][coor_c] == 81 or \
                        self.ultimoEstado[coor_f + unidad_f][coor_c] == 73:
                    self.accionador.send_keys(Keys.ARROW_DOWN)
                    self.accionador.perform()
                    self.accionPasada = 'ARROW_DOWN'
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f += 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_LEFT':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_RIGHT':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c += 1
                    self.ruta[self.head_f][self.head_c] = -1

            elif self.head_f >= mitadHor:
                if self.ultimoEstado[coor_f - unidad_f][coor_c] == 81 or \
                        self.ultimoEstado[coor_f - unidad_f][coor_c] == 73:
                    self.accionador.send_keys(Keys.ARROW_UP)
                    self.accionador.perform()
                    self.accionPasada = 'ARROW_UP'
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_f -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_LEFT':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c -= 1
                    self.ruta[self.head_f][self.head_c] = -1
                elif self.accionPasada == 'ARROW_RIGHT':
                    self.ruta[self.head_f][self.head_c] = 0
                    self.head_c += 1
                    self.ruta[self.head_f][self.head_c] = -1

            return

    def imprimir_estado(self):
        print('Estado\n')
        for fila in range(1, 16):
            print('\n')
            for columna in range(1, 18):
                coor_f = 25 + (16 + (32 * (fila - 1)))
                coor_c = 28 + (16 + (32 * (columna - 1)))
                print(self.ultimoEstado[coor_f][coor_c], end= "\t")
        return

    def actualizar_cola(self):
        coor_f = 25 + (16 + (32 * (self.tail_f - 1)))
        coor_c = 28 + (16 + (32 * (self.tail_c - 1)))
        unidad_f = 32
        unidad_c = 32
        print(self.tail_f,self.tail_c)
        if 220 <=  self.ultimoEstado[coor_f][coor_c] <= 225:
            return
        elif 220 <=  self.ultimoEstado[coor_f - unidad_f][coor_c] <= 225:
            self.tail_f -= 1
            return
        elif 220 <=  self.ultimoEstado[coor_f][coor_c - unidad_c] <= 225:
            self.tail_c -= 1
            return
        elif 220 <=  self.ultimoEstado[coor_f][coor_c + unidad_c] <= 225:
            self.tail_c += 1
            return
        elif 220 <=  self.ultimoEstado[coor_f + unidad_f][coor_c] <= 225:
            self.tail_f += 1
            return
        elif 220 <=  self.ultimoEstado[coor_f - unidad_f][coor_c - unidad_c] <= 225:
            self.tail_f -= 1
            self.tail_c -= 1
            return
        elif 220 <=  self.ultimoEstado[coor_f - unidad_f][coor_c + unidad_c] <= 225:
            self.tail_f -= 1
            self.tail_c += 1
            return
        elif 220 <=  self.ultimoEstado[coor_f + unidad_f][coor_c - unidad_c] <= 225:
            self.tail_f += 1
            self.tail_c -= 1
            return
        elif 220 <=  self.ultimoEstado[coor_f + unidad_f][coor_c + unidad_c] <= 225:
            self.tail_f += 1
            self.tail_c += 1
            return

