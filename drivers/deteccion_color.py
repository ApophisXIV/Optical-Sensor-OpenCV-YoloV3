import cv2
import numpy as np
import os


class detectar_color:

    def __init__(self, carpeta_imagenes):
        self._carpeta_imagenes = carpeta_imagenes
        self.colores = ['azul', 'rojo',  'verde', 'negro', 'amarillo']
        self.imagenes, self.imagenes_hsv, self.n_imagenes = self.__cargar_imagenes()

    def __cargar_imagenes(self):
        imagenes = []
        hsv_lista = []
        for filename in os.listdir(self._carpeta_imagenes):
            img = cv2.imread(os.path.join(self._carpeta_imagenes, filename))
            img = cv2.resize(img, None, fx=0.5, fy=0.5)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            if img is not None and hsv is not None:
                imagenes.append(img)
                hsv_lista.append(hsv)
        return imagenes, hsv_lista, len(imagenes)

    def __filtro_azul(self, hsv):
        '''
        ### Filtro Azul
        (hMin = 100 , sMin = 76, vMin = 62), (hMax = 125 , sMax = 255, vMax = 255)
        '''
        azul_min = np.array([100, 76, 62])
        azul_max = np.array([125, 255, 255])
        mask = cv2.inRange(hsv, azul_min, azul_max)
        return mask

    def __filtro_rojo(self, hsv):
        '''
        ### Filtro Rojo
        (hMin = 3 , sMin = 144, vMin = 126), (hMax = 14 , sMax = 255, vMax = 255)
        '''
        rojo_min = np.array([3, 144, 126])
        rojo_max = np.array([14, 255, 255])
        mask = cv2.inRange(hsv, rojo_min, rojo_max)
        return mask

    def __filtro_verde(self, hsv):
        '''
        ### Filtro Verde
        (hMin = 36 , sMin = 69, vMin = 51), (hMax = 65 , sMax = 215, vMax = 210)
        '''
        verde_min = np.array([36, 69, 51])
        verde_max = np.array([65, 215, 210])
        mask = cv2.inRange(hsv, verde_min, verde_max)
        return mask

    def __filtro_negro(self, hsv):
        '''
        ### Filtro Negro
        (hMin = 0 , sMin = 0, vMin = 0), (hMax = 179 , sMax = 255, vMax = 252)
        '''
        negro_min = np.array([0, 0, 0])
        negro_max = np.array([0, 255, 252])
        mask = cv2.inRange(hsv, negro_min, negro_max)
        return mask

    def __filtro_amarillo(self, hsv):
        '''
        ### Filtro Amarillo
        (hMin = 19 , sMin = 102, vMin = 141), (hMax = 35 , sMax = 255, vMax = 245)
        '''
        amarillo_min = np.array([19, 102, 141])
        amarillo_max = np.array([35, 255, 245])
        mask = cv2.inRange(hsv, amarillo_min, amarillo_max)
        return mask

    def mostrar_imagen(self, img, titulo, delay):
        cv2.imshow(titulo, img)
        cv2.waitKey(delay)
        cv2.destroyAllWindows()

    def detectar_color(self, hsv):

        filtros = [self.__filtro_azul, self.__filtro_rojo,
                   self.__filtro_verde, self.__filtro_negro, self.__filtro_amarillo]

        color_max = 0
        color_indice = 0

        for i in range(0, len(filtros)):
            mask = filtros[i](hsv)
            n_color = cv2.countNonZero(mask)
            if n_color > color_max:
                color_max = n_color
                color_indice = i

        return self.colores[color_indice]
