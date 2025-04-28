from redis.asyncio import Redis
from typing import List
from core.config import settings
import json

class RedisService:
    def __init__(self):
        self.redis = Redis.from_url(settings.redis, decode_responses=True)

    def _questions_key(self, session_id: str) -> str:
        return f"session:{session_id}:questions"

    def _session_data_key(self, session_id: str) -> str:
        return f"session:{session_id}:data"

    async def cache_questions(self, session_id: str, questions: List[dict]):
        key = self._questions_key(session_id)
        questions_json = [json.dumps(q) for q in questions]
        await self.redis.rpush(key, *questions_json)

    async def get_question(self, session_id: str) -> dict | None:
        key = self._questions_key(session_id)
        question_json = await self.redis.lindex(key, 0)
        if question_json:
            return json.loads(question_json)
        return None

    async def pop_next_question(self, session_id: str) -> dict | None:
        key = self._questions_key(session_id)
        question_json = await self.redis.lpop(key)
        if question_json:
            return json.loads(question_json)
        return None

    async def has_questions_left(self, session_id: str) -> bool:
        key = self._questions_key(session_id)
        length = await self.redis.llen(key)
        return length > 0

    async def delete_questions(self, session_id: str):
        key = self._questions_key(session_id)
        await self.redis.delete(key)


    async def set_current_question(self, session_id: str, question_id: str):
        key = self._session_data_key(session_id)
        await self.redis.hset(key, "current_question_id", question_id)

    async def get_current_question(self, session_id: str) -> str | None:
        key = self._session_data_key(session_id)
        return await self.redis.hget(key, "current_question_id")

    async def clear_current_question(self, session_id: str):
        key = self._session_data_key(session_id)
        await self.redis.hdel(key, "current_question_id")

    async def delete_session_data(self, session_id: str):
        await self.redis.delete(self._questions_key(session_id))
        await self.redis.delete(self._session_data_key(session_id))


redis_service = RedisService()
