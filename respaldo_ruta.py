def generarRuta(self, filaObj=0, columnaObj=0):
    if self.inicio == False:
        self.ruta[self.head_f][self.head_c] = -1
        self.ruta[self.head_f][self.head_c + 1:15] = list(range(1, 11))
        self.inicio = True
    else:
        incrementoF = incrementoC = 1

        if self.head_f > filaObj:
            incrementoF = -1
        elif self.head_f < filaObj:
            incrementoF = 1

        if self.head_c > columnaObj:
            incrementoC = -1
        elif self.head_c < columnaObj:
            incrementoC = 1

        if self.accionPasada == 'ARROW_LEFT' or self.accionPasada == 'ARROW_RIGHT':
            contador = 0
            for i in range(self.head_f + incrementoF, filaObj + incrementoF, incrementoF):
                self.ruta[i][self.head_c] = contador = abs(self.head_f - i)
            for i in range(self.head_c + incrementoC, columnaObj + incrementoC, incrementoC):
                self.ruta[self.head_f + (incrementoF * contador)][i] = contador + abs(self.head_c - i)


        elif self.accionPasada == 'ARROW_UP' or self.accionPasada == 'ARROW_DOWN':

            contador = 0
            for i in range(self.head_c + incrementoC, filaObj + incrementoC, incrementoC):
                self.ruta[self.head_f][i] = contador = abs(self.head_c - i)
            for i in range(self.head_f + incrementoF, columnaObj + incrementoF, incrementoF):
                self.ruta[i][self.head_c + (incrementoC * contador)] = contador + abs(self.head_f - i)
        print('------------------------------------------------')
        print(self.ruta)

