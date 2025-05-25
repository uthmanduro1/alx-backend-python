#!/usr/bin/env python3
"""
Run multiple SQLite queries concurrently using aiosqlite and asyncio.gather
"""

import asyncio
import aiosqlite

DB_NAME = "users.db"

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[ALL USERS]")
            print(users)
            return users

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("[USERS > 40]")
            print(older_users)
            return older_users

# Function to run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run it
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
