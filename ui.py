import tkinter
from tkinter import filedialog

import sys
sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib
from Forest import forest



class GUI:
    def __init__(self, corpus):
        self.master = tkinter.Tk()
        self.corpus = corpus
    
        #region Widgets
        self.master.title('Dictionary')
        self.master.iconbitmap('ui/book_icon.ico')
        
        self.intro_label = tkinter.Label(self.master, text='Welcome!')
        
        self.search_entry = tkinter.Entry(self.master)
        self.search_button = tkinter.Button(self.master, text='Search', command=self.search)

        self.dictionary_listbox = tkinter.Listbox(self.master)
        
        self.load_button = tkinter.Button(self.master, text='Import', command=self.load)
        
        self.log_label = tkinter.Label(self.master, text='Console:')
        self.log = tkinter.Text(self.master)

        self.delete_button = tkinter.Button(self.master, text='Delete', command=self.delete)
        #endregion
        
        #region Layout
        self.intro_label.grid(row=1, column=1, sticky=tkinter.W)
        self.search_entry.grid(row=2, column=1, sticky=tkinter.W)
        self.search_button.grid(row=2, column=2, sticky=tkinter.W)
        self.dictionary_listbox.grid(row=3, column=1, sticky=tkinter.W)
        self.load_button.grid(row=4, column=2)
        self.log_label.grid(row=5, column=1, sticky=tkinter.W)
        self.log.grid(row=6, column=1)
        #endregion

    
    def load(self):
        filepath = tkinter.filedialog.askopenfilename(title='Select a dictionary file to import', filetypes=(('JSON Files', '*.json'),))
        self.printlog('Importing "{}"'.format(filepath))
        self.corpus.fromJSON(filepath)

        self.refresh()


    def search(self):
        query = self.search_bar.get()
        self.printlog('Searching for '+query)

    
    def printlog(self, text):
        self.log.insert(tkinter.INSERT, text+'\n')


    def refresh(self):
        self.dictionary_listbox.delete(0, tkinter.END)

        nodes = self.corpus.traverse(mode='in')
        for node in nodes:
            self.dictionary_listbox.insert(tkinter.END, node.data[0])

    def delete(self):
        pass





if __name__ == '__main__':
    pass