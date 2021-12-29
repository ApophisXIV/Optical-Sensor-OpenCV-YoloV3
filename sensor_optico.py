import os
from drivers.deteccion_objeto import detector_objetos as d_o
from drivers.deteccion_color import detectar_color as d_c

class sensor_optico:

	def __init__(self, carpeta_imagenes_lote):
		self._carpeta_imagenes_lote = carpeta_imagenes_lote

	def __generar_reporte(self, nombre_reporte, dict_objeto):
		#Guardar reporte en la carpeta sensor_optico/out
		with open(os.path.join('out', nombre_reporte), 'w') as f:
			for key, value in dict_objeto.items():
				f.write('%s: %s\n' % (key, value))

	def sensor_leer(self, mostrar_imagen=False, duracion=250):

		detect_o = d_o("coco.names", "yolov3.weights", "yolov3.cfg")
		detect_c = d_c(carpeta_imagenes=self._carpeta_imagenes_lote)

		botellas = {}
		vasos = {}

		for i in range(0, detect_c.n_imagenes):

			color = detect_c.detectar_color(detect_c.imagenes_hsv[i])

			objeto = detect_o.detectar_objeto(detect_c.imagenes[i])

			if mostrar_imagen:
				titulo_img = objeto + ' de color ' + color
				detect_c.mostrar_imagen(detect_c.imagenes[i], titulo_img, duracion)

			try:
				if(objeto == 'bottle'):
					botellas[color] = botellas.get(color, 0) + 1

				elif(objeto == 'cup'):
					vasos[color] = vasos.get(color, 0) + 1

				else:
					raise  objeto
			except:
				print("Error (Se detiene la cinta transportadora hasta que se elimine la obstruccion): ", objeto)

		self.__generar_reporte('botellas.txt', botellas)
		self.__generar_reporte('vasos.txt', vasos)

# Ejemplo de uso:
if __name__ == '__main__':
	sensor = sensor_optico("./Lote0001")
	sensor.sensor_leer(mostrar_imagen=True, duracion= 150)
