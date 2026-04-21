import os

# https://bailian.console.aliyun.com/?tab=model#/api-key
os.environ["OPENAI_API_KEY"] = "sk-247421c217474fee969fc6b5ef2bd8c8"
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
os.environ["OPENAI_MODEL"] = "qwen-max"
os.environ["OPENAI_VISON_MODEL"] = "qwen-vl"

import uvicorn
from fastapi import FastAPI  # type: ignore
from routers.user import router as user_routers
from routers.chat import router as chat_routers
from routers.data import router as data_routers
from routers.stock import router as stock_routers

from api.autostock import app as stock_app

app = FastAPI()


@app.get("/v1/healthy")
def read_healthy():
    pass

# 自定义的服务接口  自定义的模块挂载在一起
app.include_router(user_routers)
app.include_router(chat_routers)
app.include_router(data_routers)
app.include_router(stock_routers)

# 底层stock api 接口。autostock.py定义的是一个完整的FastAPI应用实例（app=FastAPI(...),不是APIRouter）
# 这样设计既可以 1.8000端口 HTTP 前端直接调数据；2.8900端口 MCP工具 Agent对话时调
app.mount("/stock", stock_app) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main_server:app
