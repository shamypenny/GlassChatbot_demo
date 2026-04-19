import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="智能问答 - ATG研发端AI助手",
    page_icon="💬",
    layout="wide"
)

st.markdown("# 💬 智能文献问答")
st.markdown("基于RAG技术的知识库问答系统，支持自然语言查询玻璃材料相关问题。")

st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "demo_questions" not in st.session_state:
    st.session_state.demo_questions = [
        "高铝硅酸盐玻璃的热膨胀系数是多少？",
        "如何降低玻璃的热膨胀系数？",
        "Al₂O₃对玻璃性能有什么影响？",
        "玻璃的熔制温度一般是多少？",
        "什么是玻璃的退火？",
        "玻璃密度与成分的关系？",
        "如何提高玻璃的抗弯强度？",
        "玻璃的耐热性能如何评估？",
        "碱金属氧化物对玻璃的影响？",
        "玻璃的化学稳定性如何提高？"
    ]

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📝 示例问题")
    st.markdown("点击下方问题快速体验：")
    
    for i, question in enumerate(st.session_state.demo_questions[:5]):
        if st.button(f"❓ {question}", key=f"demo_q_{i}", use_container_width=True):
            st.session_state.current_question = question

with col1:
    st.markdown("### 🗨️ 对话区域")
    
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 您：</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 AI助手：</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                if "sources" in msg and msg["sources"]:
                    with st.expander("📚 查看引用来源"):
                        for j, source in enumerate(msg["sources"], 1):
                            st.markdown(f"""
                            **[{j}] {source['source']}**
                            
                            {source['content']}
                            
                            ---
                            """)
    
    st.markdown("---")
    
    current_q = st.session_state.get("current_question", "")
    
    with st.form("chat_form", clear_on_submit=True):
        col_a, col_b = st.columns([4, 1])
        
        with col_a:
            question = st.text_input(
                "请输入您的问题",
                value=current_q,
                placeholder="例如：高铝硅酸盐玻璃的热膨胀系数是多少？",
                label_visibility="collapsed"
            )
        
        with col_b:
            submitted = st.form_submit_button("发送", use_container_width=True)
        
        if submitted and question:
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            
            with st.spinner("正在思考中..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/api/chat/query",
                        json={"question": question},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("answer", "抱歉，未能获取答案")
                        sources = result.get("sources", [])
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        })
                    else:
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"抱歉，服务出现错误：{response.status_code}"
                        })
                
                except requests.exceptions.ConnectionError:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "⚠️ 无法连接到后端服务，请确保后端服务已启动。\n\n启动方式：在demo目录下运行 `python -m uvicorn backend.main:app --reload --port 8000`"
                    })
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"⚠️ 发生错误：{str(e)}"
                    })
            
            st.session_state.current_question = ""
            st.rerun()
    
    col_clear, col_feedback = st.columns(2)
    with col_clear:
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_feedback:
        st.markdown("💡 回答有帮助吗？点击 👍 或 👎 进行反馈")
