import os
import shutil

def copy_files(source_path=None, destiny_path=None):
    
    if source_path is not None:
        directories = os.listdir(source_path)
        for element in directories:
            element_path = os.path.join(source_path, element)
            if os.path.isfile(element_path):
                shutil.copy(element_path,destiny_path)
            else:
                destiny_path=os.path.join(element_path, element)
                os.mkdir(destiny_path)
                copy_files(source_path=element_path, destiny_path=destiny_path)


    else:
        shutil.rmtree("./public")
        os.mkdir("./public")
        directories = os.listdir("./static")
        for element in directories:
            element_path = f"./static/{element}"
            if os.path.isfile(element_path):
                shutil.copy(element_path, "./public")
            else:
                destiny_path = os.path.join("./public", element)
                os.mkdir(destiny_path)
                copy_files(source_path=element_path, destiny_path=destiny_path)

