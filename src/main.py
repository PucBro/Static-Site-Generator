from copyfiles import copy_files
from generate_page import generate_page, generate_pages_recursive
import sys, os
import shutil



def main():
    if sys.argv[0]:
        base_path = sys.argv[0]
    else:
        base_path = "/"
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        os.mkdir("./public")
    copy_files(source_path="./static", destiny_path="./public")
    generate_pages_recursive("./content", "./template.html", "./public")
    


if __name__== "__main__":
    main()

