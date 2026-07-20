from fastapi import APIRouter

from app.parsers.tree_sitter_parser import TreeSitterParser
from app.parsers.ast_parser import ASTParser

router = APIRouter(
    prefix="/parser",
    tags=["Parser"],
)


@router.post("/ast")
async def parse_ast(
    language: str,
    code: str,
):

    tree = TreeSitterParser.parse(
        language,
        code,
    )

    root = tree.root_node

    return ASTParser.traverse(root)