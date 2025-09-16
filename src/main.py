from copyfiles import copy_files
from generate_page import generate_page, generate_pages_recursive
import sys, os
import shutil



def main():
    if len(sys.argv)>1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    os.mkdir("./docs")  
    copy_files(source_path="./static", destiny_path="./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", base_path=base_path)
    


if __name__== "__main__":
    main()

