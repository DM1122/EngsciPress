import praw
import progress.bar
import random



class NGram:
    '''
    An NGram structure.
    '''

    def __init__(self, n=2):
        self.model = {}
        self.n = n


    def __str__(self):
        out = 'NGram Size: {}'.format(
            self.getSize())

        return out


    def getSize(self):
        return len(self.model)


    def buildFromReddit(self, sub, limit):
        '''
        Constructs an NGram model from reddit posts. Currently only supports scraping post titles.
        '''

        print('Building model from Reddit')

        reddit = praw.Reddit(client_id='RjPARG19Tby6Qg',
                             client_secret='aCdpV9DOkRCfIW2boaV-xX7SnGY',
                             user_agent='windows:scrapper:v1.0 (by u/David_M1122)')

        bar = progress.bar.Bar('Scraping', max=limit)
        scrape = []
        for submission in reddit.subreddit(sub).hot(limit=limit):
            
            scrape.append(submission.title)

            bar.next()
        bar.finish()

        bar = progress.bar.Bar('Feeding model', max=len(scrape))
        for string in scrape:
            self.feed(string)
            bar.next()
        bar.finish()


    def generate(self, seed=None, length=16):
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
            
            if not choices:
                break

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


    def prune(self):
        '''
        Prunes all grams in model with lowest probability. Updates probabilities.
        '''
        
        print('Pruning model')

        min_prob = min([data['prob'] for data in self.model.values()])
        
        
        to_delete = [gram for gram in self.model if self.model[gram]['prob'] == min_prob]

        for gram in to_delete:
            del self.model[gram]
        
        self.updateProbs()



if __name__ == '__main__':

    model = NGram(n=3)
    model.buildFromReddit(sub='casualconversation', limit=500)

    print(model)
    print(model.generate())

    model.prune()
    print(model)
    print(model.generate())

