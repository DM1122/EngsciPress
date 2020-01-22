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
        print('Building model from Reddit')

        reddit = praw.Reddit(client_id='RjPARG19Tby6Qg',
                             client_secret='aCdpV9DOkRCfIW2boaV-xX7SnGY',
                             user_agent='windows:scrapper:v1.0 (by u/David_M1122)')

        scrape = []
        for submission in reddit.subreddit(sub).hot(limit=100):
            scrape.append(submission.title)

        print('Feeding model')

        for string in scrape:
            self.feed(string)


    def generate(self, seed=None, length=12):
        '''
        Generates a string of words based on model probabilities.
        '''

        if seed != None:
            if seed not in [gram[0] for gram in self.model]:
                raise Exception('Seed not in model!')
        else:
            tokens = [gram[0] for gram in self.model]
            seed = random.choice(tokens)

        output = [seed]
        for i in range(length):
            
            choices =  [(gram, data['prob']) for gram, data in self.model.items() if gram[0] == seed]

            grams, probs = zip(*choices)
            
            token = random.choices(grams, weights=probs, k=1)[0][1]
            output.append(token)
            seed = token

        output = ' '.join(output)


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

    model = NGram(n=3)
    model.buildFromReddit('casualconversation')

    print(model)
    print(model.model)

    output = model.generate()

    print('Output:',output)
