import HW3_generate_data_final as HW
import unittest

class TestGenerateData (unittest.TestCase):

    def test_data_generator(self):
        ''' Unit test will be controlling for several things. 
        First, if the specified number of data points (n_p) matches the amount generated. 
        Second, if batch_ids were picket from the specified batch_id range (batch_id).
        Input: self 
        Output: asserted test '''

        n_p = 5 # number of the data points (same as the number of lines in our data generating file)
        batch_id = 10 #the range from which batch_id is picket (range is from 1 to 10, for more details see the data generating file)
        file_n = 'test_file.txt' 
        list_of_strings = HW.data_generator(n_p, batch_id, file_n)
        self.assertEqual(len(list_of_strings), n_p) #asserting if the specified number of data points (n_p) matches the amount generated 

        ids = [] 
        for elem in list_of_strings:
            ids.append(elem[0])
        for one_id in ids:
            self.assertTrue(0 < int(one_id) < int(batch_id)) # all batch_ids should be within the specified range
        
if __name__ =='__main__':
    unittest.main()