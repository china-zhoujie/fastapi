#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app06 = APIRouter()

"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer"""