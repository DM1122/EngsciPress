import praw
import random



class NGram:
    '''
    An NGram structure.
    '''

    def __init__(self, n=2):
        self.model = {}
        self.n = n


    def __str__(self):
        out = 'NGram Size: {}'.format(self.getSize())

        return out


    def getSize(self):
        return len(self.model)


    def buildFromReddit(self, sub):
        '''
        Constructs an NGram model from reddit posts. Currently only supports scraping post titles.
        '''

        # reddit = praw.Reddit(client_id='RjPARG19Tby6Qg',
        #                     client_secret='aCdpV9DOkRCfIW2boaV-xX7SnGY',
        #                     user_agent='windows:scrapper:v1.0 (by u/David_M1122)')

        # scrape = []
        # for submission in reddit.subreddit(sub).hot(limit=50):
        #     scrape.append(submission.title)

        # string = scrape[10]
        # print('Original:',string)
        string = 'Hello world! I leave now.'

        self.feed(string)


    def generate(self, seed=None, length=12):
        '''
        Generates a string of words based on model probabilities.
        '''

        if seed == None:
            tokens = [gram[0] for gram in self.model]
            seed = random.choice(tokens)

        print('Seed:',seed)

        
        output = [seed]
        for i in range(length):
            choices, data =  [(gram, data) for gram, data in self.model.items() if gram[0] == seed]
            print('choices',choices)

            grams = [choice[0] for choice in choices]
            print('grams',grams)
            
            
            token = random.choices([], weights=data['prob'], k=1)
            output.append()
            seed = token



        return output


    def updateProbs(self):
        '''
        Updates all the gram probabilities in the model.
        '''

        sum = 0
        for data in self.model.values():
            sum += data['count']

        for data in self.model.values():
            data['prob'] = data['count'] / sum


    def feed(self, string):
        '''
        Takes in string of arbitrary length and updates model accordingly.
        '''

        string = string.split()

        for i in range(len(string)-self.n+1):
            gram = ()
            for j in range(self.n):
                gram += (string[i+j],)
            
            if gram not in self.model:
                self.model[gram] = {'count':1,'prob':0}
            else:
                self.model[gram]['count'] += 1
            
        self.updateProbs()





if __name__ == '__main__':

    model = NGram()
    model.buildFromReddit('casualconversation')

    print(model)
    print(model.model)

    output = model.generate(seed='Hello')

    print(output)
