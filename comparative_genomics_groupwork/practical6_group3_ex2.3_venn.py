import argparse
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import csv

genome_1=12
genome_2=8

def csv_to_list(filename):
    data = []
    with open(filename, 'r') as h:
        for line in h:
            ref_hit = line.split(',')
            ref_hit[len(ref_hit)-1]=ref_hit[len(ref_hit)-1].rstrip("\n")
            data.append(ref_hit)
    
    return data

def savelist(name,list):
	with open(name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(list)

def main(args):
    BBH_list=csv_to_list(args.input_one)
    InParanoid_list=csv_to_list(args.input_two)
    intersection=[element for element in BBH_list if element in InParanoid_list]

    savelist(args.output,intersection)

    venn2(subsets = (len(BBH_list), len(InParanoid_list), len(intersection)), set_labels = ('BBH clusters', 'InParanoid clusters'))
    plt.title("Comparison between BBH clusters and InParanoid clusters")
    plt.show()
    plt.close()

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Takes in input two .csv files, makes a venn diagram of their elements and saves a .csv containing their intersection", formatter_class=argparse.RawTextHelpFormatter)
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument("input_one", type=str, help="path or name of the first input csv file")
    parser.add_argument("input_two", type=str, help="path or name of the second input csv file")
    parser.add_argument("-o","--output", type=str, help="path or name of the output csv file, containing the intersection of the inputs")
    


    args = parser.parse_args()

    main(args)