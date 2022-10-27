import uvicorn
from fastapi import FastAPI
#from coronavirus import application
from tutorial import app03, app04, app05, app06, app07, app08
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='FastAPI Tutorial and Coronavirus Tracker API Docs',
    description='FastAPI教程 新冠病毒疫情跟踪器API接口文档，项目代码：https://github.com/liaogx/fastapi-tutorial',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错

app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 中间件、CORS、后台任务、测试用例'])
#app.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])

if __name__=='__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)

