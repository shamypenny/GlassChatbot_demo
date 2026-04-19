import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="配方推荐 - ATG研发端AI助手",
    page_icon="🎯",
    layout="wide"
)

st.markdown("# 🎯 配方智能推荐")
st.markdown("根据目标性能指标，系统推荐可能满足要求的配方方案。")

st.markdown("---")

col_input, col_result = st.columns([1, 2])

with col_input:
    st.markdown("### 📝 输入目标性能")
    
    with st.form("recommend_form"):
        st.markdown("请输入目标性能指标（至少填写一项）：")
        
        thermal_expansion = st.number_input(
            "热膨胀系数 (×10⁻⁶/℃)",
            min_value=0.0,
            max_value=20.0,
            value=4.0,
            step=0.1,
            help="目标热膨胀系数，范围通常在3-10"
        )
        
        density = st.number_input(
            "密度 (g/cm³)",
            min_value=2.0,
            max_value=3.0,
            value=2.45,
            step=0.01,
            help="目标密度，范围通常在2.2-2.8"
        )
        
        bending_strength = st.number_input(
            "抗弯强度 (MPa)",
            min_value=0.0,
            max_value=200.0,
            value=80.0,
            step=1.0,
            help="目标抗弯强度，越高越好"
        )
        
        heat_resistance = st.number_input(
            "耐热温度 (℃)",
            min_value=0.0,
            max_value=800.0,
            value=500.0,
            step=10.0,
            help="目标耐热温度，越高越好"
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("🔍 开始推荐", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 使用说明
    
    1. 输入目标性能指标
    2. 点击"开始推荐"按钮
    3. 系统将返回Top-3推荐配方
    4. 查看置信度和预测性能
    
    **注意**：
    - 推荐基于历史数据
    - 置信度越高越可靠
    - 实际效果需实验验证
    """)

with col_result:
    st.markdown("### 📊 推荐结果")
    
    if submitted:
        with st.spinner("正在分析推荐中..."):
            try:
                request_data = {}
                if thermal_expansion:
                    request_data["thermal_expansion"] = thermal_expansion
                if density:
                    request_data["density"] = density
                if bending_strength:
                    request_data["bending_strength"] = bending_strength
                if heat_resistance:
                    request_data["heat_resistance"] = heat_resistance
                
                response = requests.post(
                    f"{API_BASE}/api/recommend",
                    json=request_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    if results:
                        for i, result in enumerate(results, 1):
                            confidence = result.get("confidence", 0)
                            
                            if confidence >= 0.8:
                                badge = "⭐ 强烈推荐"
                                color = "green"
                            elif confidence >= 0.6:
                                badge = "✓ 推荐"
                                color = "blue"
                            else:
                                badge = "○ 可参考"
                                color = "gray"
                            
                            with st.container():
                                st.markdown(f"""
                                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid {color};">
                                    <h4>方案{i} - {result.get('name', '未知配方')} <small style="color: {color};">({badge}, 置信度: {confidence:.0%})</small></h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    st.markdown("**主要成分 (wt%)**")
                                    composition = result.get("composition", {})
                                    
                                    comp_md = ""
                                    for key, value in composition.items():
                                        comp_md += f"- {key}: {value}%\n"
                                    
                                    st.markdown(comp_md)
                                
                                with col_b:
                                    st.markdown("**预测性能**")
                                    properties = result.get("predicted_properties", {})
                                    
                                    prop_md = ""
                                    if "thermal_expansion" in properties:
                                        prop_md += f"- 热膨胀系数: {properties['thermal_expansion']}×10⁻⁶/℃\n"
                                    if "density" in properties:
                                        prop_md += f"- 密度: {properties['density']} g/cm³\n"
                                    if "bending_strength" in properties:
                                        prop_md += f"- 抗弯强度: {properties['bending_strength']} MPa\n"
                                    if "heat_resistance" in properties:
                                        prop_md += f"- 耐热温度: {properties['heat_resistance']}℃\n"
                                    
                                    st.markdown(prop_md)
                                    
                                    st.markdown(f"**历史实验**: {result.get('history_count', 0)}次")
                                
                                if st.button(f"查看配方详情", key=f"detail_{i}"):
                                    st.info(f"配方编号: {result.get('recipe_id')}")
                                
                                st.markdown("---")
                        
                        st.markdown("""
                        <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem;">
                            <strong>💡 温馨提示</strong><br>
                            推荐结果基于历史数据，实际效果需通过实验验证。建议优先选择置信度高的配方方案。
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        st.warning("未找到满足条件的配方，请尝试调整目标性能指标。")
                
                else:
                    st.error(f"推荐失败: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("⚠️ 无法连接到后端服务，请确保后端服务已启动")
                st.code("python -m uvicorn backend.main:app --reload --port 8000")
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
    
    else:
        st.info("👈 请在左侧输入目标性能指标，然后点击"开始推荐"按钮")
        
        st.markdown("""
        ### 📋 推荐示例
        
        **示例1：低膨胀玻璃**
        - 热膨胀系数: 3.5
- 密度: 2.45
        - 抗弯强度: 85
        - 耐热温度: 550
        
        **示例2：高强度玻璃**
        - 热膨胀系数: 4.0
        - 密度: 2.46
        - 抗弯强度: 90
        - 耐热温度: 520
        """)
