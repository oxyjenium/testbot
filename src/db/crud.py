from datetime import date
from typing import Optional, List
from asyncpg.pool import Pool


class UserDB:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def create_user(self, tg_id: int, username: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.fetchrow("""
                INSERT INTO users (tg_id, username)
                VALUES ($1, $2)
                RETURNING id
            """, tg_id, username)

    async def update_user_details(self, tg_id: int, full_name: str, date_birth: date, number: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET full_name = $1,
                    date_birth = $2,
                    number = $3
                WHERE tg_id = $4
            """, full_name, date_birth, number, tg_id)
    
    async def check_user_fields(self, tg_id: int) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT full_name, date_birth, number
                FROM users
                WHERE tg_id = $1
            """, tg_id)
            return bool(row and all(row.values()))

    async def get_user(self, user_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, tg_id, username, full_name, date_birth, number
                FROM users
                WHERE tg_id = $1
            """, user_id)
            return dict(row) if row else None

    async def get_users_list(self, offset: int = 0, limit: int = 5) -> List[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT tg_id, username
                FROM users
                ORDER BY id
                LIMIT $1 OFFSET $2
            """, limit, offset)
            return [dict(row) for row in rows]

    async def get_users_count(self) -> int:
        async with self.pool.acquire() as conn:
            count = await conn.fetchval("SELECT COUNT(*) FROM users")
            return count

    async def get_all_users(self) -> List[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT tg_id, username, full_name, date_birth, number
                FROM users
            """)
            return [dict(row) for row in rows]
    

class ApplicationDB:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def add_application(
        self,
        user_id: int,
        service: str,
        description: str,
        technologies: List[str],
        deadline: str,
        screenshot: str
    ) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO requests (user_id, service, description, technologies, deadline, screenshot)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                user_id,
                service,
                description,
                ", ".join(technologies),
                deadline,
                screenshot
            )
            
    async def get_last_application_by_user(self, user_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, service, description, technologies, deadline, screenshot, created_at
                FROM requests
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT 1
            """, user_id)
            return dict(row) if row else None

    async def get_applications_list(self, offset: int = 0, limit: int = 5) -> List[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, user_id, service, description, technologies, deadline, screenshot, created_at
                FROM requests
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
            """, limit, offset)
            return [dict(row) for row in rows]

    async def get_applications_count(self) -> int:
        async with self.pool.acquire() as conn:
            count = await conn.fetchval("SELECT COUNT(*) FROM requests")
            return count

    async def get_application_by_id(self, application_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT id, user_id, service, description, technologies, deadline, screenshot, created_at
                FROM requests
                WHERE id = $1
            """, application_id)
            return dict(row) if row else None
