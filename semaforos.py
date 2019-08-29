import arcade
import threading
import time
import ast


grafo = {}
sem = []
t = []
rectangulos = []


def p(id, t):
    global rectangulos
    sem[int(id) - 1].wait()
    print('P' + str(id) + ' corriendo')
    rectangulos[id - 1].color = arcade.color.GREEN
    time.sleep(t)
    rectangulos[id - 1].color = arcade.color.RED
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

    for i in rectangulos:
        arcade.draw_rectangle_filled(i.x, i.y, i.size, i.size, i.color)
    for i in range(len(sem)):
        arcade.draw_text("P" + str(i + 1), rectangulos[i].x, rectangulos[i].y - 15, arcade.color.BLACK, font_size=30, anchor_x="center")


def main():
    get_params()
    gen_sem()
    processes = []
    for i in range(len(sem)):
        processes.append(lambda: p(i+1, t[i]))
        rectangulos.append(Rectangle(50 + i * 100, 550, 60))
        threading.Thread(target=processes[i]).start()

    arcade.open_window(800, 600, 'semaforos')
    arcade.set_background_color(arcade.color.WHITE)

    arcade.schedule(on_draw, 1 / 80)

    arcade.run()


if __name__ == "__main__":
    main()
