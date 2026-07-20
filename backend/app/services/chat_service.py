from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message import ChatMessage, MessageRole
from app.models.chat_session import ChatSession


class ChatService:
    """
    Handles all chat session operations.
    """

    async def create_session(
        self,
        db: AsyncSession,
        repository_id: UUID,
        title: str = "New Chat",
    ) -> ChatSession:

        session = ChatSession(
            repository_id=repository_id,
            title=title,
        )

        db.add(session)
        await db.commit()
        await db.refresh(session)

        return session

    async def get_session(
        self,
        db: AsyncSession,
        session_id: UUID,
    ) -> ChatSession | None:

        return await db.get(ChatSession, session_id)

    async def list_sessions(
        self,
        db: AsyncSession,
        repository_id: UUID,
    ) -> list[ChatSession]:

        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.repository_id == repository_id)
            .order_by(ChatSession.updated_at.desc())
        )

        return result.scalars().all()

    async def save_message(
        self,
        db: AsyncSession,
        session_id: UUID,
        role: MessageRole,
        content: str,
    ) -> ChatMessage:

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )

        db.add(message)

        session = await db.get(ChatSession, session_id)

        if session:
            db.add(session)

        await db.commit()
        await db.refresh(message)

        return message

    async def get_history(
        self,
        db: AsyncSession,
        session_id: UUID,
        limit: int = 10,
    ) -> list[dict]:

        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
        )

        messages = result.scalars().all()

        if len(messages) > limit:
            messages = messages[-limit:]

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

    async def rename_session(
        self,
        db: AsyncSession,
        session_id: UUID,
        title: str,
    ):

        session = await db.get(ChatSession, session_id)

        if not session:
            return None

        session.title = title

        await db.commit()
        await db.refresh(session)

        return session

    async def delete_session(
        self,
        db: AsyncSession,
        session_id: UUID,
    ):

        session = await db.get(ChatSession, session_id)

        if not session:
            return False

        await db.delete(session)
        await db.commit()

        return True
