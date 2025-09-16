from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING= "heading"
    CODE = "code"
    QUOTE="quote"
    UNORDERED_LIST="unorderer_list"
    ORDERED_LIST = "orderer_list"

#Determines the block type of a block
def block_to_block_type(block: str):
    for i in range (6):
        if block.startswith("#"*(i+1) + " "):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.splitlines()
    quote_block = False
    unordered_list = False
    ordered_list = False
    for line in lines:
        if line.startswith(">"):
            quote_block = True
        else:
            quote_block= False
            break
    if quote_block:
        return BlockType.QUOTE 
    for line in lines:
        if line.startswith("-"):
            unordered_list = True
        else:
            unordered_list= False
            break
    if unordered_list:
        return BlockType.UNORDERED_LIST 
    for line in lines:
        if re.match(r"^\d|^\.", line.strip()):
            ordered_list = True
        else:
            ordered_list= False
            break
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
    
