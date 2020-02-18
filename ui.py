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

        self.master.title('Dictionary Applet')
        self.master.iconbitmap('ui/book_icon.ico')
        
        self.intro_label = tkinter.Label(self.master, text='Welcome!')
        self.intro_label.grid(row=0, column=0, sticky=tkinter.W)

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
        self.search_entry = tkinter.Entry(self.browser_frame)

        self.search_button = tkinter.Button(self.browser_frame, text='Search', command=self.search)

        self.dictionary_listbox = tkinter.Listbox(self.browser_frame, selectmode=tkinter.SINGLE)
        #endregion

        #region Ops Frame
        self.load_button = tkinter.Button(self.ops_frame, text='Import', command=self.load)
        
        self.delete_button = tkinter.Button(self.ops_frame, text='Delete', command=self.delete)

        self.add_button = tkinter.Button(self.ops_frame, text='Add', command=self.add)
        #endregion

        #region Lookup Frame        
        self.definition_label = tkinter.Label(self.lookup_frame, text='Definition:')
        self.definition_text = tkinter.Text(self.lookup_frame)
        #endregion

        #region Console Frame
        self.log_label = tkinter.Label(self.console_frame, text='Console:')
        self.log = tkinter.Text(self.console_frame)
        #endregion

        for frame in self.frames:
            for widget in frame.children:
                frame.children[widget].pack()

        #region Layout
        # self.search_entry.grid(row=2, column=1, sticky=tkinter.W)
        # self.search_button.grid(row=2, column=2, sticky=tkinter.W)
        # self.dictionary_listbox.grid(row=3, column=1, sticky=tkinter.W)
        # self.load_button.grid(row=3, column=2)
        # self.log_label.grid(row=5, column=1, sticky=tkinter.W)
        # self.log.grid(row=6, column=1, columnspan=3, sticky=tkinter.W)
        # self.add_button.grid(row=4, column=2)
        # self.delete_button.grid(row=5, column=2)
        # self.definition_label.grid(row=2, column=3)
        # self.definition_text.grid(row=3, column=3, rowspan=1)
        #endregion

    
    def load(self):
        filepath = tkinter.filedialog.askopenfilename(title='Select a dictionary file to import', filetypes=(('JSON Files', '*.json'),))
        self.printlog('Importing "{}"'.format(filepath))
        self.corpus.fromJSON(filepath)

        self.refresh()


    def search(self):
        query = self.search_entry.get()
        self.printlog('Searching for {} in dictionary'.format(query))
        print(self.corpus.search(query))

    
    def printlog(self, text):
        self.log.insert(tkinter.INSERT, text+'\n')


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
        self.printlog('Adding "{}" from dictionary'.format('x'))

        # self.corpus.add(key)





if __name__ == '__main__':
    pass