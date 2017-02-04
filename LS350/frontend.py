import time
import zmq
from threading import Thread
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
matplotlib.use('Gtk')
from collections import deque

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class WindowHandler(object):
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
    def onButtonPressed(self, button):
        print("Hello")


builder = Gtk.Builder()
builder.add_from_file('test.glade')
builder.connect_signals(WindowHandler())

l = builder.get_object('channel_A_container')
fig = matplotlib.figure.Figure()
ax = fig.add_subplot(111)
ax.plot([1,2,3],[1,4,9])

canvas = FigureCanvas(fig)
l.pack_start(canvas, True, True, 0)

# below is optional if you want the navigation toolbar
navToolbar = NavigationToolbar(canvas, l)
navToolbar.lastDir = '/var/tmp/'
l.pack_start(navToolbar, False, True, 0)
navToolbar.show()

l = builder.get_object('channel_B_container')
fig = matplotlib.figure.Figure()
ax = fig.add_subplot(111)
ax.plot([1,2,3],[1,4,9])

canvas = FigureCanvas(fig)
l.pack_start(canvas, True, True, 0)

# below is optional if you want the navigation toolbar
navToolbar = NavigationToolbar(canvas, l)
navToolbar.lastDir = '/var/tmp/'
l.pack_start(navToolbar, False, False, 0)
navToolbar.show()

win = builder.get_object('window1')
win.show_all()
Gtk.main()



def get(socket, command, params, timeout=1000):
    socket.send_json({'METHOD': 'GET', 'CMD': command, 'PARS': params})
    if timeout > 0:
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        if poller.poll(timeout):
            return socket.recv_json()
        else:
            return "ERROR: Timeout reached"
    else:
        return socket.recv_json()


def set(socket, command, params):
    socket.send_json({'METHOD': 'SET', 'CMD': command, 'PARS': params})
    socket.recv()


class Frontend(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_gui()
        self.pack(expand=1, fill=tk.BOTH)
        self.create_commander()
        self.create_listener()
        self.last_time = time.time()

        self.temperatures_A = deque(maxlen=1000)
        self.temperatures_B = deque(maxlen=1000)

    def create_commander(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect('tcp://localhost:5559')
        self.socket.setsockopt(zmq.LINGER, 0)

        self.identity.set(get(self.socket, 'identify', '', 1000))

    def create_gui(self):
        self.setpoint_A = tk.DoubleVar(self, value=100.0)
        self.setpoint_B = tk.DoubleVar(self, value=100.0)

        self.fig1 = matplotlib.figure.Figure()
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.plot()

        self.fig2 = matplotlib.figure.Figure()
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.plot()

        frame2 = tk.Frame(self)

        frame1 = tk.Frame(self)

        frame = tk.Frame(self)
        tk.Label(self, text='Temperature A').pack(in_=frame, side=tk.LEFT)
        tk.Label(self, text='Temperature ').pack(in_=frame, side=tk.LEFT)
        frame.pack(in_=frame1, side=tk.TOP, fill=tk.X, expand=1)

        frame = tk.Frame(self)
        tk.Label(self, text='Setpoint A').pack(in_=frame, side=tk.LEFT)
        entry = tk.Entry(self, textvariable=self.setpoint_A)
        entry.pack(in_=frame, side=tk.LEFT)
        entry.bind('<Return>', self.set_setpoint_A)
        frame.pack(in_=frame1, side=tk.TOP, fill=tk.X, expand=1)

        frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(self.fig1, master=frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frame.pack(in_=frame1, side=tk.TOP)

        frame1.pack(in_=frame2, side=tk.LEFT)

        frame1 = tk.Frame(self)

        frame = tk.Frame(self)
        tk.Label(self, text='Temperature B').pack(in_=frame, side=tk.LEFT)
        tk.Label(self, text='Temperature ').pack(in_=frame, side=tk.LEFT)
        frame.pack(in_=frame1, side=tk.TOP, fill=tk.X, expand=1)

        frame = tk.Frame(self)
        tk.Label(self, text='Setpoint B').pack(in_=frame, side=tk.LEFT)
        entry = tk.Entry(self, textvariable=self.setpoint_B)
        entry.pack(in_=frame, side=tk.LEFT)
        entry.bind('<Return>', self.set_setpoint_B)
        frame.pack(in_=frame1, side=tk.TOP, fill=tk.X, expand=1)

        frame = tk.Frame(self)
        canvas = FigureCanvasTkAgg(self.fig2, master=frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        frame.pack(in_=frame1, side=tk.TOP)

        frame1.pack(in_=frame2, side=tk.LEFT)

        frame2.pack(side=tk.TOP)

        #frame = tk.Frame(self)
        #self.set_T = tk.DoubleVar(self)
        #entry = tk.Entry(self, textvariable=self.set_T)
        #label = tk.Label(self, text='Setpoint T: ')
        #label.pack(in_=frame, side=tk.LEFT)
        #entry.pack(fill=tk.X)
        #entry.bind('<Return>', self.command)
        #frame.pack(side=tk.TOP)

        frame = tk.Frame(self)
        label = tk.Label(self, text="Identity: ")
        label.pack(in_=frame, side=tk.LEFT)
        self.identity = tk.StringVar()
        label = tk.Label(self, textvariable=self.identity)
        label.pack(in_=frame, side=tk.LEFT)
        frame.pack(side=tk.TOP)

    def set_setpoint_A(self, event):
        setpoint = self.setpoint_A.get()
        set(self.socket, 'temperature_setpoint', {'channel': 'A', 'setpoint': setpoint})

    def set_setpoint_B(self, event):
        setpoint = self.setpoint_B.get()
        set(self.socket, 'temperature_setpoint', {'channel': 'B', 'setpoint': setpoint})

    def command(self, event):
        val = self.set_T.get()
        set(self.socket, 'temperature_setpoint', {'channel': 'A', 'setpoint': val})

    def create_listener(self):
        p = Thread(target=self.zmq_loop)
        p.start()

    def update_plots(self):
        self.ax1.clear()
        self.ax1.plot(range(len(self.temperatures_A)), self.temperatures_A)
        self.fig1.canvas.draw()
        self.ax2.clear()
        self.ax2.plot(range(len(self.temperatures_B)), self.temperatures_B)
        self.fig2.canvas.draw()

    def zmq_loop(self):
        context = zmq.Context()

        socket = context.socket(zmq.SUB)
        socket.connect('tcp://localhost:5556')
        socket.setsockopt_string(zmq.SUBSCRIBE, '')

        while True:
            message = socket.recv_json()
            if message['channel'] == 'A':
                self.temperatures_A.append(message['temperature'])
            elif message['channel'] == 'B':
                self.temperatures_B.append(message['temperature'])
            #self.data_array.append(message['T'])

            # Limit how often we update the graph as this is a slow operation
            if time.time() - self.last_time >= 0.25:
                self.last_time = time.time()
                self.update_plots()


if __name__ == '__main__':
    root = tk.Tk()
    Frontend(root)
    root.mainloop()
