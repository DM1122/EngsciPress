import sys

import tkinter
from tkinter import filedialog, simpledialog, ttk

sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib
from Forest import forest

import corpus, ngram, gui



class Master(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('NΨ Dictionary Applet')
        self.iconbitmap('assets/book_icon.ico')

        self.corpus = corpus.Corpus()
        self.ngram = None


        #region Tab Controller Setup
        self.tabController = tkinter.ttk.Notebook(self)
        self.corpus_tab = CorpusTab(self.tabController, self); self.tabController.add(self.corpus_tab, text='Corpus')
        self.ngram_tab = NgramTab(self.tabController, self); self.tabController.add(self.ngram_tab, text='Ngram')
        self.tabController.pack()
        #endregion

        self.map = self.updateMap()
        for widget in self.map:
            print(widget)

    
    def updateMap(self):
        map = dict()

        def scan(widget):
            map[str(widget)] = widget

            for subwidget in widget.winfo_children():
                scan(subwidget)

        scan(self)

        return map


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


    def printDefiniton(self, event):
        self.definition_text.delete(index1='1.0', index2='end')

        index = int(event.widget.curselection()[0])
        value = event.widget.get(index)

        definition = self.corpus.search(value).data
        self.definition_text.insert(index='1.0', chars=definition)


class CorpusTab(tkinter.ttk.Frame):

    class BrowserFrame(tkinter.LabelFrame):
        def __init__(self, parent, controller):
            tkinter.LabelFrame.__init__(self, parent, text='Browser')
            self.controller = controller

            self.searchbox = gui.SearchBox(self, label='Search', foo=self.search); self.searchbox.pack(side='top')

            self.listbox = tkinter.Listbox(self, height=10, width=20, selectmode='single'); self.listbox.pack(side='top')
            self.listbox.bind('<<ListboxSelect>>', self.define)


        def refresh(self):
            '''
            Updates listbox with corpus data.
            '''
            self.listbox.delete(0, tkinter.END)

            nodes = self.controller.corpus.traverse(mode='in')
            for node in nodes:
                self.listbox.insert(tkinter.END, node.data[0])


        def getSelection(self):
            idx = self.listbox.curselection()
            key = self.listbox.get(idx)

            return key


        def search(self):
            pass


        def define(self):
            pass




    class OpsFrame(tkinter.LabelFrame):
        def __init__(self, parent, controller):
            tkinter.LabelFrame.__init__(self, parent, text='Ops')
            self.controller = controller

            self.load_button = tkinter.Button(self, text='Load', width=5, height=1, command=self.load); self.load_button.pack(side='top')
            self.add_button = tkinter.Button(self, text='Add', width=5, height=1, command=self.add); self.add_button.pack(side='top')
            self.delete_button = tkinter.Button(self, text='Delete', width=5, height=1, command=self.delete); self.delete_button.pack(side='top')
            self.clear_button = tkinter.Button(self, text='Clear', width=5, height=1, command=self.clear); self.clear_button.pack(side='top')
            self.draw_button = tkinter.Button(self, text='Draw', width=5, height=1, command=self.draw); self.draw_button.pack(side='top')
            self.export_button = tkinter.Button(self, text='Export', width=5, height=1, command=self.export); self.export_button.pack(side='top')
            self.stats_button = tkinter.Button(self, text='Stats', width=5, height=1, command=self.stats); self.stats_button.pack(side='top')
            
        def load(self):
            filepath = tkinter.filedialog.askopenfilename(title='Select a dictionary file to import', filetypes=(('CSV Files', '*.csv'),))
            if not filepath: return
            print('Importing "{}"'.format(filepath))

            self.controller.corpus.fromCSV(filepath)
            self.controller.map['.!notebook.!corpustab.!frame.!browserframe'].refresh()


        def add(self):
            key = tkinter.simpledialog.askstring(title='Add word', prompt='Please enter new word')
            if not key: return
            val = tkinter.simpledialog.askstring(title='Add word', prompt='Please enter definition')
            if not val: return

            self.controller.corpus.insert((key,val))
            self.controller.map['.!notebook.!corpustab.!frame.!browserframe'].refresh()


        def delete(self):
            if self.controller.corpus.getSize() == 0:
                return
            key = self.controller.map['.!notebook.!corpustab.!frame.!browserframe'].getSelection()
            print(key) ####WIP
            self.controller.corpus.delete(key)
            self.controller.map['.!notebook.!corpustab.!frame.!browserframe'].refresh()


        def clear(self):
            if self.controller.corpus.getSize() == 0:
                return
            choice = tkinter.messagebox.askokcancel(title='Clear Dictionary', message='WARNING: You are about to delete the entire dictionary')

            if choice:
                self.controller.corpus = None
                self.controller.corpus = corpus.Corpus()
                self.controller.map['.!notebook.!corpustab.!frame.!browserframe'].refresh()
                tkinter.messagebox.showinfo(title='Clear Dictionary', message='Dictionary cleared')


        def draw(self):
            filepath = tkinter.filedialog.askdirectory(title='Select a directory to save drawing')
            self.controller.corpus.draw(dir=filepath, show=True)


        def export(self):
            filepath = tkinter.filedialog.asksaveasfilename(title='Export')
            self.controller.corpus.toCSV(filepath)
            tkinter.messagebox.showinfo(title='Export', message='Corpus has been exported!')


        def stats(self):
            size = 'Corpus Size: {}'.format(self.controller.corpus.getSize())
            tkinter.messagebox.showinfo(title='Statistics', message=size)






    class LookupFrame(tkinter.LabelFrame):
        def __init__(self, parent, controller):
            tkinter.LabelFrame.__init__(self, parent, text='Lookup')
            self.controller = controller
            
            self.display = gui.Display(self, size=(10,25)); self.display.pack(side='top')
        

    def __init__(self, parent, controller):
        tkinter.ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.header = gui.Margin(self, label='Welcome! Get started by loading a CSV dict or creating your own.', anc='w'); self.header.pack(side='top', fill='both')

        self.content = tkinter.Frame(self); self.content.pack(side='top', fill='both')

        self.browser_frame = self.BrowserFrame(self.content, self.controller); self.browser_frame.pack(side='left')
        self.ops_frame = self.OpsFrame(self.content, self.controller); self.ops_frame.pack(side='left')
        self.lookup_frame = self.LookupFrame(self.content, self.controller); self.lookup_frame.pack(side='left')

        self.footer = gui.Margin(self, label='David Maranto | 2020', anc='e'); self.footer.pack(side='bottom', fill='both')


class NgramTab(tkinter.ttk.Frame):

    class BuildFrame(tkinter.LabelFrame):
        def __init__(self, parent, controller):
            tkinter.LabelFrame.__init__(self, parent, text='Build')
            self.controller = controller

            self.ngram_len_spinbox = gui.LabelSpinbox(self, label='Ngram Length', startend=(0,8)); self.ngram_len_spinbox.pack(side='left')
            self.scrape_count_spinbox = gui.LabelSpinbox(self, label='Scrape Count', startend=(0,1000)); self.scrape_count_spinbox.pack(side='left')
            self.restrict_to_corpus_checkbox = gui.LabelCheckbox(self, label='Only allow words in corpus'); self.restrict_to_corpus_checkbox.pack(side='left')
            self.build_button = tkinter.Button(self, text='Build', command=self.build); self.build_button.pack(side='bottom')
        
        def build():
            '''
            Collects data from build frame and instantiates ngram model.
            '''
            pass


    class GenerateFrame(tkinter.LabelFrame):
        def __init__(self, parent, controller):
            tkinter.LabelFrame.__init__(self, parent, text='Generate')
            self.controller = controller

            self.seed_entry = gui.TextBoxInput(self, 'Seed'); self.seed_entry.pack(side='top')
            self.generate_button = tkinter.Button(self, text='Generate!', command=self.generate); self.generate_button.pack(side='top')
            self.display = gui.Display(self, 'Ouput'); self.display.pack(side='top')
            self.reset_button = tkinter.Button(self, text='Reset', command=self.reset); self.reset_button.pack(side='top')
            self.stats_button = tkinter.Button(self, text='Stats', command=self.stats); self.stats_button.pack(side='top')
        
        def generate():
            pass

        def stats():
            pass

        def reset():
            '''
            Deletes ngram model and reactivates build frame.
            '''
            pass


    def __init__(self, parent, controller):
        tkinter.ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.header = gui.Margin(self, label='Ngram model builder', anc='w'); self.header.pack(side='top', fill='both')

        self.content = tkinter.Frame(self); self.content.pack(side='top', fill='both')

        self.build_frame = self.BuildFrame(self.content, self.controller); self.build_frame.pack(side='top')
        self.generate_frame = self.GenerateFrame(self.content, self.controller); self.generate_frame.pack(side='top')

        self.footer = gui.Margin(self, label='David Maranto | 2020', anc='e'); self.footer.pack(side='bottom', fill='both')
       


if __name__ == '__main__':
    ws = workspacelib.Workspace(paths=['temp', 'temp/drawings'], verbose=0)
    ws.reset()

    print('Running UI...')
    master = Master()
    master.mainloop()