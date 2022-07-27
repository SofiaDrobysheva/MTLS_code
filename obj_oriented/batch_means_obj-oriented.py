class Point: 

    def __init__(self, batch_id, x_coor, y_coor, measurement):
        self.batch_id = batch_id 
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.measurement = measurement

    def is_outlier(self):
        ''' Will use x_coor and y_coor to check control for outliers. 
        Input: Class object (self), to access x_coor and y_coor atributes. Output: True is x and y are below 1. False is x and y are above 1. '''
        if float(self.x_coor)**2 + float(self.y_coor)**2 <= 1:
            return False 
        else: 
            return True


class Batch: 
    
    def __init__(self, batch_id): 
        self.batch_id = batch_id
        self.list_point = []

    def add_point(self, points):
        """Generates a list of samples with points from Points.""" 
        self.list_point.append(points) 

    def batch_average(self): 
        '''Calculates the average of the measurments corresponding to the same batch_id.
        Input: list of points. Output: the printed average and the batch_id. '''

        if len(self.list_point) > 0:  #sanity check, to be sure that we have at least one element indisde the tuple 
            n = 0
            val_sum = 0
            for point in self.list_point: 
                if point.is_outlier:
                    val_sum += point.measurement
                    n += 1
            average = val_sum/n
            print(self.batch_id, "\t", average)
        else:
            print(self.batch_id, "\tNo data") 

         
def creating_batches(file): 
    ''' Formats the text file to create Point and Batch objects to then calculate the mean. 
    Input: a text file prompted by the main function. Output: dictionary named batches. '''
    with open (file, 'r') as textfile: 
        batches = {}
        for line in textfile: 
            b_id, x_c, y_c, meas = line.split(",") #splits the data and populates b, x_c, y_c, meas respectively
            point_object = Point(int(b_id), float(x_c), float(y_c), int(meas)) #population of Point object
            if point_object.is_outlier():
                continue
            else:
                if b_id not in batches: #if b_id is not in batches
                    batch_object = Batch(b_id)
                    batch_object.add_point(point_object) #collecting all data from Point object
                    batches[b_id] = batch_object #linking batch_id to the Batch object
                else: 
                    batch_object = batches[b_id]
                    batch_object.add_point(point_object)
    return batches

def main():
    '''Calles the text file on which action will be performed. '''
    filename = input('Name of the text file? ') #Here, run my previously generated_data.txt file 
    batch_dict = creating_batches(filename)
    for key, batch in batch_dict.items():
        batch.batch_average()

if __name__ == '__main__':
    main()