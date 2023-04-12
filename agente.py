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
        self.ruta = np.zeros((17, 19),dtype=int)
        self.inicio = False
        self.objetivo = True
        self.ultimoEstado = None
        self.accionador = ActionChains(driver)
        self.accionPasada = None
        self.celdaObj = None
        self.fase = 1
        self.valor_cola = 229
        self.simulacionEstado = np.full((17, 19),52,dtype=int)
        self.simulacion_head_f = None
        self.simulacion_head_c = None
        self.simulacion_tail_f = None
        self.simulacion_tail_c = None
        self.tam_registro = None
        self.rutaSegura = None
        self.peligro = None


    def generarRuta(self, filaObj=0, columnaObj=0):
        if self.inicio == False:
            self.ruta[self.head_f][self.head_c] = -1
            self.ruta[self.head_f][self.head_c + 1:15] = list(range(1, 11))
            self.inicio = True
        elif self.fase == 1:
            self.a_estrella1()


    def a_estrella1(self):
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

        #caminoDelante = {}
        celda = self.celdaObj
        if self.celdaObj in camino:
            while celda != inicio:
                self.ruta[celda[0]][celda[1]] = puntaje_g[celda]
                celda = camino[celda]
            if self.verificacion2():
                return
            elif self.verificacion(puntaje_g[self.celdaObj]):
                return
            else:
                self.borrarRuta()
                self.a_estrella3(self.head_f, self.head_c, self.tail_f, self.tail_c)
        else:
            self.a_estrella3(self.head_f, self.head_c, self.tail_f, self.tail_c)

    def a_estrella2(self,f_inicio,c_inicio,f_obj,c_obj):
        inicio = (f_inicio,c_inicio)
        objetivo = (f_obj,c_obj)
        # puntaje g - costo en paso desde el inicia a una celda
        puntaje_g = {(x, y): float('inf') for x in range(17) for y in range(19)}
        puntaje_f = {(x, y): float('inf') for x in range(17) for y in range(19)}
        puntaje_g[inicio] = 0
        puntaje_f[inicio] = self.h(inicio, objetivo)

        disponibles = PriorityQueue()
        disponibles.put((self.h(inicio, objetivo), self.h(inicio, objetivo), inicio))

        # Estructuración del path o camino

        camino = {}

        while not disponibles.empty():
            celdaActual = disponibles.get()[2]
            if celdaActual == objetivo:
                break
            for d in 'ESNW':
                if ((100 > self.simulacionEstado[celdaActual[0]][celdaActual[1] + 1] > 55) or \
                    (f_obj == celdaActual[0] and c_obj == celdaActual[1] + 1))\
                        and \
                        d == 'E':
                    celdaVecina = (celdaActual[0], celdaActual[1] + 1)
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.simulacionEstado[celdaActual[0]][celdaActual[1] - 1] > 55) or \
                    (f_obj == celdaActual[0] and c_obj == (celdaActual[1] - 1))) and \
                        d == 'W':
                    celdaVecina = (celdaActual[0], celdaActual[1] - 1)
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.simulacionEstado[celdaActual[0] - 1][celdaActual[1]] > 55) or \
                    (f_obj == (celdaActual[0] - 1) and c_obj == celdaActual[1])) and \
                        d == 'N':
                    celdaVecina = (celdaActual[0] - 1, celdaActual[1])
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.simulacionEstado[celdaActual[0] + 1][celdaActual[1]] > 55) or \
                    (f_obj == (celdaActual[0] + 1) and c_obj == celdaActual[1])) and \
                        d == 'S':
                    celdaVecina = (celdaActual[0] + 1, celdaActual[1])
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual

        # caminoDelante = {}
        #celda = objetivo
        if objetivo in camino:
            return True
        else:
            return False
    def a_estrella3(self,f_inicio,c_inicio,f_obj,c_obj):
        inicio = (f_inicio,c_inicio)
        objetivo = (f_obj,c_obj)
        # puntaje g - costo en paso desde el inicia a una celda
        puntaje_g = {(x, y): float('inf') for x in range(17) for y in range(19)}
        puntaje_f = {(x, y): float('inf') for x in range(17) for y in range(19)}
        puntaje_g[inicio] = 0
        puntaje_f[inicio] = self.h(inicio, objetivo)

        disponibles = PriorityQueue()
        disponibles.put((self.h(inicio, objetivo), self.h(inicio, objetivo), inicio))

        # Estructuración del path o camino

        camino = {}

        while not disponibles.empty():
            celdaActual = disponibles.get()[2]
            if celdaActual == objetivo:
                break
            coor_f = 25 + (16 + (32 * (celdaActual[0] - 1)))
            coor_c = 28 + (16 + (32 * (celdaActual[1] - 1)))
            unidad_f = 32
            unidad_c = 32
            for d in 'ESNW':
                if ((100 > self.ultimoEstado[coor_f][coor_c + unidad_c] > 55) or \
                    (f_obj == celdaActual[0] and c_obj == celdaActual[1] + 1))\
                        and \
                        d == 'E':
                    celdaVecina = (celdaActual[0], celdaActual[1] + 1)
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.ultimoEstado[coor_f][coor_c - unidad_c] > 55) or \
                    (f_obj == celdaActual[0] and c_obj == (celdaActual[1] - 1))) and \
                        d == 'W':
                    celdaVecina = (celdaActual[0], celdaActual[1] - 1)
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.ultimoEstado[coor_f - unidad_f][coor_c] > 55) or \
                    (f_obj == (celdaActual[0] - 1) and c_obj == celdaActual[1])) and \
                        d == 'N':
                    celdaVecina = (celdaActual[0] - 1, celdaActual[1])
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual
                if ((100 > self.ultimoEstado[coor_f + unidad_f][coor_c] > 55) or \
                    (f_obj == (celdaActual[0] + 1) and c_obj == celdaActual[1])) and \
                        d == 'S':
                    celdaVecina = (celdaActual[0] + 1, celdaActual[1])
                    temp_puntaje_g = puntaje_g[celdaActual] + 1
                    temp_puntaje_f = temp_puntaje_g + self.h(celdaVecina, objetivo)
                    if temp_puntaje_f < puntaje_f[celdaVecina]:
                        puntaje_g[celdaVecina] = temp_puntaje_g
                        puntaje_f[celdaVecina] = temp_puntaje_f
                        disponibles.put((temp_puntaje_f, self.h(celdaVecina, objetivo), celdaVecina))
                        camino[celdaVecina] = celdaActual

        celda = objetivo

        if objetivo in camino:
            while celda != inicio:
                self.ruta[celda[0]][celda[1]] = puntaje_g[celda]
                celda = camino[celda]
        else:
            print("no se anexo o encontro la cola")
            print(objetivo)
            print(objetivo in camino)

    def verificacion(self,n):
        self.simulacion(n)
        return self.a_estrella2(self.simulacion_head_f,self.simulacion_head_c,self.simulacion_tail_f \
                                ,self.simulacion_tail_c)


    def simulacion(self,n):
        self.copiaEstado()
        self.simulacion_head_f = self.head_f
        self.simulacion_head_c = self.head_c
        self.simulacion_tail_f = self.tail_f
        self.simulacion_tail_c = self.tail_c
        #self.longitud = self.tamanoSimulacion(n)
        """
        print("Coordenadas cabeza")
        print((self.simulacion_head_f,self.simulacion_head_c))
        print("Coordenadas cola")
        print((self.simulacion_tail_f, self.simulacion_tail_c))
        """
        inicio = self.simulacionEstado[self.simulacion_head_f][self.simulacion_head_c]


        for marca_s in range(1, n + 1):
            if self.ruta[self.simulacion_head_f][self.simulacion_head_c - 1] == marca_s:
                self.simulacion_head_c -= 1
                self.simulacionEstado[self.simulacion_head_f][self.simulacion_head_c] = inicio + marca_s
                self.actualizar_cola_simulada()

            elif self.ruta[self.simulacion_head_f][self.simulacion_head_c + 1] == marca_s:
                self.simulacion_head_c += 1
                self.simulacionEstado[self.simulacion_head_f][self.simulacion_head_c] = inicio + marca_s
                self.actualizar_cola_simulada()

            elif self.ruta[self.simulacion_head_f + 1][self.simulacion_head_c] == marca_s:
                self.simulacion_head_f += 1
                self.simulacionEstado[self.simulacion_head_f][self.simulacion_head_c] = inicio + marca_s
                self.actualizar_cola_simulada()

            elif self.ruta[self.simulacion_head_f - 1][self.simulacion_head_c] == marca_s:
                self.simulacion_head_f -= 1
                self.simulacionEstado[self.simulacion_head_f][self.simulacion_head_c] = inicio + marca_s
                self.actualizar_cola_simulada()

        """
        self.imprimir_ruta()
        self.imprimir_estado()
        self.imprimir_simulacion()
        """

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
                    fila, columna = self.busquedaLineal()
                    if fila != -1:
                        self.celdaObj = (fila, columna)
                        self.generarRuta(fila, columna)
                        self.objetivo = False
                        marca = 1
                    else:
                        print('movimiento adicional')
                        self.movAdicional()
                        marca = 1

    def checkarCambio(self):

        if self.objetivo:
            estado()
            imagen = cv2.imread("frames\prueba.bmp")

            #matriz_colores = cv2.resize(imagen, None, fx=0.031, fy=0.0315)
            #self.ultimoEstado = matriz_colores[:, :, 0]

            self.ultimoEstado = imagen[:,:,0]
            self.actualizar_cola()
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
        print('\n--------------------------------------')
        print('\nultimo Estado\n')
        print('--------------------------------------------\n')
        for fila in range(1, 16):
            print('\n')
            for columna in range(1, 18):
                coor_f = 25 + (16 + (32 * (fila - 1)))
                coor_c = 28 + (16 + (32 * (columna - 1)))
                print(self.ultimoEstado[coor_f][coor_c], end= "\t")

    def imprimir_simulacion(self):
        print('\n--------------------------------------')
        print('\nSimulacion Estado\n')
        print('--------------------------------------------\n')
        for fila in range(1, 16):
            print('\n')
            for columna in range(1, 18):
                print(int(self.simulacionEstado[fila][columna]), end= "\t")

    def imprimir_ruta(self):
        print('\n--------------------------------------')
        print('\nRuta\n')
        print('--------------------------------------------\n')
        for fila in range(1, 16):
            print('\n')
            for columna in range(1, 18):
                print(int(self.ruta[fila][columna]), end="\t")

    def actualizar_cola(self):
        coor_f = 25 + (16 + (32 * (self.tail_f - 1)))
        coor_c = 28 + (16 + (32 * (self.tail_c - 1)))
        temp_f = self.tail_f
        temp_c = self.tail_c

        self.valor_cola = self.ultimoEstado[coor_f][coor_c]

        if self.valor_cola < 100:
            self.valor_cola = 255
        if 100 < self.ultimoEstado[coor_f][coor_c] < self.valor_cola:
            self.valor_cola = self.ultimoEstado[coor_f][coor_c]

        if 100 < self.ultimoEstado[coor_f - 32][coor_c] < self.valor_cola:
            self.tail_f = temp_f - 1
            self.valor_cola = self.ultimoEstado[coor_f - 32][coor_c]

        if 100 < self.ultimoEstado[coor_f + 32][coor_c] < self.valor_cola:
            self.tail_f = temp_f + 1
            self.valor_cola = self.ultimoEstado[coor_f + 32][coor_c]

        if 100 < self.ultimoEstado[coor_f][coor_c + 32] < self.valor_cola:
            self.tail_c = temp_c + 1
            self.valor_cola = self.ultimoEstado[coor_f][coor_c + 32]

        if 100 < self.ultimoEstado[coor_f][coor_c - 32] < self.valor_cola:
            self.tail_c = temp_c - 1
            self.valor_cola = self.ultimoEstado[coor_f][coor_c - 32]



    def actualizar_cola_simulada(self):
        minimo = 500
        minimo_loc = None
        valor = self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c]
        self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c] = 73


        if (self.simulacionEstado[self.simulacion_tail_f - 1][self.simulacion_tail_c] > valor) and \
                self.simulacionEstado[self.simulacion_tail_f - 1][self.simulacion_tail_c]\
                < minimo:
            minimo = self.simulacionEstado[self.simulacion_tail_f - 1][self.simulacion_tail_c]
            minimo_loc = (self.simulacion_tail_f - 1,self.simulacion_tail_c)
        if (self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c - 1] > valor)\
                and self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c - 1]\
                < minimo:
            minimo = self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c - 1]
            minimo_loc = (self.simulacion_tail_f,self.simulacion_tail_c - 1)
        if (self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c + 1] > valor) and\
                self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c + 1]\
                < minimo:
            minimo = self.simulacionEstado[self.simulacion_tail_f][self.simulacion_tail_c + 1]
            minimo_loc = (self.simulacion_tail_f, self.simulacion_tail_c + 1)
        if (self.simulacionEstado[self.simulacion_tail_f + 1][self.simulacion_tail_c] > valor) and\
                self.simulacionEstado[self.simulacion_tail_f + 1][self.simulacion_tail_c]\
                < minimo:
            minimo = self.simulacionEstado[self.simulacion_tail_f + 1][self.simulacion_tail_c]
            minimo_loc = (self.simulacion_tail_f + 1,self.simulacion_tail_c)
        if minimo_loc != None:
            self.simulacion_tail_f = minimo_loc[0]
            self.simulacion_tail_c = minimo_loc[1]

    def borrarRuta(self):
        fil = self.head_f
        col = self.head_c
        marca = 1

        while True:
            if self.ruta[fil + 1][col] == marca:
                fil += 1
                self.ruta[fil][col] = 0
                marca += 1
            elif self.ruta[fil - 1][col] == marca:
                fil -= 1
                self.ruta[fil][col] = 0
                marca += 1
            elif self.ruta[fil][col - 1] == marca:
                col -= 1
                self.ruta[fil][col] = 0
                marca += 1
            elif self.ruta[fil][col + 1] == marca:
                col += 1
                self.ruta[fil][col] = 0
                marca += 1
            else:
                break

    def verificacion2(self):
        costo = self.ruta[self.celdaObj[0]][self.celdaObj[1]]
        tam = 1
        tf = self.tail_f
        tc = self.tail_c
        f = self.trans_f(tf)
        c = self.trans_c(tc)
        u = 32
        ref = self.valor_cola
        minimo = 500
        minimo_loc = None
        while True:

            if self.ultimoEstado[f - u][c] > ref and self.ultimoEstado[f-u][c] < minimo:
                minimo = self.ultimoEstado[f-u][c]
                minimo_loc = (f - u,c)
            if self.ultimoEstado[f + u][c] > ref and self.ultimoEstado[f + u][c] < minimo:
                minimo = self.ultimoEstado[f + u][c]
                minimo_loc = (f + u, c)
            if self.ultimoEstado[f][c-u] > ref and self.ultimoEstado[f][c-u] < minimo:
                minimo = self.ultimoEstado[f][c-u]
                minimo_loc = (f, c - u)
            if self.ultimoEstado[f][c+u] > ref and self.ultimoEstado[f][c+u] < minimo:
                minimo = self.ultimoEstado[f][c+u]
                minimo_loc = (f, c + u)
            if minimo_loc != None:
                tam += 1
                f = minimo_loc[0]
                c = minimo_loc[1]
                ref = minimo
                minimo = 500
                minimo_loc = None
            else:
                break
        if tam < costo:
            return True
        else:
            return False




    def trans_f(self, fila):
        coor_f = 25 + (16 + (32 * (fila - 1)))
        return coor_f
    def trans_c(self,columna):
        coor_c = 28 + (16 + (32 * (columna - 1)))
        return coor_c
    def trans_u(self):
        return 32

    def copiaEstado(self):
        for fila in range(1,16):
            for columna in range(1,18):
                f = self.trans_f(fila)
                c = self.trans_c(columna)
                self.simulacionEstado[fila][columna] = self.ultimoEstado[f][c]





    def tamanoSimulacion(self,camino_longitud):
        tam = 1
        f = self.trans_f(self.simulacion_tail_f)
        c = self.trans_c(self.simulacion_tail_c)
        u = 32
        ref = self.simulacionEstado[f][c]
        minimo = 500
        minimo_loc = None
        while True:

            if tam > camino_longitud:
                return tam


            if self.simulacionEstado[f - u][c] > ref and self.simulacionEstado[f-u][c] < minimo:
                minimo = self.simulacionEstado[f-u][c]
                minimo_loc = (f - u,c)
            if self.simulacionEstado[f + u][c] > ref and self.simulacionEstado[f - u][c] < minimo:
                minimo = self.simulacionEstado[f - u][c]
                minimo_loc = (f + u, c)
            if self.simulacionEstado[f][c-u] > ref and self.simulacionEstado[f][c-u] < minimo:
                minimo = self.simulacionEstado[f][c-u]
                minimo_loc = (f, c - u)
            if self.simulacionEstado[f][c-u] > ref and self.simulacionEstado[f][c-u] < minimo:
                minimo = self.simulacionEstado[f][c-u]
                minimo_loc = (f, c + u)
            if minimo_loc != None:
                tam += 1
                f = minimo_loc[0]
                c = minimo_loc[1]
                ref = minimo
                minimo = 500
                minimo_loc = None
            else:
                return tam









