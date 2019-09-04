import arcade
import threading
import time
import math
import ast
import networkx as nx

grafo = {}
sem = []
t = []
rect = []
my_pos = None
dg = nx.DiGraph()

def p(id, t):
    global rect
    sem[int(id) - 1].wait()
    print('P' + str(id) + ' corriendo')
    rect[id - 1].color = arcade.color.GREEN
    time.sleep(t)
    rect[id - 1].color = arcade.color.RED
    print('P' + str(id) + ' terminado')
    for i in grafo[str(id)][1]:
        sem[int(i) - 1].wait()



def get_params():
    global grafo
    with open('parametros.txt', 'r') as f:
        s = f.read()
        grafo = ast.literal_eval(s)


def gen_sem():
    global grafo
    for i in grafo:
        sem.append(threading.Barrier(len(grafo[i][0]) + 1))
        t.append(grafo[i][2])


class Rectangle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = arcade.color.GRAY


def on_draw(a):
    global COLOR
    arcade.start_render()

    arcade.draw_texture_rectangle(800 // 2, 800 // 2, 800, 800, arcade.load_texture("cpu.png"))
    arcade.draw_text("Asignacion 1 - Semaforos", 400, 750, arcade.color.WHITE, font_size=30, anchor_x="center")

    for k in grafo:
        for i in grafo[k][1]:
            xr, yr = radio( rect[int(k) - 1].x,
                            rect[int(k) - 1].y,
                            rect[int(i) - 1].x,
                            rect[int(i) - 1].y)

            xa, ya, xb, yb = arrow(rect[int(k) - 1].x,
                                   rect[int(k) - 1].y,
                                   xr, yr)

            arcade.draw_triangle_filled(xa, ya, xb, yb, xr, yr,
                                        arcade.color.BLACK)

            arcade.draw_line(rect[int(k) - 1].x,
                             rect[int(k) - 1].y,
                             xr, yr,
                             color=arcade.color.BLACK,
                             line_width=4)

            """arcade.draw_triangle_filled(rectangulos[int(k) - 1].x + 10,
                            rectangulos[int(k) - 1].y + 10,
                            rectangulos[int(k) - 1].x - 10,
                            rectangulos[int(k) - 1].y - 10,
                            rectangulos[int(i) - 1].x,
                            rectangulos[int(i) - 1].y,
                            arcade.color.BLACK)"""
    for i in rect:
        arcade.draw_circle_filled(i.x, i.y, i.size, i.color)
    for i in range(len(sem)):
        arcade.draw_text(grafo[str(i+1)][3], rect[i].x, rect[i].y - 15, arcade.color.BLACK, font_size=30, anchor_x="center")

def radio(xa, ya, xb, yb):
    t = 0.89
    x = xa + t * (xb - xa)
    y = ya + t * (yb - ya)
    return x, y

def arrow(x1, y1, x2, y2):
    dx, dy = x1 - x2, y1 - y2
    norm = math.sqrt(dx * dx + dy * dy)
    udx, udy = dx / norm, dy / norm
    ax = udx * math.sqrt(3) / 2 - udy * 1 / 2
    ay = udx * 1 / 2 + udy * math.sqrt(3) / 2
    bx = udx * math.sqrt(3) / 2 + udy * 1 / 2
    by = - udx * 1 / 2 + udy * math.sqrt(3) / 2
    return x2 + 20 * ax, y2 + 20 * ay, x2 + 20 * bx, y2 + 20 * by

def dirGraph():
    global grafo
    global dg, my_pos
    for k in grafo:
        dg.add_node(k)
        for s in grafo[k][1]:
            dg.add_edge(k, s)
    my_pos = nx.spring_layout(dg, seed=200)
    print(my_pos)

def main():
    cont = 0
    j = 0
    get_params()
    gen_sem()
    dirGraph()
    processes = []
    for i in range(len(sem)):
        processes.append(lambda: p(i+1, t[i]))
        rect.append(Rectangle(float(my_pos[str(i + 1)][0] * 200 + 400), float(my_pos[str(i + 1)][1] * 200 + 400), 25))
        if i == 7:
            cont = 0
            j += 80
        else:
            cont += 1
        threading.Thread(target=processes[i]).start()

    arcade.open_window(800, 800, 'semaforos')
    arcade.set_background_color(arcade.color.AMAZON)

    arcade.schedule(on_draw, 1 / 80)

    arcade.run()


if __name__ == "__main__":
    main()
