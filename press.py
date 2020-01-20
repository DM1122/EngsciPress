import praw
import random


class Dicktionary:
    
    def __init__(self):
        pass

    @classmethod
    def build(cls, file_name):
        '''
        Build word dictionary from text file.
        '''
        pass
        # return cls(...)
    
    
    def search(self, query):
        pass


    def insert(self, word, definition):
        pass


    def delete(self, query):
        pass


    def suggest(self, query):
        pass


class RedditGram:
    '''
    An NGram structure.
    '''

    def __init__(self, gram, dictionary):
        self.gram = gram
        self.dictionary = dictionary    # a Dicktionary structure composed of allowable words
        

    @classmethod
    def build(cls, sub, dictionary):
        pass
        # return cls(gram, dictionary)



    def generate(self, count):
        pass
        # return output







if __name__ == '__main__':
    reddit = praw.Reddit(client_id='RjPARG19Tby6Qg',
                        client_secret='aCdpV9DOkRCfIW2boaV-xX7SnGY',
                        user_agent='windows:scrapper:v1.0 (by u/David_M1122)')

    sentences = []
    for submission in reddit.subreddit('casualconversation').hot(limit=50):
        sentences.append(submission.title)
