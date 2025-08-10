from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict = None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if self.tag:
            if self.children:
                html = f"<{self.tag} {self.props_to_html()}".strip() + ">"
                for child in self.children:
                    html += child.to_html()
                return f"{html}</{self.tag}>"

                
            else:
                raise ValueError("No children")

        else:
            raise ValueError("No tag")
