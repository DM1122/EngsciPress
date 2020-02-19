import tkinter
from tkinter import filedialog, simpledialog

import sys
sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib
from Forest import forest



class GUI:
    def __init__(self, corpus):
        self.master = tkinter.Tk()
        self.corpus = corpus

        self.master.title('Dictionary Applet')
        self.master.iconbitmap('ui/book_icon.ico')
        
        self.intro_label = tkinter.Label(self.master, anchor='w', text='Welcome! Get started by importing a JSON dictionary or creating your own')
        self.intro_label.grid(row=0, column=0)

        #region Frames
        self.browser_frame = tkinter.Frame(self.master)
        self.ops_frame = tkinter.Frame(self.master)
        self.lookup_frame = tkinter.Frame(self.master)
        self.console_frame = tkinter.Frame(self.master)

        self.browser_frame.grid(row=1, column=0)
        self.ops_frame.grid(row=1, column=1)
        self.lookup_frame.grid(row=1, column=2)
        self.console_frame.grid(row=2, column=0)

        self.frames = (self.browser_frame, self.ops_frame, self.lookup_frame, self.console_frame)           # EXPERIMENTAL
        #endregion


        #region Browser Frame
        self.search_entry = tkinter.Entry(self.browser_frame, width=20)

        self.search_button = tkinter.Button(self.browser_frame, width=16, text='Search', command=self.search)

        self.dictionary_listbox = tkinter.Listbox(self.browser_frame, height=10, width=20, selectmode=tkinter.SINGLE)
        self.dictionary_listbox.bind('<<ListboxSelect>>', self.printDefiniton)
        #endregion

        #region Ops Frame
        self.load_button = tkinter.Button(self.ops_frame, text='Import', command=self.load)
        
        self.delete_button = tkinter.Button(self.ops_frame, text='Delete', command=self.delete)

        self.add_button = tkinter.Button(self.ops_frame, text='Add', command=self.add)

        self.clear_button = tkinter.Button(self.ops_frame, text='Clear', command=self.clear)
        #endregion

        #region Lookup Frame        
        self.definition_label = tkinter.Label(self.lookup_frame, anchor='w', text='Definition:')
        self.definition_text = tkinter.Text(self.lookup_frame, height=15, width=20, wrap='word')
        #endregion

        #region Console Frame
        self.log_label = tkinter.Label(self.console_frame, anchor='w', text='Console:')
        self.log = tkinter.Text(self.console_frame, height=2, width=50)
        #endregion

        for frame in self.frames:
            for widget in frame.children:
                frame.children[widget].pack()


    def load(self):
        filepath = tkinter.filedialog.askopenfilename(title='Select a dictionary file to import', filetypes=(('JSON Files', '*.json'),))
        self.printlog('Importing "{}"'.format(filepath))
        self.corpus.fromJSON(filepath)

        self.refresh()


    def search(self):
        query = self.search_entry.get()

        if query:
            self.printlog('Searching for "{}" in dictionary'.format(query))
            
            result = self.corpus.search(query)
            if result:
                index = self.dictionary_listbox.get(0, 'end').index(query)
                self.dictionary_listbox.SelectedIndex = index  
            else:
                tkinter.messagebox.showwarning(title='Warning', message='"{}" was not found in dictionary!'.format(query))

    
    def printlog(self, text):
        self.log.insert(tkinter.INSERT, text+'\n')
        self.log.see('end')


    def refresh(self):
        self.dictionary_listbox.delete(0, tkinter.END)

        nodes = self.corpus.traverse(mode='in')
        for node in nodes:
            self.dictionary_listbox.insert(tkinter.END, node.data[0])


    def delete(self):
        idx = self.dictionary_listbox.curselection()
        key = self.dictionary_listbox.get(idx)
        self.printlog('Deleting "{}" from dictionary'.format(key))

        # self.corpus.delete(key)


    def add(self):
        key = tkinter.simpledialog.askstring(title='Add word', prompt='Please enter new key word')
        if not key: return
        val = tkinter.simpledialog.askstring(title='Add word', prompt='Please enter key definition')
        if not val: return

        self.printlog('Adding "{}" to dictionary'.format(key))

        data = (key, val)

        self.corpus.insert(data)
        self.refresh()


    def printDefiniton(self, event):
        self.definition_text.delete(index1='1.0', index2='end')

        index = int(event.widget.curselection()[0])
        value = event.widget.get(index)

        definition = self.corpus.search(value).data[1]
        self.definition_text.insert(index='1.0', chars=definition)


    def clear(self):
        result = tkinter.messagebox.askokcancel(title='Clear Dictionary', message='WARNING: You are about to delete the dictionary')

        if result == True:
            # delete corpus
            tkinter.messagebox.showinfo(title='Clear Dictionary', message='Dictionary cleared')





if __name__ == '__main__':
    pass