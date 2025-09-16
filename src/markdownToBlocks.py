from blocktype import block_to_block_type, BlockType
from htmlnode import HTMLNode
from textnodetohtml import text_node_to_html_node
from splitnodesdelimiter import text_to_textnodes
from parentNode import ParentNode
from textnode import TextNode, TextType


def extract_title(markdown:str):
    lines = markdown.splitlines()
    for line in lines: 
        if line.strip().startswith("# ") and line.strip():
            title = line.split("# ", 1)
            return title[1].strip()
    raise ValueError("There is no title in this markdown")




def markdown_to_blocks(text:str):
    blocks = text.split("\n\n")
    new_blocks=[]
    for block in blocks:
        if block.strip():
            new_block="\n".join(line.strip() for line in block.splitlines() if line.strip())
            
            new_blocks.append(new_block)
        else:
            continue
    return new_blocks

def text_to_children(text:str):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]



def markdown_to_html_node(markdown:str):
    
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.HEADING:
            split =block.split(maxsplit=1)
            tag = f"h{len(split[0])}"
            children = text_to_children(split[1])
            html_blocks.append(ParentNode(tag=tag,children=children))
            continue

        elif type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            html_blocks.append(ParentNode(tag="p", children=children))
            continue

        elif type == BlockType.QUOTE:
            text = "\n".join([line.split(">",1)[1].strip() for line in block.splitlines()])
            children = text_to_children(text)
            html_blocks.append(ParentNode(tag="blockquote", children=children))
            continue

        elif type == BlockType.UNORDERED_LIST:
            lines = [line.split("-",1)[1].strip() for line in block.splitlines()]
            children = []
            for line in lines:
                grandchildren = text_to_children(line)
                children.append(ParentNode("li", grandchildren))
            html_blocks.append(ParentNode(tag="ul", children=children))
            continue

        elif type == BlockType.ORDERED_LIST:
            lines = [line.split(".",1)[1].strip() for line in block.splitlines()]
            children = []
            for line in lines:
                grandchildren = text_to_children(line)
                children.append(ParentNode("li", grandchildren))
            html_blocks.append(ParentNode(tag="ol", children=children))
            continue

        elif type == BlockType.CODE:
            text = block.split("```", 1)[1].rsplit("```", 1)[0]
            code_node = TextNode(text=text, text_type= TextType.CODE)
            children = [text_node_to_html_node(code_node)]
            html_blocks.append(ParentNode(tag = "pre", children=children) )
            continue
        
    return ParentNode(tag = "div", children= html_blocks)
        

            



            
            
