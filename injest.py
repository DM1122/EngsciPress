import csv
import os

filepath = 'data/csv/'
filename = 'A.csv'
outpath = 'data/processed/out.csv'





if __name__ == '__main__':
    # data = []
    # for filename in os.listdir(filepath):
    #     print("Processing '{}'".format(filename))
    #     with open(filepath+filename, 'r') as fil:
    #         reader = csv.reader(fil)
    #         read = [row for row in reader]
    #         data.extend(read)
    
    # print('Outputting csv...')
    # with open(outpath+'output.csv', 'w') as fil:
    #     writer = csv.writer(fil, delimiter='\t')

    # print("Processing '{}'".format(filename))
    # with open(filepath+filename, 'r') as fil:
    #     reader = csv.reader(fil)
    #     read = [row for row in reader]
        
    #     print(read)

    with open(filepath+filename, 'r') as in_file:
        with open(outpath, 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                print('Processing:',row)
                if row != []:
                    row = row.pop().replace('"', '')
                    print('Row is not empty')
                    writer.writerow(row)

"it is icy".replace("i", "")