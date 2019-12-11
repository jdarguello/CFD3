import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML, display
from ipywidgets import interact, interactive, interact_manual
import sqlite3 as sql
try:
	from App.Preprocessing.Geometry import *
	from App.Preprocessing.DataBase import DB
except:
	from Geometry import *
	from DataBase import DB

class Element():
	"""
		Desarrolla el dibujo del elemento
	"""
	def esquemaN(self, Es, nodos, color = 'black'):
		self.nodos = nodos
		Es.scatter(nodos[:, [0]], nodos[:, [1]], c=color)
	def esquemaEL(self, Es, puntos, color = 'black', arrow=[True, True]):
		for i in range(1,len(puntos)):
			Es.plot(
				[puntos[i-1][0], puntos[i][0]],
				[puntos[i-1][1], puntos[i][1]],
				color=color
			)
		if arrow[0]:
			#Flujo horizontal
			dx = -(puntos[0][0]-puntos[1][0])/4
			x = puntos[1][0]-dx/2
			y = puntos[1][1] + (puntos[2][1]-puntos[1][1])/2
			dx = -(puntos[0][0]-puntos[1][0])/4
			dy = 0
			head = dx/4
			l = head
			c = "red"
			Es.arrow(x,y,dx,dy, head_width=head, head_length=l, fc=c, ec=c)
		if arrow[1]:
			#Flujo vertical
			x = puntos[0][0] + (puntos[1][0]-puntos[0][0])/2
			dy = -(puntos[0][0]-puntos[1][0])/4
			y = puntos[2][1] - dy/2 
			dx = 0
			head = dy/4
			l = head
			c = "blue"
			Es.arrow(x,y,dx,dy, head_width=head, head_length=l, fc=c, ec=c)
	def save(self, nodos, coord, arrow, *args):
		#Guardar en base de datos
		con, cursor = args[0]
		#Nodos
		Final_nodes = []
		for nodo in nodos:
			datos = con.execute("SELECT * FROM nodes").fetchall()
			exist = False
			for data in datos:
				if data[2] == nodo[0] and data[3] == nodo[1]:
					exist = True
					Final_nodes.append(data[0])
			if not exist:
				if not np.isnan(nodo[2]):
					text = 'INSERT INTO nodes (x,y,T) VALUES ('
					text += str(nodo[0]) + ',' + str(nodo[1]) + ','
					text += str(nodo[2]) + ')'
				else:
					text = 'INSERT INTO nodes (x,y) VALUES ('
					text += str(nodo[0]) + ',' + str(nodo[1]) + ')'
				cursor.execute(text)
				ID = con.execute('SELECT * FROM nodes ORDER BY NodeID DESC LIMIT 1')
				Node = ID.fetchall()
				Final_nodes.append(Node[0][0])
		#Elementos
		text = 'INSERT INTO elements ('
		text2 = ''
		for i in range(len(Final_nodes)):
			text += coord[i] + ', '
			text2 += str(Final_nodes[i]) + ', '
		if not arrow[0]:
			text +=  'u, '
			text2 += "0, "
		if not arrow[1]:
			text += 'v, '
			text2 += "0, "
		text2 = text2[:-2] + ')'
		text = text[:-2] + ') VALUES (' + text2
		cursor.execute(text)
		con.commit()
	def Guardar(self, nodos):
		text = """
				INSERT INTO nodes
				"""
   
class Mono(Element):
	"""
		Elemento cuadrangular "cíclope".

	"""
	def __init__(self, tam, Es, init=[0,0], limit=("S", "W"), arrow=[True,True], **kwargs):
		#Puntos cartesianos del elemento
		points = self.puntos(init,tam, arrow)
		#Nodos
		try:
			Ts = kwargs['Ts']
		except:
			Ts = []
		nodes, coord = self.nodes(init, tam, limit,Ts)
		#Esquema - nodos
		self.esquemaN(Es, nodes)
		#Esquema - Elementos
		self.esquemaEL(Es, points, arrow=arrow)

		#Guardar en base de datos
		self.save(nodes, coord, arrow, kwargs['db'])

	def nodes(self, init, tam, limit, Ti):
		coord = ["p"]
		if limit[0] and limit[1]:
			nodes = np.zeros((3,3))
			if limit[0] == "S":
				coord.append("S")
				nodes[1][0] = init[0]+tam[0]/2
				nodes[1][1] = init[1]
				nodes[1][2] = Ti[1]
			elif limit[0] == "N":
				coord.append("N")
				nodes[1][0] = init[0]+tam[0]/2
				nodes[1][1] = init[1] + tam[1]
				nodes[1][2] = Ti[0]
			if limit[1] == "W":
				coord.append("W")
				nodes[2][0] = init[0]
				nodes[2][1] = init[1]+tam[1]/2
				nodes[2][2] = Ti[1]
			elif limit[1] == "E":
				coord.append("E")
				nodes[2][0] = init[0] + tam[0]
				nodes[2][1] = init[1]+tam[1]/2
				nodes[2][2] = Ti[1]
		elif limit[0] or limit[1]:
			nodes = np.zeros((2,3))
			if limit[0] == "S":
				coord.append("S")
				nodes[1][0] = init[0]+tam[0]/2
				nodes[1][1] = init[1]
				nodes[1][2] = Ti[1]
			elif limit[0] == "N":
				coord.append("N")
				nodes[1][0] = init[0]+tam[0]/2
				nodes[1][1] = init[1] + tam[1]
				nodes[1][2] = Ti[0]
			if limit[1] == "W":
				coord.append("W")
				nodes[1][0] = init[0]
				nodes[1][1] = init[1]+tam[1]/2
				nodes[1][2] = Ti[1]
			elif limit[1] == "E":
				coord.append("E")
				nodes[1][0] = init[0] + tam[0]
				nodes[1][1] = init[1]+tam[1]/2
				nodes[1][2] = Ti[1]
		else:
			nodes = np.zeros((1,3))
		nodes[0][0] = init[0]+tam[0]/2
		nodes[0][1] = init[1]+tam[1]/2
		nodes[0][2] = np.nan
		return nodes, coord

	def puntos(self, init, tam, arrow):
		points = np.zeros((4,2))
		for i in range(len(points)):
			if i == 0:
				points[i][0] = init[0]
				points[i][1] = init[1]
			else:
				abajo = True
				for j in range(2):
					points[i][j] = points[i-1][j]
					if abajo and points[i-1][j] == init[j]:
						points[i][j] = init[j] + tam[j]
						abajo = False
				if abajo:
					points[i][0] = init[0]
		if arrow[0]:
			#flujo horizontal
			x = points[1][0]
			y = points[1][1] + (points[2][1]-points[1][1])/2
		if arrow[1]:
			x = points[0][0] + (points[1][0]-points[0][0])/2
			y = points[2][1] 
		return points



class Malla(DB, Geo):
	"""
		OBJETIVO:
			Desarrolla la malla para simulación numérica y almacena la
			ínformación de los nodos y elementos en una base de datos.

		ARGUMENTOS:
			- dom 	->	Dominio o figura a mallar.
			- Eltype ->	Tipo de elemento.
			- El 	 ->	Dimensiones de los elementos estándar
			- ref	 ->	Refinamiento de curvatura
			- num 	 ->	Vector booleano para numeración de nodos y elementos
	"""
	def __init__(self, El, Ts, ref, num = [False, False],dom=False, local = False):
		#Conexión con base de datos
		super().__init__(local)
		#Dominio General - Frontera
		if dom:
			super(DB, self).__init__(dom)
		#Dibujo de los elementos
		arrows = [True, True]
		coord = [-dom['W']/2,0]
		limit = [False,False]
		for x in range(int(dom['W']/El[0])):
			if x == 0:
				limit[1] = "W"
			elif x == int(dom['W']/El[0])-1:
				limit[1] = "E"
				arrows[0] = False
			else:
				limit[1] = False
			for y in range(int(dom['H']/El[1])):
				#print(coord)
				if y == 0:
					limit[0] = "S"
					arrows[1] = True
				elif y == int(dom['H']/El[1])-1:
					limit[0] = "N"
					arrows[1] = False
				else:
					limit[0] = False
				if limit[0] or limit[1]:
					Mono(El, self.ax, coord, limit, arrows, db=[self.con, self.cursor], Ts=Ts)
				else:
					Mono(El, self.ax, coord, limit, arrows, db=[self.con, self.cursor])
				coord[1] += El[1]
			coord[0] += El[0]
			coord[1] = 0

		#Organizar tablas
		self.organizar()

		#Texto Nodal
		if num[0]:
			self.textN()

		#Texto Elemental
		"""
		if num[1]:
			self.textE()
		"""
		#Gráfica
		plt.show()

	def textN(self):
		datos = self.con.execute("SELECT * FROM nodes ORDER BY ID ASC").fetchall()
		for dato in datos:
			plt.text(dato[2], dato[3], str(dato[1]))

	def textE(self):
		elements = self.data('elements')
		nodos = self.con.execute("SELECT * FROM nodes ORDER BY ID ASC").fetchall()
		for element in elements:
			dominio = [[0,0], [0,0]]	#Mínimos y máximos en x e y.
			for i in range(1,len(element)):
				if i == 1:
					dominio[0][0] = nodos[element[i]-1][2]
					dominio[1][0] = nodos[element[i]-1][3]
				else:
					if nodos[element[i]-1][2] > dominio[0][0]:
						dominio[0][1] = nodos[element[i]-1][2]
					if nodos[element[i]-1][3] > dominio[1][0]:
						dominio[1][1] = nodos[element[i]-1][3]
			plt.text((dominio[0][1]+dominio[0][0])/2,
						(dominio[1][0]+dominio[1][1])/2,
						str(element[0]))

	def organizar(self):
		def guardar(key, j, i):
			self.con.execute('UPDATE elements SET ' + key + '=' + \
				str(nodes[elements[j][3]-1][0]) + ' WHERE ElID=' + str(elements[i][0]))
		def llenado(j, i, vec):
			nodal_info = (nodes[elements[j][3]-1][2], nodes[elements[j][3]-1][3])
			for key in vec:
				if not vec[key]['value']:
					try:
						# ¿x?
						if vec[key]['x'] == '+':
							if nodal_info[0] > p[0] and p[1] == nodal_info[1]:
								guardar(key, j, i)
								vec[key]['value'] = True
						else:
							if nodal_info[0] < p[0] and p[1] == nodal_info[1]:
								guardar(key, j, i)
								vec[key]['value'] = True
					except:
						# y
						if vec[key]['y'] == '+':
							if nodal_info[1] > p[1] and p[0] == nodal_info[0]:
								guardar(key, j, i)
								vec[key]['value'] = True
						else:
							if nodal_info[1] < p[1] and p[0] == nodal_info[0]:
								guardar(key, j, i)
								vec[key]['value'] = True
		datos = self.con.execute("SELECT * FROM nodes ORDER BY x ASC, y DESC").fetchall()
		new_ids = {}
		elements = self.data('elements')
		nodes = self.con.execute("SELECT * FROM nodes").fetchall()
		#Matriz booleana
		M = []
		for i in range(len(elements)):
			vec = []
			for j in range(1,len(elements[i])):
				vec.append(True)
			M.append(vec)
		#Llenar información de elementos
		for i in range(len(elements)):
			p = (nodes[elements[i][3]-1][2], nodes[elements[i][3]-1][3])
			#Planteamiento vector booleano
			vec = {
				'N': {
					'value': False,
					'y': '+'
				},
				'S': {
					'value': False,
					'y': '-'
				}, 
				'E': {
					'value': False,
					'x': '+'
				},
				'W': {
					'value': False,
					'x': '-'
				},
			}
			for item in range(1, len(elements[i])-2):
				if item == 1:
					o = 'N'
				elif item == 2:
					o = 'S'
				elif item == 4:
					o = 'E'
				elif item == 5:
					o = 'W'
				if elements[i][item] is not None and item != 3:
					vec[o]['value'] = True
			#Forward
			for j in range(i, len(elements)):
				if vec['N']['value'] and vec['E']['value']:
					break
				else:
					llenado(j, i, vec)
			#Backward
			for j in range(i, -1, -1):
				if vec['S']['value'] and vec['W']['value']:
					break
				else:
					llenado(j, i, vec)
		#Organización de la información - Renombrar
		elements = self.data('elements')
		vec = ['N', 'S', 'p', 'E', 'W']
		for i in range(len(datos)):
			new_ids[i+1] = datos[i][0]
			self.con.execute('UPDATE nodes SET ID=' + \
				str(i+1) + ' WHERE NodeID=' + str(new_ids[i+1]))
			for j in range(1, len(elements)+1):
				for k in range(1, len(elements[0])):
					if M[j-1][k-1] and elements[j-1][k] == new_ids[i+1]:
						text = 'UPDATE elements SET ' + vec[k-1] + '= '
						text += str(i+1) + ' WHERE ElID='
						text += str(j)
						self.con.execute(text)
						M[j-1][k-1] = False

		#print(self.data('elements'))
		#print(M)
		self.con.commit()			

if __name__ == '__main__':
	data = {
	    'Geometría': {
	        'W': 8,
	        'H': 10,
	    },
	    'Propiedades': {
	        'E': 200E6,
	        'v': 0.3
        }
	}
	Malla((2,2), (5,0), (False, False), [True, True],  data['Geometría'], local=True)