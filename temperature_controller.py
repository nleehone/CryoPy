import visa
from drivers.LS350 import *
import tkinter as tk


class TemperatureControllerApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        rm = visa.ResourceManager('instruments.yaml@sim')
        self.driver = LS350(rm.open_resource('ASRL1::INSTR'))
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.tempA = tk.StringVar()
        self.tempALabel = tk.Label(self, font=('Helvetica', 24))
        self.tempALabel.pack(side='top')
        self.tempALabel['textvariable'] = self.tempA
        self.quit = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
        self.quit.pack(side='bottom')
        self.onUpdate()

    def onUpdate(self):
        self.after(1000, self.onUpdate)
        self.tempA.set(self.driver.get_temperature('A'))


if __name__ == '__main__':
    root = tk.Tk()
    app = TemperatureControllerApplication(master=root)
    root.mainloop()
