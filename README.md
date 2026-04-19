# 玻璃企业研发端AI助手 Demo

玻璃材料研发智能化解决方案 - Demo版本

## 项目简介

玻璃企业研发端AI助手是一个面向玻璃材料研发领域的智能化系统，通过AI技术解决研发流程中的核心痛点，提升研发效率。

## 核心功能

### 💬 智能文献问答
- 基于RAG技术的知识库问答
- 支持自然语言查询
- 提供引用溯源
- 文献检索效率提升50%+

### 📋 配方数据管理
- 配方数字化录入
- 测试数据关联
- 全生命周期追溯
- 配方数据100%可追溯

### 🎯 配方智能推荐
- 输入目标性能指标
- 系统推荐配方方案
- 提供置信度评估
- 研发周期缩短30%+

## 技术栈

| 组件 | 技术 | 说明 |
|-----|------|------|
| LLM | 智谱GLM-4 | 国产大模型，中文能力强 |
| Embedding | BGE-M3 | 中文语义向量模型 |
| 向量库 | Chroma | 轻量级向量数据库 |
| 后端 | FastAPI | 高性能Python Web框架 |
| 前端 | Streamlit | 快速数据应用开发框架 |

## 快速启动

### 方式一：一键启动（推荐）

**Windows:**
```bash
双击运行 start_windows.bat
```

**Linux/Mac:**
```bash
chmod +x start_linux.sh
./start_linux.sh
```

### 方式二：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动后端（终端1）
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 启动前端（终端2）
python -m streamlit run frontend/app.py --server.port 8501
```

### 访问地址

- 前端界面: http://localhost:8501
- API文档: http://localhost:8000/docs

## 项目结构

```
demo/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI入口
│   ├── models/             # 数据模型
│   ├── routers/            # API路由
│   │   ├── chat.py         # 问答接口
│   │   ├── recipe.py       # 配方接口
│   │   └── recommend.py    # 推荐接口
│   └── services/           # 业务服务
│       ├── rag_service.py  # RAG服务
│       ├── recipe_service.py # 配方服务
│       ├── recommend_service.py # 推荐服务
│       └── llm_service.py  # LLM服务
├── frontend/               # 前端代码
│   ├── app.py             # Streamlit入口
│   └── pages/             # 页面组件
│       ├── 1_智能问答.py
│       ├── 2_配方管理.py
│       └── 3_配方推荐.py
├── demo_data/              # 演示数据
│   ├── documents.json      # 文献数据（10篇）
│   ├── recipes.json        # 配方数据（15条）
│   ├── test_results.json   # 测试数据
│   └── demo_questions.json # 演示问题
├── data/                   # 运行时数据
│   └── chroma_db/          # 向量数据库
├── config/                 # 配置文件
│   └── settings.py        # 全局配置
├── docs/                   # 文档
│   ├── 部署指南.md
│   ├── 演示脚本.md
│   ├── PPT大纲.md
│   └── 视频脚本.md
├── requirements.txt        # Python依赖
├── run_demo.py            # 启动脚本
├── start_windows.bat      # Windows启动
├── start_linux.sh         # Linux启动
└── README.md              # 本文件
```

## 配置说明

### API Key配置（可选）

如需使用真实的LLM服务，请配置智谱API Key：

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```
ZHIPU_API_KEY=your-api-key-here
```

> 如不配置API Key，系统将使用模拟回答模式，仍可正常演示。

## 演示数据

### 文献数据
- 10篇玻璃材料相关文献
- 涵盖基础知识、成分影响、工艺参数等

### 配方数据
- 15条模拟配方
- 包含成分配比、熔制制度、测试数据

### 演示问题
- 10个预设问题
- 确保演示效果稳定

## 部署方式

### 本地部署
详见 [docs/部署指南.md](docs/部署指南.md)

### 服务器部署
支持Docker部署和系统服务部署，详见部署指南。

## 演示材料

- [演示脚本](docs/演示脚本.md) - 详细演示流程和话术
- [PPT大纲](docs/PPT大纲.md) - 项目介绍PPT结构
- [视频脚本](docs/视频脚本.md) - 演示视频录制指南

## 注意事项

1. **首次启动**：首次启动会下载Embedding模型，需要几分钟时间
2. **网络要求**：如使用在线LLM服务，需要稳定的网络连接
3. **数据安全**：所有数据存储在本地，不会外传
4. **浏览器兼容**：推荐使用Chrome或Edge浏览器

## 常见问题

### Q: 启动失败，提示端口被占用？
A: 检查8000和8501端口是否被其他程序占用，或修改启动脚本中的端口号。

### Q: Embedding模型下载失败？
A: 模型较大（约2GB），请确保网络稳定。也可以手动下载后放到本地。

### Q: 问答功能无响应？
A: 检查后端服务是否正常启动，访问 http://localhost:8000/docs 确认API可用。

## 版本信息

- 版本: v1.0.0 Demo
- 更新日期: 2025年

## 联系方式

如有问题或建议，请联系项目负责人。

---

*ATG研发端AI助手 - 用AI赋能研发，让数据创造价值*
