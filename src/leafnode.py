from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag:str, value:str, props:dict = None):
        super().__init__(tag=tag,value=value,props=props)
    
    def to_html(self):
        if self.value is not None:
            if self.tag is not None:
                if self.tag=="img":
                    return f"<{self.tag} {self.props_to_html()}".strip() + f">{self.value.strip()}"
                return f"<{self.tag} {self.props_to_html()}".strip() + f">{self.value.strip()}</{self.tag}>"
            else:
                return self.value
        else:
            raise ValueError
        