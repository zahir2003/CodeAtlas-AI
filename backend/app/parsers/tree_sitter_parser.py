from tree_sitter_language_pack import get_parser


class TreeSitterParser:

    @staticmethod
    def parse(language: str, code: str):

        parser = get_parser(language)

        tree = parser.parse(
            bytes(code, "utf-8")
        )

        return tree