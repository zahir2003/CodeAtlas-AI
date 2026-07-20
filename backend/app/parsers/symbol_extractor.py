from tree_sitter import Node


class SymbolExtractor:

    @staticmethod
    def extract(root: Node):

        symbols = []

        def visit(node):

            if node.type in (
                "function_definition",
                "class_definition",
            ):

                name = None

                for child in node.children:

                    if child.type == "identifier":

                        name = child.text.decode()

                        break

                symbols.append(
                    {
                        "type": node.type,
                        "name": name,
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                    }
                )

            for child in node.children:

                visit(child)

        visit(root)

        return symbols