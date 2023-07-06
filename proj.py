from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# Coordenadas de los vértices del rectángulo
vertices = [[(-.5, -.5), (0, -.5), (0, 0), (-.5, 0)],
			[(0, -.5), (.5, -.5), (.5,0), (0,0)],
			[(-.5, 0), (0, 0), (0, .5), (-.5,.5)]]
selected_vertex = None  # Vértice seleccionado
dragging = False  # Indicador de arrastre del vértice

image_indices = [None, None, None]

def load_texture(image_path):
	image = Image.open(image_path)
	image_data = image.tobytes("raw", "RGBX", 0, -1)
	texture_id = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, texture_id)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
	return texture_id

texture_ids = [
	"D:\\Computer-Graphics\\Imagenes\\1.jpeg",
	"D:\\Computer-Graphics\\Imagenes\\1.jpeg",
	"D:\\Computer-Graphics\\Imagenes\\1.jpeg"
]

def draw_color(color, vertices):
	glColor3f(color[0], color[1], color[2])
	glBegin(GL_QUADS)
	for vertex in vertices:
		glVertex2f(vertex[0], vertex[1])
	glEnd()

def draw_image(texture_id, vertices):
	glBindTexture(GL_TEXTURE_2D, texture_id)
	glEnable(GL_TEXTURE_2D)
	glBegin(GL_QUADS)

	glTexCoord2f(0.0, 0.0)
	glVertex2f(vertices[0][0], vertices[0][1])

	glTexCoord2f(1.0, 0.0)
	glVertex2f(vertices[1][0], vertices[1][1])

	glTexCoord2f(1.0, 1.0)
	glVertex2f(vertices[2][0], vertices[2][1])

	glTexCoord2f(0.0, 1.0)
	glVertex2f(vertices[3][0], vertices[3][1])
	
	glEnd()
	glDisable(GL_TEXTURE_2D)

def draw_rect():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	draw_color((1.0,0.0,0.0),vertices[0])
	draw_color((0.0,1.0,0.0),vertices[1])
	draw_color((0.0,0.0,1.0),vertices[2])
	glColor3f(1.0, 1.0, 1.0)

	if image_indices[0] is not None:
		# Proyección ortográfica
		glOrtho(-1, 1, -1, 1, -1, 1)
		# Dibuja el cuadrado con la imagen proyectada
		draw_image(texture_id3, vertices[0])
	if image_indices[1] is not None:
		# Proyección ortográfica
		glOrtho(-1, 1, -1, 1, -1, 1)
		# Dibuja el cuadrado con la imagen proyectada
		draw_image(texture_id2, vertices[1])
	if image_indices[2] is not None:
		# Proyección ortográfica
		glOrtho(-1, 1, -1, 1, -1, 1)
		# Dibuja el cuadrado con la imagen proyectada
		draw_image(texture_id, vertices[2])

	glutSwapBuffers()
	glFlush()

def mouse(button, state, x, y):
	global selected_vertex, dragging
	norm_x = (2.0 * x / WIDTH) - 1.0
	norm_y = 1.0 - (2.0 * y / HEIGHT)

	if button == GLUT_LEFT_BUTTON:
		if state == GLUT_DOWN:
			selected_vertex = None
			for i, square_points in enumerate(vertices):
				for j, point in enumerate(square_points):
					if abs(point[0] - norm_x) < 0.05 and abs(point[1] - norm_y) < 0.05:
						selected_vertex = (i, j)
						dragging = True
						break
				if selected_vertex is not None:
					break
		else:
			dragging = False

	glutPostRedisplay()

	if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
		for i, square_points in enumerate(vertices):
			if point_inside_square(square_points, norm_x, norm_y):
				if image_indices[i] is not None:
					# Si ya se muestra una imagen en el cuadrado, remueve la imagen
					image_indices[i] = None
				else:
					# Si no se muestra una imagen, carga y muestra la imagen correspondiente al cuadrado
					image_indices[i] = load_texture(texture_ids[i])
		glutPostRedisplay()

def point_inside_square(vertices, x, y):
	# Verifica si un punto (x, y) está dentro de un cuadrado definido por sus puntos
	min_x = min(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0])
	max_x = max(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0])
	min_y = min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])
	max_y = max(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])

	return min_x <= x <= max_x and min_y <= y <= max_y


def motion(x, y):
	if dragging and selected_vertex is not None:
		norm_x = (2.0 * x / WIDTH) - 1.0
		norm_y = 1.0 - (2.0 * y / HEIGHT)
		vertices[selected_vertex[0]][selected_vertex[1]] = [norm_x, norm_y]
		glutPostRedisplay()


def main():
	#Inicialización de OpenGL
	glutInit()

	global WIDTH, HEIGHT
	WIDTH = glutGet(GLUT_SCREEN_WIDTH)
	HEIGHT = glutGet(GLUT_SCREEN_HEIGHT)

	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(WIDTH, HEIGHT)
	glutCreateWindow("Arrastrar esquinas con OpenGL")

	textures = []
	# Carga la textura
	for path in texture_ids:
		textures.append(load_texture(path))

	global texture_id, texture_id2, texture_id3
	texture_id = textures[0]
	texture_id2 = textures[1]
	texture_id3 = textures[2]

	#Configuración de la función de renderizado
	#Funciones de callback
	glutMouseFunc(mouse)
	glutMotionFunc(motion)
	glutDisplayFunc(draw_rect)

	# Configuración de la proyección ortográfica
	#glutReshapeFunc(reshape)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

	glutMainLoop()

if __name__ == '__main__':
	main()
