#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from typing import Optional

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header

app05 = APIRouter()

"""Dependencies 创建、导入和声明依赖"""