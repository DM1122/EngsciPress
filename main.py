import praw
import random

import sys
sys.path.append('C:\\Users\\DMara\\Documents\\_Workbench')
from Workspace import workspacelib
from Forest import forest



class Corpus(forest.Tree):

    def suggest(self, query):
        '''
        Suggestion is made based on which node is closest to where query might have been found.
        '''
        pass
    
    


if __name__ == '__main__':
    ws = workspacelib.Workspace(paths=['data'], verbose=1)

    corpus = Corpus().fromTextFile(filepath='data/words_sample.txt')
