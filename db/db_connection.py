import asyncio

import aiomysql


async def connect(host: str, port: int, db: str, user: str, password: str, loop: asyncio.AbstractEventLoop) -> aiomysql.Pool:
    return await aiomysql.create_pool(
        pool_recycle=600,
        host=host,
        port=port,
        db=db,
        user=user,
        password=password,
        loop=loop,
        charset='utf8',
        use_unicode=True
    )
