import praw
import random
import itertools

import sys
sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib
from Forest import forest

import ui



class Corpus(forest.BSTree):

    def suggest(self, query):
        '''
        Suggestion is made based on which node is closest to where query might have been found.
        Returns all predecessors and successsors
        '''
        
        curr = self.root

        # find closest match
        while True:
            if query < curr.data[0] and curr.left != None:
                curr = curr.left
            elif query > curr.data[0] and curr.right != None:
                curr = curr.right
            else:
                origin = curr
                break
        
        # get all predecessors and successors
        precs = []
        curr = origin
        while self.prec(curr):
            curr = self.prec(curr)
            precs.append(curr)

        succs = []
        curr = origin
        while self.succ(curr):
            curr = self.succ(curr)
            succs.append(curr)
        
        # merge precs and succs elementwise with origin
        ziplist = zip(precs, itertools.cycle(succs)) if len(precs) > len(succs) else zip(itertools.cycle(precs), succs)
        suggestions = [origin] + [item for x in ziplist for item in x]


        return suggestions


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
    corpus.fromJSON('data/dictionary.json')
    print(corpus)
    suggs = corpus.suggest('DAVID')

    for i in range(9):
        print(suggs[i].data)
    corpus.draw()

    # ui = ui.GUI(corpus)

    # ui.master.mainloop()
    
    
