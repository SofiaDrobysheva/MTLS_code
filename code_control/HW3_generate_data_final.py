import random
import string
import numpy as np
import argparse
from random import randrange

#Some lines might contain an additional comma (i.e., more than 4 values) - this homework requirement was not achived
# -- any suggestions how to achive it are very welcomed! :)

def data_generator(n_p, batch_id, path):

    '''Random data generator. 
    Input: Number of data points (n_p).
    The upper limit of the range from which batch id (batch_id) will be picket (the lower limit is 1 and is hardcoded into the function).
    The path, that specifies the name of the file and the path to it.

    Output: A text file with randomly generated data, organized in comma separated strings. 
    Measurments are mostly (90%) composed of integers in the range between 0 and 100. 
    5% are negative integers in range of -1 and -100, and the remaining 5% of measurments are random letters (string elements).
    '''

    outfile = open(path, 'w') 
    g_data = []

    for i in range(n_p): #in range of the number of points

        b_id = randrange(1, batch_id) 
        x = round(random.uniform(0, 1), 2)  #x-coordinates
        y = round(random.uniform(0, 1), 2)  #y-coordinates
        
        lett = random.choice(string.ascii_letters)
        minus = random.randint(-100, -1) #outside of the radius of a valid measurment 
        normal = random.randint(0, 100) 

        probabilities = [0.05, 0.05, 0.9]
        pre_m = [lett, minus, normal] #list of pre-selected measurments, selection is based on the specified probabilities
        m = random.choices(pre_m, probabilities) #choosing final measurment 
        s = "{0}, {1}, {2}, {3} \n".format(b_id, x, y, m[0])
        outfile.write(s)
        g_data.append(s)

    outfile.close()
    return g_data

def main(args):
    try:
        data_generator(args.n_p, args.batch_id, args.path) 
    except:
        print("An error related to parsing occured.\
        Check if the file has the right format.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generating random data and saving it to a text file.", \
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('n_p', type=int, default = 10, 
        help='Number of data points')
    parser.add_argument('batch_id', type=int, default = 5, 
        help='The range from which Batch_ids will be randomly picked')
    parser.add_argument('path', type=str,
        help='File name and its directory, where file will be saved. If you provide directiry/file_name.txt and it returns you an error,\
         then try to only write a file_name.txt. Your file will then be saved in the same directiry where the code is.') 

    args = parser.parse_args()
    main(args)