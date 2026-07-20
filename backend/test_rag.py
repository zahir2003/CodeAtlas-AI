import asyncio

from app.services.rag_service import RAGService


async def main():

    rag = RAGService()

    result = await rag.answer("Explain the authentication flow.")

    print("\nQuestion:\n")

    print(result["question"])

    print("\nAnswer:\n")

    print(result["answer"])

    print("\nRetrieved Chunks:")

    print(len(result["sources"]))


asyncio.run(main())
