import praw
import random

import sys
sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib
from Forest import forest

import ui



class Corpus(forest.BSTree):

    def suggest(self, query):
        '''
        Suggestion is made based on which node is closest to where query might have been found.
        '''
        pass
    
    


if __name__ == '__main__':
    ws = workspacelib.Workspace(paths=['temp', 'temp/drawings'], verbose=0)
    ws.reset()

    
    corpus = Corpus()
    ui = ui.GUI(corpus)

    ui.master.mainloop()
    
    
