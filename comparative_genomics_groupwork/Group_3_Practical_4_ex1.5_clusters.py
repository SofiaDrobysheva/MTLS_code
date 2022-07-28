import argparse
import csv

def csv_to_dict(filenameone, filenametwo, filenamethree):
    data = {}
    with open(filenameone, 'r') as h:
        for line in h:
            ref_hit = line.split(',')
            reference = ref_hit[0]
            ref_hit[1]=ref_hit[1].rstrip("\n")
            if not reference in data:
                data[reference] = []
            data[reference] += [ref_hit[1]]
    
    with open(filenametwo, 'r') as h:
        for line in h:
            ref_hit = line.split(',')
            reference = ref_hit[0]
            ref_hit[1]=ref_hit[1].rstrip("\n")
            if not reference in data:
                data[reference] = []
            data[reference] += [ref_hit[1]]

    with open(filenamethree, 'r') as h:
        for line in h:
            ref_hit = line.split(',')
            reference = ref_hit[0]
            ref_hit[1]=ref_hit[1].rstrip("\n")
            if not reference in data:
                data[reference] = []
            data[reference] += [ref_hit[1]]

    return data

def main(args):
    clusters=csv_to_dict(args.input_one,args.input_two,args.input_three)
    # for item in clusters.items():
    #     print(item)
    with open(args.output,'w') as f:
        for key, values in clusters.items():
            f.write(key)
            for value in values:
                f.write(",{}".format(value))
            f.write("\n")


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Takes as input three files (.csv) containing in the first column a list of ORFs of a reference genome and in the second column the best hit in the db for that particular ORF (i.e. the output files of Group_3_Practical_4_ex1.py) and produces from them clusters of the best hit for each reference ORF in each genome", formatter_class=argparse.RawTextHelpFormatter)
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument("input_one", type=str, help="path or name of the first input csv file")
    parser.add_argument("input_two", type=str, help="path or name of the second input csv file")
    parser.add_argument("input_three", type=str, help="path or name of the third input csv file")
    parser.add_argument("-o", "--output", type=str, help="path or name of the output file", default="out.csv") 

    args = parser.parse_args()

    main(args)