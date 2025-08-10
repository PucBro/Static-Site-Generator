import unittest

from parentNode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple_nodes(self):
        parent_node =  ParentNode("p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
        self.assertEqual(parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_parent_node_with_attributes(self):
        """
        Verifica que el ParentNode renderice correctamente sus propios atributos.
        """
        child_node_1 = LeafNode(None, "Hola ")
        child_node_2 = LeafNode("b", "mundo")
        props = {"class": "greeting", "id": "main-message"}
        parent_node = ParentNode("p", [child_node_1, child_node_2], props)
        expected_html = '<p class="greeting" id="main-message">Hola <b>mundo</b></p>'
        self.assertEqual(parent_node.to_html(), expected_html)

        
    
    def test_nested_nodes_with_multiple_attributes(self):
        """
        Verifica que la estructura anidada con atributos múltiples en diferentes niveles
        se renderice correctamente.
        """
        # Nodo más interno (hoja) con un atributo
        grandchild_node = LeafNode("a", "Google", {"href": "https://google.com"})

        # Nodo intermedio (padre) con múltiples atributos y un hijo
        child_node_props = {"class": "link-container", "data-type": "external"}
        child_node = ParentNode("div", [grandchild_node], child_node_props)

        # Nodo más externo (padre) con múltiples hijos (otro padre y una hoja)
        parent_node_props = {"id": "main-content", "style": "padding: 10px;"}
        parent_node = ParentNode("section", [
            child_node,
            LeafNode("p", "Esto es otro párrafo.")
        ], parent_node_props)

        expected_html = (
            '<section id="main-content" style="padding: 10px;">'
            '<div class="link-container" data-type="external">'
            '<a href="https://google.com">Google</a>'
            '</div>'
            '<p>Esto es otro párrafo.</p>'
            '</section>'
        )

        self.assertEqual(parent_node.to_html(), expected_html)
    


if __name__=="__main__":
    unittest.main()
