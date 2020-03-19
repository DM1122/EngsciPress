import tkinter



class LabelSpinbox(tkinter.Frame):
    def __init__(self, parent, label='Spinbox', startend=(0,10)):
        tkinter.Frame.__init__(self, parent)

        self.label = tkinter.Label(self, text=label); self.label.pack(side='left')
        self.spin = tkinter.Spinbox(self, from_=startend[0], to=startend[1]); self.spin.pack(side='left')