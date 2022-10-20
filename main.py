import uvicorn
import json
from typing import Union, Optional, List
from fastapi import FastAPI, Query

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
    
from typing import Optional

from fastapi import FastAPI

app = FastAPI()

#查询参数和字符串校验,...表示忽略必填项
@app.get("/items2/")
async def read_items2(q: Optional[List[str]] = Query(...,max_length=50,title="Query string",regex="^baidu.com$",deprecated=True)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
    
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()

#alias别名
@app.get("/items3/")
async def read_items3(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
    
#路径参数和数值效验
from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items4/{item_id}")
async def read_items4(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



    
if __name__=='__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
