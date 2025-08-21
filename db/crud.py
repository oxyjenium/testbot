import asyncpg
import os

pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        user=os.getenv("USER_DB"),
        password=os.getenv("PASSWORD_DB"),
        database=os.getenv("NAME_DB"),
        host=os.getenv("HOST_DB"),
        port=os.getenv("PORT_DB")
    )

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            full_name TEXT,
            date_birth DATE,
            number TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """)
        
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES users(tg_id),
            service TEXT,
            description TEXT,
            technologies TEXT,
            deadline TEXT,
            screenshot TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

async def get_connection():
    global pool
    return pool
