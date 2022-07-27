import random
from random import randrange

file = open('generated_data.txt', 'w')

n = random.randrange(1,10) #number of batches; randomly generated in the range from 1 to 10
k = random.randrange(1,10)
merged  = []

for i in range(n):
    n_id = str(i+1) #batch-id #(!!!) Now I want to tell it to repeat twice
    for j in range(k):
        x = round(random.uniform(0, 1), 2)  #x-coordinates
        y = round(random.uniform(0, 1), 2)  #y-coordinates
        m = randrange(100)  #measurments 
        merged.append(str(n_id) + ", "  + str(x) + ", " + str(y) + ", " + str(m)) # or however the formatting should be. 
        string = "\n".join(merged)
        
file.writelines(str(string))

file.close()
