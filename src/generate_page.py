import re
from markdownToBlocks import extract_title, markdown_to_html_node
import os

def generate_page(from_path:str,template_path:str, dest_path:str):
    print(f"Generating page from {from_path} to dest_path using {template_path}")
    with open(from_path, "r") as file:
        markdown_contents = file.read()
    with open(template_path, "r") as file:
        template_contents = file.read()
    title = extract_title(markdown_contents)
    content = markdown_to_html_node(markdown_contents).to_html()
    final_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, "w") as file:
        file.write(final_html)

def generate_pages_recursive(dir_path_content:str, template_path:str, dest_dir_path:str):
    directories = os.listdir(dir_path_content)
    for element in directories:
        element_path = os.path.join(dir_path_content, element)
        destiny_path=os.path.join(dest_dir_path, element )
        if os.path.isfile(element_path):
            destiny_path=os.path.join(dest_dir_path, f"{element.split('.md')[0]}.html" )
            generate_page(element_path, template_path=template_path, dest_path=destiny_path)
        else:
            os.mkdir(destiny_path)
            generate_pages_recursive(dir_path_content=element_path, template_path=template_path, dest_dir_path=destiny_path)

    

    