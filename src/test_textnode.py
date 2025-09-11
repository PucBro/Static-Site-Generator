import unittest

from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "http://www.boot.dev")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "http://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "http://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_splitNode_error(self):
        # Caso inválido: número par de delimitadores
        nodes = [TextNode("This **is invalid** markdown **", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_splitNode_no_delimiters(self):
        # No cambia nada si no hay delimitadores
        nodes = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_splitNode_bold(self):
        # Caso válido con un par de ** delimitadores
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_splitNode_italic_multiple(self):
        # Texto con dos segmentos en itálicas
        nodes = [TextNode("Some *italic* and more *text*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and more ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            
        ]
        self.assertEqual(result, expected)

    def test_splitNode_code_inline(self):
        # Caso de `código en línea`
        nodes = [TextNode("Here is `code` snippet", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" snippet", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_splitNode_non_text_node(self):
        # No debe modificar nodos que no son TEXT
        nodes = [TextNode("already bold", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, nodes)
    
    def test_splitNode_multiple_nodes(self):
        # Lista con dos nodos, uno con delimitadores y otro sin
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Just plain", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Just plain", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_splitNode_mixed_types(self):
        # Lista con un nodo TEXT y otro ya en BOLD (no se debe dividir el segundo)
        nodes = [
            TextNode("Mix *italic* here", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Mix ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_splitNode_multiple_nodes_with_error(self):
        # Varios nodos, unos válidos y el último con error de delimitador sin cerrar
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),   # válido
            TextNode("Here is *italic* too", TextType.TEXT),    # válido
            TextNode("Broken **bold start only", TextType.TEXT) # inválido (sin cerrar)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_splitNode_multiple_nodes_with_errors(self):
        # Varios nodos, unos válidos y el último con error de delimitador sin cerrar
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),   # válido
            TextNode("Here is *italic* too", TextType.TEXT),    # válido
            TextNode("Broken **bold start only** but this dont have **delimiter", TextType.TEXT) # inválido (sin cerrar)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        ##Test cases for extract_markdown_images, extract_markdown_links
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) in the text."
        result = extract_markdown_images(text)
        expected = [("alt text", "http://example.com/image.png")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links(self):
        text = "Here is a [link text](http://example.com) in the text."
        result = extract_markdown_links(text)
        expected = [("link text", "http://example.com")]
        self.assertEqual(result, expected)
    def test_no_empty_node_at_start(self):
        """
        Prueba que no se cree un TextNode vacío al principio si el texto
        comienza con markdown.
        """
        text = "**Bold** at the beginning."
        # La versión anterior podría haber producido: [TextNode("", "text"), TextNode("Bold", "bold"), ...]
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the beginning.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_empty_node_at_end(self):
        """
        Prueba que no se cree un TextNode vacío al final si el texto
        termina con markdown.
        """
        text = "Text ending with `code`"
        # La versión anterior podría haber producido: [..., TextNode("code", "code"), TextNode("", "text")]
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)
        
    def test_only_markdown_element(self):
        """
        Prueba que un texto que es solo un elemento markdown no genera
        nodos de texto vacíos alrededor.
        """
        text = "![Just an image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Just an image", TextType.IMAGE, "https://example.com/img.png")
        ]
        self.assertEqual(result, expected)

    def test_consecutive_markdown_no_empty_node(self):
        """
        Prueba que no se cree un TextNode vacío entre dos elementos
        markdown consecutivos.
        """
        text = "A [link](https://boot.dev)**followed by bold**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("followed by bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        """
        Prueba específicamente con una imagen al inicio del texto.
        """
        text = "![alt text](url) followed by text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("alt text", TextType.IMAGE, "url"),
            TextNode(" followed by text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    def test_interleaved_mismatched_delimiters(self):
        """
        Prueba con delimitadores mal entrelazados. Esto es markdown inválido
        y debería lanzar un error.
        """
        text = "This is **bold that starts and _italic that ends**._"
        with self.assertRaises(ValueError, msg="Debería fallar con delimitadores mal entrelazados"):
            text_to_textnodes(text)

    def test_delimiters_with_only_whitespace(self):
        """
        Prueba qué sucede con delimitadores que solo contienen espacios.
        No debería crear un nodo vacío.
        """
        text = "This should not be empty: ** **. And this: ` `."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This should not be empty: ", TextType.TEXT),
            TextNode(" ", TextType.BOLD),
            TextNode(". And this: ", TextType.TEXT),
            TextNode(" ", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_resembling_delimiters(self):
        """
        Prueba texto que contiene caracteres de delimitador pero no debería
        ser formateado, como en nombres de archivo.
        """
        text = "The file is `my_awesome_file.py`. Don't format the underscores."
        result = text_to_textnodes(text)
        expected = [
            TextNode("The file is ", TextType.TEXT),
            TextNode("my_awesome_file.py", TextType.CODE),
            TextNode(". Don't format the underscores.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_complex_markdown_in_one_line(self):
        """
        Prueba una mezcla densa de todo en una sola línea para verificar la robustez general.
        """
        text = "Start with a `code_block`, then a link to [Boot.dev](https://boot.dev) and an image ![alt](img.url) **and finish bold.**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Start with a ", TextType.TEXT),
            TextNode("code_block", TextType.CODE),
            TextNode(", then a link to ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.url"),
            TextNode(" ", TextType.TEXT),
            TextNode("and finish bold.", TextType.BOLD),
        ]
        self.assertEqual(result, expected)



    


if __name__ == "__main__":
    unittest.main()