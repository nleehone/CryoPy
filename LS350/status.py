import tkinter as tk
import subprocess


class StatusWindow(tk.Frame):
    subprocesses = {}

    def create_part(self, row, title, process):
        label = tk.Label(self, text=title)
        label.grid(row=row, column=0)

        label = tk.Label(self, text='    ', bg='red')
        label.grid(row=row, column=1, padx=10)
        self.status[row] = label

        def spawn_proc():
            self.subprocesses[row] = subprocess.Popen(['python3', process])

        button = tk.Button(self, text='Start', command=spawn_proc)
        button.grid(row=row, column=2)

        button = tk.Button(self, text='Stop', command=lambda: self.subprocesses[row].terminate())
        button.grid(row=row, column=3)

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.status = {}

        self.create_part(0, 'Driver', 'driver.py')
        self.create_part(1, 'Acquirer', 'acquirer.py')
        self.create_part(2, 'Data Store', 'data_store.py')
        self.create_part(3, 'Recorder', 'recorder.py')
        self.create_part(4, 'Controller', 'controller.py')
        self.create_part(5, 'Front End', 'frontend.py')
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
