

class HTMLNode():

    def __init__(self, tag:str = None, value:str =None, children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attributes = ''
        if self.props:
            for key in self.props:
                attributes += f'{key}="{self.props[key]}" '
            return attributes.strip()
        else:
            return attributes
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})'



    
