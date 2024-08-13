class HTMLNode():
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f" {key}=\"{value}\""
        return prop_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag or not children:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def validate_child(self, child):
        if not isinstance(child, HTMLNode):
            raise ValueError("ParentNode children must be HTMLNode instances")
        return child

    def to_html(self):
        if not self.tag: raise ValueError("ParentNode must have a tag")
        if not self.children: raise ValueError("ParentNode must have children")

        return f"<{self.tag}{self.props_to_html()}>{''.join([self.validate_child(child).to_html() for child in self.children])}</{self.tag}>"
    