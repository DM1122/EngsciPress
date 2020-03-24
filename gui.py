import tkinter


class CustomUI(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

    def configure(self, state):
        for child in self.winfo_children():
            child.configure(state=state)


class LabelSpinbox(CustomUI):
    def __init__(self, parent, label='Spinbox', startend=(0,10)):
        CustomUI.__init__(self, parent)

        self.label = tkinter.Label(self, text=label); self.label.pack(side='left')
        self.spin = tkinter.Spinbox(self, from_=startend[0], to=startend[1]); self.spin.pack(side='left')
    
    def get(self):
        return self.spin.get()


class LabelCheckbox(CustomUI):
    def __init__(self, parent, label='Checkbox'):
        CustomUI.__init__(self, parent)
    
        self.bool = tkinter.IntVar()
        self.check = tkinter.Checkbutton(self, text=label, variable=self.bool); self.check.pack(side='left')

    def get(self):
        return self.bool.get()


class TextBoxInput(CustomUI):
    def __init__(self, parent, label):
        CustomUI.__init__(self, parent)
        self.label = tkinter.Label(self, text=label); self.label.pack(side='left')
        self.entry = tkinter.Entry(self, width=10); self.entry.pack(side='left')

    def get(self):
        return self.entry.get()


class SearchBox(CustomUI):
    def __init__(self, parent, label, foo):
        CustomUI.__init__(self, parent)
        self.entry = tkinter.Entry(self, width=10); self.entry.pack(side='left')
        self.button = tkinter.Button(self, text=label, width=5, command=foo); self.button.pack(side='left')

    def get(self):
        return self.entry.get()


class Display(CustomUI):
    def __init__(self, parent, label=None, size=(2,64)):
        CustomUI.__init__(self, parent)
    
        self.label = tkinter.Label(self, text=label); self.label.pack(side='top', anchor='w')
        self.disp = tkinter.Text(self, height=size[0], width=size[1], wrap='word'); self.disp.pack(side='top')

    def write(self, text):
        self.disp.delete('1.0','end')
        self.disp.insert('insert', text)    


class Margin(CustomUI):
    def __init__(self, parent, label=None, anc='w'):
        CustomUI.__init__(self, parent)
        self.label = tkinter.Label(self, text=label); self.label.pack(side='top', anchor=anc)


class ContentFrame(CustomUI):
    def __init__(self, parent, controller):
        CustomUI.__init__(self, parent)