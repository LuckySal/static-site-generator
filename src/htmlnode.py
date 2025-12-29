class HTMLNode:
    """Parent class for all HTML nodes"""

    def __init__(self, tag=None, value=None, children=[], props={}):
        """HTMLNode constructor

        Args:
            tag (string, optional): An HTML tag. Defaults to None.
            value (string, optional): A text value. Defaults to None.
            children (list, optional): A list of children of the node. Defaults to [].
            props (dict, optional): A dictionary of HTML properties. Defaults to {}.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Template for child classes

        Raises:
            NotImplementedError: Child classes must implement
        """
        raise NotImplementedError(
            f"child class {type(self)} must override to_html method"
        )

    def props_to_html(self):
        """Returns a formatted string of HTML properties

        Returns:
            string: formatted string of HTML properties
        """
        res = ""
        for key, val in self.props.items():
            res += f' {key}="{val}"'
        return res

    def __repr__(self):
        return (
            "HTMLNode "
            f'tag: "{self.tag}" '
            f'value: "{self.value}" '
            f'children: "{self.children}" '
            f'props: "{self.props}"'
        )


class LeafNode(HTMLNode):
    """An HTML node with no children

    Attributes:
        tag: A string HTML tag
        value: A string text value
        props: A dictionary of properties. Default is empty dictionary.
    """

    def __init__(self, tag, value, props={}):
        """LeafNode constructor

        Args:
            tag (string): The HTML tag
            value (string): The text value
            props (dict, optional): A dictionary of properties. Defaults to {}.
        """
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        """Returns a formatted HTML string using node properties.

        Raises:
            ValueError: leaf nodes must have a value

        Returns:
            string: HTML formatted string
        """
        if not self.value:
            raise ValueError("leaf nodes must have a value")
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
