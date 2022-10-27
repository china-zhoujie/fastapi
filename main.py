import uvicorn
import json
from typing import Union, Optional, List
from fastapi import FastAPI, Query, Path, Cookie
from pydantic import BaseModel

app=FastAPI()

@app.get("/")
async def read_root():
    return {"hello":" word"}

    
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/post/{name_id}")
async def read_name(name_id: int, q: Union[str, None] = None):
    return {"name_id":name_id, "q": q}
    
@app.get("/items1/{item_id}")
async def read_item1(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
    
#请求体
class header_to(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[str] = None
    
@app.post("/header/{city}")
async def get_header(city: str, he: header_to):
    return {"city":city,"he_name":he.name,"he_description":he.description,"he_price":he.price,"he_tax":he.tax}
    


#查询参数和字符串校验,...表示忽略必填项
@app.get("/items2/")
async def read_items2(q: Optional[List[str]] = Query(...,max_length=50,title="Query string",regex="^baidu.com$",deprecated=True)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#alias别名
@app.get("/items3/")
async def read_items3(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
    
#路径参数和数值效验

@app.get("/items4/{item_id}")
async def read_items4(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items5/{item_id}")
async def update_item5(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


#导入cookie
@app.get("/items6/")
async def read_items6(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

    
if __name__=='__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000,debug=True,reload=True)
