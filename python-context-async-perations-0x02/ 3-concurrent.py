import asyncio
import aiosqlite

# 1️⃣ Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All Users:")
            for row in results:
                print(row)
            return results

# 2️⃣ Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for row in results:
                print(row)
            return results

# 3️⃣ Async function to run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# 4️⃣ Run the concurrent fetch
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
