import cv2
import numpy as np

class detector_objetos:

	def __init__(self, nombres_objetos, pesos, configuracion):
		self._net, self._output_layers, self._nombres_objetos = self.__cargar_modelo(nombres_objetos, pesos, configuracion)

	def __cargar_modelo(self,nombres, pesos, configuracion):
		red = cv2.dnn.readNet(pesos, configuracion)
		nombres_objetos = []
		with open(nombres, "r") as f:
			nombres_objetos = [linea.strip() for linea in f.readlines()]
		capas_salida = [
			nombre_capa for nombre_capa in red.getUnconnectedOutLayersNames()]
		return red, capas_salida, nombres_objetos


	def __tipo_objeto(self, outputs):
		class_id_max = 0
		for output in outputs:
			for detect in output:
				scores = detect[5:]
				class_id = np.argmax(scores)
				conf = scores[class_id]
				if conf > 0.4:
					class_id_max = class_id
		return class_id_max

	def detectar_objeto(self, img):
		blob = cv2.dnn.blobFromImage(img, scalefactor=0.00394, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
		self._net.setInput(blob)
		outputs = self._net.forward(self._output_layers)
		class_id_max = self.__tipo_objeto(outputs)
		return self._nombres_objetos[class_id_max]