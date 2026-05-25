class HTMLNode():
    def __init__(self, tag = None, value = None, children =  None, props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        if not self.props:
            return ""
        atr = ""
        for i in self.props:
            atr += " "
            atr += i + "=" + '"'
            atr += self.props[i] +'"'
        return atr
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"   
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent object must have tag")
        if self.children == None:
            raise ValueError("Parent node must have children")
        return_string =  f"<{self.tag}{self.props_to_html()}>"
        for i in self.children:
            return_string += f"{i.to_html()}"
        return_string += f"</{self.tag}>"
        return return_string