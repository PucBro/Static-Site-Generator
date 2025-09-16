import os
import shutil

def copy_files(source_path, destiny_path):

    
    directories = os.listdir(source_path)
    for element in directories:
        element_path = os.path.join(source_path, element)     
        if os.path.isfile(element_path):
            path_to_copy =os.path.join(destiny_path, element)
            shutil.copy( element_path,path_to_copy)
        else:
            destiny_path = os.path.join(destiny_path, element)
            os.mkdir(destiny_path)
            copy_files(source_path=element_path, destiny_path=destiny_path)


    

