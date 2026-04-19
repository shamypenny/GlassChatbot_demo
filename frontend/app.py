import streamlit as st
import requests
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="ATG研发端AI助手",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4472C4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #5B9BD5;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .source-box {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/test-tube.png", width=80)
    st.title("ATG研发端AI助手")
    st.markdown("---")
    
    page = st.radio(
        "功能导航",
        ["🏠 首页", "💬 智能问答", "📋 配方管理", "🎯 配方推荐"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    **版本**: v1.0.0 Demo
    
    **技术栈**:
    - GLM-4 大模型
    - RAG 检索增强
    - Chroma 向量库
    """)
    
    st.markdown("---")
    st.caption("© 2024 ATG研发端AI助手")

if page == "🏠 首页":
    st.markdown('<h1 class="main-header">🔬 ATG研发端AI助手</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">玻璃材料研发智能化解决方案</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 💬 智能文献问答
        基于RAG技术的知识库问答系统，支持自然语言查询，精准定位相关文献，提供引用溯源。
        """)
        if st.button("开始问答", key="btn_chat", use_container_width=True):
            st.switch_page("pages/1_智能问答.py")
    
    with col2:
        st.markdown("""
        ### 📋 配方数据管理
        管理玻璃配方数据，支持录入、查询、编辑配方，并关联测试数据形成完整的样品档案。
        """)
        if st.button("管理配方", key="btn_recipe", use_container_width=True):
            st.switch_page("pages/2_配方管理.py")
    
    with col3:
        st.markdown("""
        ### 🎯 配方智能推荐
        根据目标性能指标，系统推荐可能满足要求的配方方案，提供置信度评估。
        """)
        if st.button("获取推荐", key="btn_recommend", use_container_width=True):
            st.switch_page("pages/3_配方推荐.py")
    
    st.markdown("---")
    
    st.markdown("### 📊 数据概览")
    
    try:
        response = requests.get(f"{API_BASE}/api/recipes/statistics", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("配方总数", stats.get("total_recipes", 0))
            with col2:
                st.metric("已测试配方", stats.get("status_distribution", {}).get("已测试", 0))
            with col3:
                st.metric("测试记录", stats.get("total_tests", 0))
    except:
        st.info("后端服务未启动，请先运行后端服务")
    
    st.markdown("---")
    
    st.markdown("### 🎯 核心功能")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **解决的问题**:
        - ✅ 文献检索效率低，知识难以复用
        - ✅ 配方数据纸质化，无法追溯
        - ✅ 历史经验难以有效利用
        - ✅ 研发周期长，试错成本高
        """)
    
    with col2:
        st.markdown("""
        **带来的价值**:
        - 📈 文献检索效率提升50%+
        - 📈 配方数据100%数字化
        - 📈 研发周期缩短30%+
        - 📈 知识沉淀与传承
        """)
