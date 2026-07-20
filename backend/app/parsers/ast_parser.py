class ASTParser:

    @staticmethod
    def traverse(node):

        return {
            "type": node.type,
            "start": node.start_point,
            "end": node.end_point,
            "children": [
                ASTParser.traverse(child)
                for child in node.children
            ],
        }