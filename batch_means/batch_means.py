def organizing_data_file(file):

    '''Reads in the file as a text format, where line is comma separated list'''
    
    data = dict()

    with open(file, 'r') as h:

        for line in h:
            four_vals = line.split(',')
            batch = four_vals[0]
            if not batch in data:
                data[batch] = [] # adding the batch number to the dict_data if it is new
            data[batch] += [(float(four_vals[1]), float(four_vals[2]), float(four_vals[3]))] # collect data from an experiment

    return data

def batch_avarge(data):

    '''Calculates the average of the batch (a group) from the imported dataset. '''

    for batch, sample in data.items(): 

        if len(sample) > 0:
            n = 0
            x_sum = 0
            for (x, y, val) in sample:
                if x**2 + y**2 <= 1:
                    x_sum += val
                    n += 1
            average = x_sum/n
            print(batch, "\t", average)

        else:
            print(batch, "\tNo data")
            

if __name__ == '__main__':
    batch_avarge(organizing_data_file(input('Which data file? Insert path to file:')))