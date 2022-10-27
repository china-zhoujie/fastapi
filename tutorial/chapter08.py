#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

app08 = APIRouter()

"""【见run.py】Middleware 中间件"""

# 注：带yield的依赖的退出部分的代码 和 后台任务 会在中间件之后运行

"""【见run.py】CORS (Cross-Origin Resource Sharing) 跨源资源共享"""

# 域的概念：协议+域名+端口

"""Background Tasks 后台任务"""