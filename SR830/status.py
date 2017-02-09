import tkinter as tk
import subprocess
import sys
sys.path.append('../')


class StatusWindow(tk.Frame):
    subprocesses = {}

    def create_part(self, row, title, process):
        label = tk.Label(self, text=title)
        label.grid(row=row, column=0)

        label = tk.Label(self, text='    ', bg='red')
        label.grid(row=row, column=1, padx=10)
        self.status[row] = label

        def spawn_proc(port):
            try:
                self.subprocesses[row] = subprocess.Popen(['python3', process, str(port)])
            except:
                self.subprocesses[row] = subprocess.Popen(['python', process, str(port)])

        button = tk.Button(self, text='Start', command=lambda: spawn_proc(self.port.get()))
        button.grid(row=row, column=2)

        button = tk.Button(self, text='Stop', command=lambda: self.subprocesses[row].terminate())
        button.grid(row=row, column=3)

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.status = {}

        label = tk.Label(self, text='Port:')
        label.grid(row=0, column=0)
        self.port = tk.IntVar()
        entry = tk.Entry(self, textvariable=self.port)
        entry.grid(row=0, column=1, columnspan=2)

        self.create_part(1, 'Driver', 'driver.py')
        self.create_part(2, 'Acquirer', 'acquirer.py')
        #self.create_part(3, 'Data Store', 'data_store.py')
        #self.create_part(4, 'Recorder', 'recorder.py')
        self.create_part(5, 'Controller', 'controller.py')
        #self.create_part(6, 'Front End', 'frontend.py')
        self.check_status()

    def check_status(self):
        for key, proc in self.subprocesses.items():
            if proc.poll() is None:
                self.status[key].configure(background='green')
            else:
                self.status[key].configure(background='red')

        root.after(100, self.check_status)


if __name__ == '__main__':
    root = tk.Tk()
    sw = StatusWindow(root)
    root.mainloop()
