import visa
from drivers.LS350 import *
import tkinter as tk


class TemperatureControllerApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        rm = visa.ResourceManager()
        self.driver = LS350(rm.open_resource('ASRL6::INSTR'))
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.tempA = tk.StringVar()
        self.tempB = tk.StringVar()
        self.tempC = tk.StringVar()
        self.tempD = tk.StringVar()
        self.tempALabel = tk.Label(self, font=('Helvetica', 24))
        self.tempBLabel = tk.Label(self, font=('Helvetica', 24))
        self.tempCLabel = tk.Label(self, font=('Helvetica', 24))
        self.tempDLabel = tk.Label(self, font=('Helvetica', 24))
        self.tempALabel.pack(side='top')
        self.tempBLabel.pack(side='top')
        self.tempCLabel.pack(side='top')
        self.tempDLabel.pack(side='top')
        self.tempALabel['textvariable'] = self.tempA
        self.tempBLabel['textvariable'] = self.tempB
        self.tempCLabel['textvariable'] = self.tempC
        self.tempDLabel['textvariable'] = self.tempD
        self.quit = tk.Button(self, text='QUIT', fg='red', command=root.destroy)
        self.quit.pack(side='bottom')
        self.onUpdate()

    def onUpdate(self):
        self.after(1000, self.onUpdate)
        self.tempA.set(self.driver.get_temperature('A'))
        self.tempB.set(self.driver.get_temperature('B'))
        self.tempC.set(self.driver.get_temperature('C'))
        self.tempD.set(self.driver.get_temperature('D'))


if __name__ == '__main__':
    root = tk.Tk()
    app = TemperatureControllerApplication(master=root)
    root.mainloop()
