import argparse

def organizing_data_file(file):
    '''Reads in a text file and converts it into dictinary, 
    where batch_id is the key and the corresponding data points (samples) are values.
    Input: file.txt     Output: a dictionary '''

    data = dict()
    #with open(file, 'r') as h:
    for line in file:
        four_vals = line.split(',')
        batch = four_vals[0]
        if not batch in data:
            data[batch] = [] #adding the batch number to the dict_data if it is new
        try:
            data[batch] += [(float(four_vals[1]), float(four_vals[2]), float(four_vals[3]))] # Collect data from an experiment
        except ValueError:
            pass #passing on to the next without adding values to the dictionary

    return data


def batch_average(data, rad):
    '''Calculates the average of the batch's measurments, 
    from previously organized file (done by the function above).
    Input: data in form of a dictionary, where batch_id is the key 
    and the corresponding data points (samples) are values. 
    Output: printed average of all the measurments within respective batch-id.'''
    average_dict = {}
    for batch, sample in data.items(): 
        if len(sample) > 0:
            n = 0
            x_sum = 0
            for (x, y, val) in sample:
                if x**2 + y**2 <= rad: 
                    x_sum += val
                    n += 1
            try: 
                average = x_sum/n
                average_dict[batch] = average
            except ZeroDivisionError:
                average_dict[batch] = 'The radius is outside of a specified cut of value. Try to increase the cut-off radius value.'
        else:
            average_dict[batch] = "No data"
    return average_dict


def main(args):
    try:
        organized_data = organizing_data_file(args.fn) #fn = file name 
        bd = batch_average(organized_data, args.rad) #batch dictionary 

        for bat_id, mean in sorted(bd.items()): #by adding sorted my mean values will be ordered
            print(bat_id, "\t", mean)
    except:
        print("An error related to parsing occured.\
        Check if the file is in a right format.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculating the mean of measurments from a text file. Allowed radius (rad) for x and y values should be specified.", \
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--rad', type=float, default = 1, 
        help='allowed radius')
    parser.add_argument('fn', type=argparse.FileType('r'),
        help='input path/name of the input file')

    args = parser.parse_args()
    main(args)