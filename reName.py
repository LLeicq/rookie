import os
import numpy


path ='..\\红树林鸟类声音\\mp3\\0黑领椋鸟'
all_file = os.listdir(path)
for filename in all_file:
    if filename.find(' ') > 0:
        temp = filename.split('-')
        if len(temp[3][1:].split(' ')) == 3:
            new_name = temp[0][:-1]+'-'+temp[3][1:].split(' ')[0]+'_'+temp[3][1:].split(' ')[1]+temp[3][1:].split(' ')[2][-4:]
        else:
            new_name = temp[0][:-1]+'-'+temp[3][1:].replace(' ', '_')
        os.rename(os.path.join(path, filename), os.path.join(path, new_name))

#path ='..\\红树林鸟类声音\\白头鹎'
#all_file = os.listdir(path)
#for filename in all_file:
#    
#    temp = filename.split('-')
#    new_name = temp[0] 
#    os.rename(os.path.join(path, filename), os.path.join(path, new_name))

   
