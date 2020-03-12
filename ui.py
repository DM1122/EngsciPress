import tkinter
from tkinter import filedialog, simpledialog, ttk

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

        #region Tabs
        self.tabControl = tkinter.ttk.Notebook(self.master)

        self.corpus_tab = tkinter.ttk.Frame(self.tabControl)
        self.tabControl.add(self.corpus_tab, text='Corpus')

        self.ngram_tab = tkinter.ttk.Frame(self.tabControl)
        self.tabControl.add(self.ngram_tab, text='Ngram')

        self.tabControl.pack(expan=1, fill='both')
         #endregion


        #region Corpus Frames
        self.header_frame = tkinter.Frame(self.corpus_tab)
        self.browser_frame = tkinter.Frame(self.corpus_tab)
        self.ops_frame = tkinter.Frame(self.corpus_tab)
        self.lookup_frame = tkinter.Frame(self.corpus_tab)
        self.console_frame = tkinter.Frame(self.corpus_tab)
        self.footer_frame = tkinter.Frame(self.corpus_tab)

        self.header_frame.grid(row=0, column=0, columnspan=3)
        self.browser_frame.grid(row=1, column=0)
        self.ops_frame.grid(row=1, column=1)
        self.lookup_frame.grid(row=1, column=2)
        self.console_frame.grid(row=2, column=0, columnspan=3)
        self.header_frame.grid(row=3, column=0, columnspan=3)
        #endregion

        #region Ngram Frames
        self.header_frame_ngram = tkinter.Frame(self.ngram_tab)
        self.config_frame_ngram = tkinter.Frame(self.ngram_tab)
        self.generate_frame_ngram = tkinter.Frame(self.ngram_tab)
        self.footer_frame_ngram = tkinter.Frame(self.ngram_tab)

        self.header_frame_ngram.grid(row=0, column=0)
        self.config_frame_ngram.grid(row=1, column=0)
        self.generate_frame_ngram.grid(row=2, column=0)
        self.footer_frame_ngram.grid(row=3, column=0)
        #endregion


        #region Header Frame
        self.header_label = tkinter.Label(self.header_frame, text='Welcome! Get started by importing a JSON dictionary or creating your own')

        self.header_label.pack(side='left')
        #endregion


        #region Browser Frame
        self.search_entry = tkinter.Entry(self.browser_frame, width=10)
        self.search_button = tkinter.Button(self.browser_frame, width=5, text='Search', command=self.search)
        self.dictionary_listbox = tkinter.Listbox(self.browser_frame, height=10, width=20, selectmode=tkinter.SINGLE)
        self.dictionary_listbox.bind('<<ListboxSelect>>', self.printDefiniton)

        self.search_entry.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)
        self.dictionary_listbox.grid(row=1, column=0, columnspan=2)
        #endregion

        #region Ops Frame
        self.load_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Import', command=self.load)
        self.delete_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Delete', command=self.delete)
        self.add_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Add', command=self.add)
        self.clear_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Clear', command=self.clear)
        self.stats_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Stats', command=self.showStats)
        self.export_button = tkinter.Button(self.ops_frame, width=5, height=1, text='Export', command=self.export)

        self.load_button.pack()
        self.delete_button.pack()
        self.add_button.pack()
        self.clear_button.pack()
        self.stats_button.pack()
        self.export_button.pack()
        #endregion

        #region Lookup Frame        
        self.definition_label = tkinter.Label(self.lookup_frame, anchor='w', text='Definition:')
        self.definition_text = tkinter.Text(self.lookup_frame, height=15, width=20, wrap='word')

        self.definition_label.pack(side='left')
        self.definition_text.pack()
        #endregion

        #region Console Frame
        self.log_label = tkinter.Label(self.console_frame, anchor='w', text='Console:')
        self.log = tkinter.Text(self.console_frame, height=2, width=50)

        self.log_label.pack(side='left')
        self.log.pack()
        #endregion


        #region Footer Frame
        self.footer_label = tkinter.Label(self.footer_frame, text='David Maranto | 2020')

        self.footer_label.pack(side='right')
        #endregion


        #region Header Frame Ngram
        self.header_label_ngram = tkinter.Label(self.header_frame_ngram, text='Ngram viewer')

        self.header_label_ngram.pack(side='left')
        #endregion

        #region Footer Frame Ngram
        
        #endregion



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


    def showStats(self):
        size = 'Corpus Size: {}'.format(self.corpus.getSize())
        stats_str = size

        tkinter.messagebox.showinfo(title='Statistics', message=stats_str)

    def export(self):
        dirpath = tkinter.filedialog.askdirectory(title='Export')
        self.corpus.toTXT(dirpath)
        tkinter.messagebox.showinfo(title='Export', message='Corpus has been exported!')


if __name__ == '__main__':
    pass