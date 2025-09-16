from copyfiles import copy_files
from generate_page import generate_page, generate_pages_recursive


def main():
    copy_files()
    generate_pages_recursive("./content", "./template.html", "./public")
    


if __name__== "__main__":
    main()

