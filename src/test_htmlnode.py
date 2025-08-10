import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        htmlNode =HTMLNode(tag="<a>", props={"href": "https://www.google.com","target": "_blank",})
        result =  'href="https://www.google.com" target="_blank"'
        self.assertEqual(htmlNode.props_to_html(), result)
    
    def test_props_to_html2(self):
        htmlNode =HTMLNode(tag="<a>", props={"href": "https://www.google.com","target": "_blank", "class":"perrona"})
        result =  'href="https://www.google.com" target="_blank" class="perrona" '
        self.assertNotEqual(htmlNode.props_to_html(), result)
    
    def test_props_to_html3(self):
        htmlNode =HTMLNode(tag="<a>", props={"href": "https://www.google.com","target": "_blank", "class":"perrona"})
        result =  'href="https://www.google.com" target="_blank" class="perrona"'
        self.assertEqual(htmlNode.props_to_html(), result)
    
    
if __name__ == "__main__":
    unittest.main()

    




        