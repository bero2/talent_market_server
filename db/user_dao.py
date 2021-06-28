import asyncio
from typing import *

import aiomysql
import pandas as pd

from db.db_connection import connect
from models.user import User
from utils.parsers import ParseUser


def fetch_user_info(db_conf: Mapping[str, str], user_id: str):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _fetch_user_info(loop: asyncio.AbstractEventLoop, user_id: str) -> Optional[pd.DataFrame]:
        pool: aiomysql.Pool = await connect(db_conf['host'], int(db_conf['port']), db_conf['db'], db_conf['user_svc'], db_conf['pw'], loop=loop)

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'''
                    select 
                        user_id
                        , user_nm
                        , user_pw
                        , user_email
                        , phone_number
                        , user_auth
                        , use_yn
                        , del_yn
                    from tm.tm_user_info
                    where
                        user_id = "{user_id}"
                ''')
                result = await cur.fetchall()

                if len(result) == 0:
                    return None
                else:
                    df_user = pd.DataFrame(
                        data=result,
                        columns=[
                            'user_id',
                            'user_nm',
                            'user_pw',
                            'user_email',
                            'phone_number',
                            'user_auth',
                            'use_yn',
                            'del_yn'
                        ]
                    )
                    user = ParseUser()
                    return user.parse_user(df_user)

    user_info = loop.run_until_complete(_fetch_user_info(loop, user_id))
    loop.close()

    return user_info


def fetch_all_user_info(db_conf: Mapping[str, str]):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _fetch_all_user_info(loop: asyncio.AbstractEventLoop) -> Optional[pd.DataFrame]:
        pool: aiomysql.Pool = await connect(db_conf['host'], int(db_conf['port']), db_conf['db'], db_conf['user_svc'], db_conf['pw'], loop=loop)

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'''
                    select 
                        user_id
                        , user_nm
                        , user_pw
                        , user_email
                        , phone_number
                        , user_auth
                    from tm.tm_user_info
                    where
                        use_yn = 'Y'
                        and del_yn = 'N'
                ''')
                result = await cur.fetchall()

                if len(result) == 0:
                    return None
                else:
                    return pd.DataFrame(
                        data=result,
                        columns=[
                            'user_id',
                            'user_nm',
                            'user_pw',
                            'user_email',
                            'phone_number',
                            'user_auth'
                        ]
                    )

    user_info = loop.run_until_complete(_fetch_all_user_info(loop))
    loop.close()

    return user_info


def insert_user_info(db_conf: Mapping[str, str], user: User):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _insert_user_info(loop: asyncio.AbstractEventLoop, user: User) -> Optional[pd.DataFrame]:
        pool: aiomysql.Pool = await connect(db_conf['host'], int(db_conf['port']), db_conf['db'], db_conf['user_svc'], db_conf['pw'], loop=loop)

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'''
                    insert into tm.tm_user_info (user_id, user_nm, user_pw, user_email, phone_number, user_auth)
                    values ("{user.user_id}", "{user.user_nm}", "{user.user_pw_hash}", "{user.user_email}", "{user.phone_number}", "{user.user_auth}")
                ''')
                await conn.commit()

    loop.run_until_complete(_insert_user_info(loop, user))
    loop.close()


# TODO DB 사용자 정보 업데이트
def update_user_info(db_conf: Mapping[str, str], user: User):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _update_user_info(loop: asyncio.AbstractEventLoop, user: User) -> Optional[pd.DataFrame]:
        pool: aiomysql.Pool = await connect(db_conf['host'], int(db_conf['port']), db_conf['db'], db_conf['user_svc'], db_conf['pw'], loop=loop)
        pass

    loop.run_until_complete(_update_user_info(loop, user))
    loop.close()


def delete_user_info(db_conf: Mapping[str, str], user_id: str):
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _delete_user_info(loop: asyncio.AbstractEventLoop, user_id: str) -> Optional[pd.DataFrame]:
        pool: aiomysql.Pool = await connect(db_conf['host'], int(db_conf['port']), db_conf['db'], db_conf['user_svc'], db_conf['pw'], loop=loop)

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'''
                    update tm.tm_user_info
                    set use_yn = 'N', del_yn = 'Y'
                    where
                        user_id = "{user_id}"
                ''')
                await conn.commit()

    loop.run_until_complete(_delete_user_info(loop, user_id))
    loop.close()


