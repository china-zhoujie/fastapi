#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from typing import Optional

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Header

app05 = APIRouter()

"""Dependencies 创建、导入和声明依赖"""

async def common_params(q: Optional[str] = None, page: int = 1, limit: int=100):
    return {"q":q,"page":page,"limit":limit}
    
@app05.get('/dependency01')
async def dependency01(commos: dict=Depends(common_params)):#函数作为依赖项
    return commos
    
@app05.get('/dependency02')
def dependency02(commos: dict=Depends(common_params)): # 可以在async def中调用def依赖，也可以在def中导入async def依赖
    return commos
    

"""Classes as Dependencies 类作为依赖项"""

fake_item_db=[{"item_name":"Foo"},{"item_name":"Ztp"},{"item_name":"Eto"}]

class CommonQueryParams:
    def __init__(self,q: Optional[str] = None, page: int =0, limit: int =100):
        self.q = q
        self.page = page
        self.limit = limit
        
@app05.get("/classes_as_dependencies")
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()):
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q":commons.q})
    items = fake_item_db[commons.page:commons.page+commons.limit]
    response.update({"items":items})
    return response
    
        
"""Sub-dependencies 子依赖"""
def query(q: Optional[str]):
    return q

def sub_query(q: Optional[str] = Depends(query),last_query: Optional[str] = None):
    if not q:
        return last_query
    return q
    
@app05.get("/sub_dependency")
async def sub_dependency(final_query: Optional[str] = Depends(sub_query,use_cache=True)):
    """use_cache默认是True, 表示当多个依赖有一个共同的子依赖时，每次request请求只会调用子依赖一次，多次调用将从缓存中获取"""
    return {"sub_dependency":final_query}
    
    
"""Dependencies in path operation decorators 路径操作装饰器中的多依赖"""

async def verify_token(x_token: str=Header(...)):
    """没有返回值的子依赖"""
    if x_token != "fake-super-secret-token":
        return HTTPException(status_code=400,detail="X-key header invalid")
        
async def verify_key(x_key: str=Header(...)):
    """有返回值的子依赖，但是返回值不会被调用"""
    if x_key != "fake-super-secret-token":
        return HTTPException(status_code=400,detail="X-key header invalid")
    return x_key
    
@app05.get("/dependency_in_path_operation", dependencies=[Depends(verify_token), Depends(verify_key)])  # 这时候不是在函数参数中调用依赖，而是在路径操作中
async def dependency_in_path_operation():
    return [{"user": "user01"}, {"user": "user02"}]
    
"""Global Dependencies 全局依赖"""

# app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])