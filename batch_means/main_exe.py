from batch_means import organizing_data_file as reorg
from batch_means import batch_avarge as ba

def main():
    '''Input: A comma seprated text file, each string starting from a new line. 
    Output: the average of each batch of values'''
    ba(reorg(input('Which data file? Insert path to file:')))

if __name__=='__main__':
    main()