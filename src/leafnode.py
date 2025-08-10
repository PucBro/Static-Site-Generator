from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag:str, value:str, props:dict = None):
        super().__init__(tag=tag,value=value,props=props)
    
    def to_html(self):
        if self.value:
            if self.tag:
                return f"<{self.tag} {self.props_to_html()}".strip() + f">{self.value}</{self.tag}>"
            else:
                return self.value
        else:
            raise ValueError
        