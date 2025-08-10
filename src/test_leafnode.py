import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_props_to_html_a(self):
        node= LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_props_to_html_multiple_attributes(self):
        """
        Verifica que el método to_html() maneje correctamente múltiples atributos.
        """
        props = {
            "href": "https://www.openai.com",
            "target": "_blank",
            "class": "external-link"
        }
        node = LeafNode("a", "Visita OpenAI", props)
        expected_html = '<a href="https://www.openai.com" target="_blank" class="external-link">Visita OpenAI</a>'
        self.assertEqual(node.to_html(), expected_html)
    
    

if __name__ == "__main__":
    unittest.main()
