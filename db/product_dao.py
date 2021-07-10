import asyncio
from typing import *

import aiomysql
import pandas as pd

from db.db_connection import connect

""" 상품 관련 기능 기능
    1. 상품 등록, 수정, 삭제
    2. 재고관리
    3. 장바구니
    6. 배송관리
    7. 매출 통계
"""