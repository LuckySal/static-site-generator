import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ul(self):
        md = """
        
# This is a header

- List item
- List item **bold**
- List item _italic text_

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1><ul><li>List item</li><li>List item <b>bold</b></li><li>List item <i>italic text</i></li></ul></div>",
        )

    def test_subheaders(self):
        md = """

# This is a h1

## This is a h2

### This is a h3

#### This is a h4 _some text_

##### This is a h5

###### This is a h6 `code`

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a h1</h1><h2>This is a h2</h2><h3>This is a h3</h3><h4>This is a h4 <i>some text</i></h4><h5>This is a h5</h5><h6>This is a h6 <code>code</code></h6></div>",
        )

    def test_ol(self):
        md = """

## Ordered list

1. Item 1
2. A _sandwich_, please
3. With **pickles**
4. That is all

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Ordered list</h2><ol><li>Item 1</li><li>A <i>sandwich</i>, please</li><li>With <b>pickles</b></li><li>That is all</li></ol></div>",
        )

    def test_blockquote(self):
        md = """

### Quote block

>Darkness cannot drive out darkness:
>only light can do that.
>Hate cannot drive out hate:
>only love can do that.
>- Martin Luther King Jr.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Quote block</h3><blockquote>Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that. - Martin Luther King Jr.</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
