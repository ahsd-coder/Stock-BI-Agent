# 项目背景

现有的商业智能 (BI) 工具和数据分析软件功能强大，但操作复杂，需要专业的知识和技能才能有效使用，不适合快速、临时的查询和分析。用户无法用自然语言直接询问数据问题，而是必须通过复杂的图表配置和公式编写来获取信息。

# 项目目的

1. 不想在本地部署agent，做一个基于分布式部署的股票分析助手。
2. 调用云端mcp服务，也，查询股票可以分析股票。
3. 支持多轮对话，也可以记录历史对话。


# 项目架构

- 模块1：MCP Server，自定义工具，股票查询，其他天气或外部【工具，查询类型】
- 模块2：Fast API后端服务，提供后端的业务逻辑【接口，非工具类型】
  - 查询股票，可以是mcp
  - 用户注册，不推荐是mcp
  - 用户登录，不推荐是mcp
- 模块3：Streamlit实现前端页面

# 文件划分

- `main_mcp.py` - MCP Server 主程序 （模块1）
- `main_server.py` - Fast API Web服务主程序 （模块2）
  
- `./routers/` - FastAPI路由（每个模块fastapi服务）
  - `chat.py` - 聊天路由
  - `stock.py` - 股票数据路由
  - `user.py` - 用户管理路由
  - `data.py` - 数据管理路由

- `./api/` - API接口模块（底层api、外部api，fastmcp服务）
  - `autostock.py` - 股票数据接口（付费接口）
  - `news.py` - 新闻数据接口
  - `saying.py` - 名言/语录接口
  - `tool.py` - 工具类接口
  
- `./services/` - 业务服务层（具体业务实现代码）
  - `chat.py` - 聊天服务
  - `stock.py` - 股票服务
  - `user.py` - 用户服务
  
- `./models/` - 数据模型
  - `data_models.py` - Pydantic和typing数据模型定义
  - `orm.py` - 关系型数据库关系映射
  
- `REAME.md` - 项目说明文档（注意文件名拼写应为README.md）
- `./agent/` - 智能Agent模块（工作流、openai-agent代码）
  - `stock_agent.py` - 股票分析智能代理
  - `db_agent.py` - 数据库操作代理
  - `csv_agent.py` - CSV文件处理代理
  - `excel_agent.py` - Excel文件处理代理
  - `vison_agent.py` - 视觉分析代理
  - `summary_agent.py` - 摘要生成代理
  
- ./demo - Streamlit 前端页面 （模块3）
  - ./demo/chat/` - 聊天功能演示
    - `chat.py` - 聊天主程序
    - `chat_list.py` - 聊天列表管理
  - `./demo/stock/` - 股票功能演示
    - `stock_info.py` - 股票信息
    - `stock_kline.py` - K线图数据
    - `stock_search.py` - 股票搜索
    - `stock_rank.py` - 股票排名
    - `stock_board.py` - 板块数据
    - `stock_industry.py` - 行业数据
    - `stock_favorite.py` - 收藏功能
    - `stock_min_data.py` - 分钟数据
  - `./demo/user/` - 用户管理演示
    - `user_login.py` - 用户登录
    - `user_register.py` - 用户注册
    - `user_info.py` - 用户信息
    - `user_list.py` - 用户列表
    - `user_delete.py` - 用户删除
    - `user_reset.py` - 密码重置
  - `./demo/mcp/` - MCP协议演示
    - `mcp_list.py` - MCP列表
    - `mcp_debug.py` - MCP调试
  - `./demo/data/` - 数据管理演示
    - `data_list.py` - 数据列表
    - `data_manage.py` - 数据管理
  
- `./templates/` - 模板文件
  - `chat_start_system_prompt.jinjia2` - 聊天系统提示模板（Jinja2格式）

- `./assert/` - 资源文件
  - `conversations.db*` - 对话记录数据库
  - `sever.db` - 服务器数据库
  - `chat-message` - 聊天消息数据
- `./test/` - 单元测试文件
  - `test_agent.py` - 代理测试
  - `test_autostock.py` - 自动化股票测试
  - `test_jinja2_template.py` - 模板测试
  - `test_mcp.py` - MCP协议测试

# 开发过程
## 模块1: mcp 服务，2-3天

```code
mcp = FastMCP.from_fastapi(app=app) # 导入fastapi 服务

async def setup():
    await mcp.import_server(news_mcp, prefix="") # 定义mcp 服务
    await mcp.import_server(saying_mcp, prefix="")
    await mcp.import_server(tool_mcp, prefix="")
```

mcp server 非常灵活，可以来源比较多样；
- @mcp.tool： 在函数加注解，定义为mcp 服务 -> 通过mcp client调用
- 从fastapi导入（灵活）： 从fast api 导入为mcp 服务 -> 通过http、mcp client调用
- 从外部 openapi json 导入：导入外部其他的程序api json


## 模块2: Fast API 后端开发，3-4天

```code
# 前后端交互的http接口，与业务相关的api
# http://127.0.0.1:8000/docs#/
app.include_router(user_routers)
app.include_router(chat_routers)
app.include_router(data_routers)
app.include_router(stock_routers)

# 底层的股票http接口，底层相关的api
# http://127.0.0.1:8000/stock/docs#/
app.mount("/stock", stock_app)
```

- 底层数据库，models
- 业务代码，services
- fastapi路由，routers

## 模块3: Streamlit 前端开发，1-2天

> Streamlit 不是强制的，但是推荐掌握一下。帮助理解前后端如何交互。

## 开发过程
- 模块进行划分：用户管理模块、股票管理模块、对话模块（主要模块）
- 对话模块：
  - 历史对话记录，对话切换
  - 大模型历史状态管理的过程
    - AdvancedSQLiteSession：主要依赖openai-agent的服务，不是很透明，比较简单
    - 自己实现：历史对话也输入给大模型，基于历史输入继续对话（限制最后10条历史对话作为输入，如果对话太长大模型忘记最开始信息）
  - 对话：

## 项目启动
- 1.python main_mcp.py
- 2.python main_server.py
- 3.streamlit run demo/streamlit_demo.py
- 注：本人也尝试在阿里云服务器端进行部署，可进行公网访问。

## 相关问题
- 1. 什么是前后端分离？
- 答：前后端分离就是：前端和后端是两个独立程序，通过API通信，各自独立开发、部署、运行。在这个项目中具体体现为：
  ·后端——main_server.py，端口8000。
    ·Fast API服务，只负责提供数据接口（REST API）
    ·通过routers暴露 /user、/chat、/data、/stock 等API端点
    ·不关心页面怎么渲染，只返回JSON数据
       ——main_mcp.py，端口8900.
    ·跑MCP/SSE服务，供Agent对话时调用工具，但走的是不同的协议（SSE而非HTTP REST）
  ·前端——demo目录下的streamlit页面
    ·独立的Streamlit应用，负责UI展示和用户交互
    ·通过requests库调用后端API获取数据，例如 requests.post("http://127.0.0.1:8000/user/login")
    ·不关心数据从哪来、怎么处理、只管展示

- 2.历史对话如何存储，以及如何将历史对话作为大模型的下一次输入？
- 答：在开发大模型应用（如 Chatbot）时，由于 LLM 本身是无状态（Stateless）的，它不会记得你上一句话说了什么。

[
  {"role": "user", "content": "你好，请问今天天气怎么样？"},
  {"role": "assistant", "content": "今天天气晴朗，温度约为 25°C。"},
  {"role": "user", "content": "那我适合去爬山吗？"}
]

- 只保留最近的 K 轮对话。当新对话进入时，移除最旧的一条。这能保证模型始终记得最近的语境，同时控制成本。【滑动窗口——丢弃最旧的消息，保留最近的N条】
- 当对话过长时，调用大模型对之前的历史做一个“简短摘要”。【摘要压缩——用LLM把旧对话总结成一段话，大幅缩减Token】
- 从历史对话中检索到相关的信息 + 最近的K条 作为历史。【重要性过滤——只保留关键信息（用户指令、重要结论），丢弃过程细节】
