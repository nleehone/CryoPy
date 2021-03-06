import time
import zmq
from threading import Thread
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use('TkAgg')


class Frontend(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_gui()
        self.pack()
        self.create_commander()
        self.create_listener()
        self.last_time = time.time()

        self.data_array = []

    def create_commander(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect('tcp://localhost:5556')

    def create_gui(self):
        self.f = matplotlib.figure.Figure()
        self.a = self.f.add_subplot(111)
        self.a.plot([1,2,3],[1,4,9])
        canvas = FigureCanvasTkAgg(self.f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.set_T = tk.DoubleVar()
        entry = tk.Entry(self, textvariable=self.set_T)
        label = tk.Label(self, text='Setpoint T: ')
        label.pack(side=tk.LEFT)
        entry.pack(fill=tk.X)
        entry.bind('<Return>', self.command)

    def command(self, event):
        val = self.set_T.get()
        self.socket.send_json({'Set T': float(val)})
        self.socket.recv()

    def create_listener(self):
        p = Thread(target=self.zmq_loop)
        p.start()

    def update_plot(self):
        self.a.clear()
        self.a.plot(range(len(self.data_array)), self.data_array)
        self.f.canvas.draw()

    def zmq_loop(self):
        context = zmq.Context()

        socket = context.socket(zmq.SUB)
        socket.connect('tcp://localhost:5555')
        socket.setsockopt_string(zmq.SUBSCRIBE, '')

        while True:
            message = socket.recv_json()
            print(message)
            self.data_array.append(message['T'])

            # Limit how often we update the graph as this is a slow operation
            if time.time() - self.last_time >= 1:
                self.last_time = time.time()
                self.update_plot()


if __name__ == '__main__':
    root = tk.Tk()
    Frontend(root)
    root.mainloop()
