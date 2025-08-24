from datetime import date

from db.db import get_connection


async def create_user(tg_id: int, username: str) -> None:
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.fetchrow("""
            INSERT INTO users (tg_id, username)
            VALUES ($1, $2)
            RETURNING id
        """, tg_id, username)



async def update_user_details(tg_id: int, full_name: str, date_birth: date, number: str) -> None:
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE users
            SET full_name = $1,
                date_birth = $2,
                number = $3
            WHERE tg_id = $4
        """, full_name, date_birth, number, tg_id)
        
        
async def check_user_fields(tg_id: int) -> bool:
    pool = await get_connection()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT full_name, date_birth, number
            FROM users
            WHERE tg_id = $1
        """, tg_id)

        if row and all(row.values()):
            return True
        return False
    

import asyncpg
from typing import Optional, List


async def add_application(
    user_id: int,
    service: str,
    description: str,
    technologies: List[str],
    deadline: str,
    screenshot: str
):
    pool = await get_connection()
    async with pool.acquire() as conn:
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
        
        
async def get_last_application_by_user(user_id: int) -> Optional[dict]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, service, description, technologies, deadline, screenshot, created_at
            FROM requests
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT 1
        """, user_id)

        return dict(row) if row else None
    

async def get_user(user_id: int) -> Optional[dict]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, tg_id, username, full_name, date_birth, number
            FROM users
            WHERE tg_id = $1
        """, user_id)

        return dict(row) if row else None
    

async def get_users_list(offset: int = 0, limit: int = 5) -> List[dict]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT tg_id, username
            FROM users
            ORDER BY id
            LIMIT $1 OFFSET $2
        """, limit, offset)
        return [dict(row) for row in rows]
    

async def get_users_count():
    pool = await get_connection()
    async with pool.acquire() as conn:
        count = await conn.fetchval("SELECT COUNT(*) FROM users")
        return count
    

async def get_applications_list(offset: int = 0, limit: int = 5) -> List[dict]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, user_id, service, description, technologies, deadline, screenshot, created_at
            FROM requests
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """, limit, offset)
        return [dict(row) for row in rows]
    

async def get_applications_count() -> int:
    pool = await get_connection()
    async with pool.acquire() as conn:
        count = await conn.fetchval("SELECT COUNT(*) FROM requests")
        return count
    

async def get_application_by_id(application_id: int) -> Optional[dict]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, user_id, service, description, technologies, deadline, screenshot, created_at
            FROM requests
            WHERE id = $1
        """, application_id)

        return dict(row) if row else None
    
    
async def get_all_user() -> Optional[List[dict]]:
    pool = await get_connection()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT tg_id, username, full_name, date_birth, number
            FROM users
        """)
        return [dict(row) for row in rows] if rows else []
