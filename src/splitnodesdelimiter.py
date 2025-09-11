from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type: TextType):  
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split = node.text.split(delimiter)
            if len(split) % 2 == 0:
                raise ValueError("that's invalid Markdown syntax.")
            for i in range(len(split)):
                if i%2 == 1:
                    new_nodes.append(TextNode(split[i], text_type))
                else:
                    if split[i]:
                        new_nodes.append(TextNode(split[i], TextType.TEXT))
                    continue
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text:str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text:str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes:list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if len(images)== 0:
                new_nodes.append(node)
                continue
            for image, link in images:
                split = node.text.split(f"![{image}]({link})", 1)
                if len(split) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if split[0]:
                    if split[1]:
                        new_nodes.extend([TextNode(split[0],TextType.TEXT),TextNode(image, TextType.IMAGE, link), TextNode(split[1],TextType.TEXT)])
                    else:
                        new_nodes.extend([TextNode(split[0],TextType.TEXT),TextNode(image, TextType.IMAGE, link)] )
                else:
                    if split[1]:
                        new_nodes.extend([TextNode(image, TextType.IMAGE, link), TextNode(split[1],TextType.TEXT)])
                    else:
                        new_nodes.append(TextNode(image, TextType.IMAGE, link))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes:list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if len(links)== 0:
                new_nodes.append(node)
                continue
            for name, link in links:
                split = node.text.split(f"[{name}]({link})", 1)
                if len(split) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if split[0]:
                    if split[1]:
                        new_nodes.extend([TextNode(split[0],TextType.TEXT),TextNode(name, TextType.LINK, link), TextNode(split[1],TextType.TEXT)])
                    else:
                        new_nodes.extend([TextNode(split[0],TextType.TEXT),TextNode(name, TextType.LINK, link)] )
                else:
                    if split[1]:
                        new_nodes.extend([TextNode(name, TextType.LINK, link), TextNode(split[1],TextType.TEXT)])
                    else:
                        new_nodes.append(TextNode(name, TextType.LINK, link))
        else:
            new_nodes.append(node)
    return new_nodes
                
                
           




def text_to_textnodes(text:str):
    new_nodes =[TextNode(text, TextType.TEXT)]
    types= {TextType.BOLD:"**", TextType.CODE:"`", TextType.ITALIC:"_"}
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    for item in types:
        new_nodes = split_nodes_delimiter(new_nodes,types[item],item)
    return new_nodes



    




            
