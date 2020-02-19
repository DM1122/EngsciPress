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
    

    def toTXT(self, dirpath):
        '''
        Exports corpus keys to textfile
        '''

        filename = dirpath+'/corpus.txt'

        nodes = self.traverse(mode='in')
        keys = [node.data[0] for node in nodes]

        with open(filename, 'w') as fil:
            for node in nodes:
                fil.write('{}: {}\n'.format(node.data[0], node.data[1]))

    
    


if __name__ == '__main__':
    ws = workspacelib.Workspace(paths=['temp', 'temp/drawings'], verbose=0)
    ws.reset()

    
    corpus = Corpus()
    ui = ui.GUI(corpus)

    ui.master.mainloop()
    
    
