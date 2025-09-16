import unittest
from markdownToBlocks import markdown_to_blocks, markdown_to_html_node, extract_title
import re



class TestMarkdownToBlocks(unittest.TestCase):
        
        def _normalize_html(self, html_string: str) -> str:
            """
            Toma un string de HTML y lo normaliza:
            1. Reemplaza cualquier secuencia de espacios en blanco (espacios, saltos de línea, tabs) con un solo espacio.
            2. Elimina los espacios en blanco al principio y al final.
            """
            return re.sub(r'\s+', ' ', html_string).strip()
        def test_markdown_to_blocks(self):
            md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
                """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_empty_string(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])

        def test_single_paragraph(self):
            md = "Just a single paragraph with no breaks."
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, ["Just a single paragraph with no breaks."])

        def test_multiple_lists(self):
            md = """
                - First list item
                - Second list item

                - Another list
                - More items
                """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "- First list item\n- Second list item",
                    "- Another list\n- More items",
                ],
            )
        def test_paragraphs(self):
            md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

            node = markdown_to_html_node(md)
            
            html = node.to_html()
            print(html)
            self.assertEqual(
                self._normalize_html(html),
                self._normalize_html("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"),
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
                self._normalize_html(html),
                self._normalize_html("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"),
            )
        def test_combined_markdown(self):
    # Input Markdown
            md = """
        # Main Title

        This is the first paragraph. It includes **bold** and _italic_ text.

        > A wise person once said something profound.

        ## Subtitle

        . First ordered item.
        . Second, with a `code` snippet.

        - An unordered item.
        - Another unordered item.
        """

            # Expected HTML
            expected_html = "<div><h1>Main Title</h1><p>This is the first paragraph. It includes <b>bold</b> and <i>italic</i> text.</p><blockquote>A wise person once said something profound.</blockquote><h2>Subtitle</h2><ol><li>First ordered item.</li><li>Second, with a <code>code</code> snippet.</li></ol><ul><li>An unordered item.</li><li>Another unordered item.</li></ul></div>"

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(self._normalize_html(html), self._normalize_html(expected_html))
        
        def test_headings(self):
            md = """
            # This is an h1

            ## This is an h2

            ###### This is an h6

            """
            expected_html = "<div><h1>This is an h1</h1><h2>This is an h2</h2><h6>This is an h6</h6></div>"

            actual_html = markdown_to_html_node(md).to_html()
            self.assertEqual(
                self._normalize_html(actual_html),
                self._normalize_html(expected_html)
            )
        def test_inline_links_and_images(self):
            md = "This is a paragraph with a [link to Google](https://google.com) and an ![image of a cat](https://placekitten.com/200/300)."
            expected_html = '<div><p>This is a paragraph with a <a href="https://google.com">link to Google</a> and an <img src="https://placekitten.com/200/300" alt="image of a cat">.</p></div>'

            actual_html = markdown_to_html_node(md).to_html()
            self.assertEqual(
                self._normalize_html(actual_html),
                self._normalize_html(expected_html)
            )
        def test_simple_h1_title(self):
            """Prueba que extrae un título H1 simple y correcto."""
            md = "# Este es el título principal"
            self.assertEqual(extract_title(md), "Este es el título principal")

        def test_title_with_leading_and_trailing_whitespace(self):
            """Prueba que la función limpia los espacios en blanco del título."""
            md = "#   Un título con espacios extra   "
            self.assertEqual(extract_title(md), "Un título con espacios extra")

        def test_returns_only_the_first_h1_title(self):
            """Prueba que la función se detiene y devuelve solo el primer título H1 que encuentra."""
            md = """
            Contenido previo.
            # Primer Título
            Más contenido.
            # Segundo Título que debe ser ignorado
            """
            self.assertEqual(extract_title(md), "Primer Título")

        # ⚠️ Casos que deben lanzar ValueError
        # ------------------------------------
        def test_raises_error_if_no_title_exists(self):
            """Prueba que lanza ValueError si no hay ninguna línea de título."""
            md = "Este es un párrafo de texto normal.\nSin ningún título."
            with self.assertRaises(ValueError):
                extract_title(md)

        def test_raises_error_for_empty_markdown(self):
            """Prueba que lanza ValueError para un string de markdown vacío."""
            md = ""
            with self.assertRaises(ValueError):
                extract_title(md)

        def test_raises_error_for_h2_or_lower_titles(self):
            """Prueba que ignora títulos que no son H1 (##, ###) y lanza un error."""
            md = "## Este es un subtítulo, no un título principal"
            with self.assertRaises(ValueError):
                extract_title(md)
                
        def test_raises_error_if_no_space_after_hash(self):
            """
            Prueba un caso límite importante: la función requiere un espacio después del '#'.
            """
            md = "#TítuloSinEspacio"
            with self.assertRaises(ValueError):
                extract_title(md)

if __name__ == "__main__":
     unittest.main()