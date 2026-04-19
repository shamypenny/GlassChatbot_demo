import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="配方管理 - ATG研发端AI助手",
    page_icon="📋",
    layout="wide"
)

st.markdown("# 📋 配方数据管理")
st.markdown("管理玻璃配方数据，支持录入、查询、编辑配方，并关联测试数据。")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 配方列表", "➕ 新增配方", "📊 数据统计"])

with tab1:
    col_search, col_filter, col_refresh = st.columns([3, 2, 1])
    
    with col_search:
        search_keyword = st.text_input("搜索", placeholder="输入配方名称或编号...", label_visibility="collapsed")
    
    with col_filter:
        status_filter = st.selectbox("状态筛选", ["全部", "已测试", "实验中", "待测试"], label_visibility="collapsed")
    
    with col_refresh:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()
    
    try:
        params = {}
        if search_keyword:
            params["keyword"] = search_keyword
        if status_filter != "全部":
            params["status"] = status_filter
        
        response = requests.get(f"{API_BASE}/api/recipes", params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            recipes = data.get("recipes", [])
            
            if recipes:
                for recipe in recipes:
                    with st.expander(f"**{recipe['recipe_id']}** - {recipe['name']} ({recipe['status']})", expanded=False):
                        col_info, col_comp = st.columns([1, 1])
                        
                        with col_info:
                            st.markdown("#### 基本信息")
                            st.markdown(f"""
                            - **配方编号**: {recipe['recipe_id']}
                            - **配方名称**: {recipe['name']}
                            - **创建日期**: {recipe['created_at']}
                            - **创建人**: {recipe['created_by']}
                            - **状态**: {recipe['status']}
                            - **备注**: {recipe.get('notes', '-')}
                            """)
                            
                            st.markdown("#### 熔制制度")
                            process = recipe.get('process_params', {})
                            st.markdown(f"""
                            - **熔制温度**: {process.get('melting_temp', '-')}℃
                            - **保温时间**: {process.get('holding_time', '-')}h
                            - **退火温度**: {process.get('annealing_temp', '-')}℃
                            """)
                        
                        with col_comp:
                            st.markdown("#### 成分配比 (wt%)")
                            composition = recipe.get('composition', {})
                            
                            comp_data = {
                                "成分": ["SiO₂", "Al₂O₃", "Na₂O", "K₂O", "CaO", "MgO", "其他"],
                                "含量(%)": [
                                    composition.get('SiO2', 0),
                                    composition.get('Al2O3', 0),
                                    composition.get('Na2O', 0),
                                    composition.get('K2O', 0),
                                    composition.get('CaO', 0),
                                    composition.get('MgO', 0),
                                    composition.get('Others', 0)
                                ]
                            }
                            
                            df = pd.DataFrame(comp_data)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        test_results = recipe.get('test_results', [])
                        if test_results:
                            st.markdown("#### 关联测试数据")
                            
                            for test in test_results:
                                st.markdown(f"**测试日期**: {test['test_date']}")
                                
                                test_items = test.get('test_items', [])
                                if test_items:
                                    test_df = pd.DataFrame(test_items)
                                    st.dataframe(test_df, use_container_width=True, hide_index=True)
                        else:
                            st.info("暂无测试数据")
            else:
                st.info("暂无配方数据")
        
        else:
            st.error(f"获取数据失败: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        st.error("⚠️ 无法连接到后端服务，请确保后端服务已启动")
        st.code("python -m uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        st.error(f"发生错误: {str(e)}")

with tab2:
    st.markdown("### 新增配方")
    
    with st.form("recipe_form"):
        col_left, col_right = st.columns(2)
        
        with col_left:
            name = st.text_input("配方名称*", placeholder="例如：高铝硅酸盐-01")
            created_by = st.text_input("创建人*", placeholder="例如：张工")
            notes = st.text_area("备注", placeholder="配方说明...")
            
            st.markdown("#### 熔制制度")
            melting_temp = st.number_input("熔制温度 (℃)", min_value=1200, max_value=1800, value=1600)
            holding_time = st.number_input("保温时间 (h)", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
            annealing_temp = st.number_input("退火温度 (℃)", min_value=400, max_value=700, value=550)
        
        with col_right:
            st.markdown("#### 成分配比 (wt%)")
            
            total = st.session_state.get("comp_total", 100)
            
            SiO2 = st.number_input("SiO₂", min_value=0.0, max_value=100.0, value=60.0, step=0.5)
            Al2O3 = st.number_input("Al₂O₃", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
            Na2O = st.number_input("Na₂O", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
            K2O = st.number_input("K₂O", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
            CaO = st.number_input("CaO", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
            MgO = st.number_input("MgO", min_value=0.0, max_value=100.0, value=3.0, step=0.5)
            Others = st.number_input("其他", min_value=0.0, max_value=100.0, value=2.0, step=0.5)
            
            total = SiO2 + Al2O3 + Na2O + K2O + CaO + MgO + Others
            
            if abs(total - 100) > 0.1:
                st.warning(f"成分总和: {total:.1f}% (应为100%)")
            else:
                st.success(f"成分总和: {total:.1f}% ✓")
        
        submitted = st.form_submit_button("提交配方", use_container_width=True)
        
        if submitted:
            if not name or not created_by:
                st.error("请填写必填项（配方名称、创建人）")
            elif abs(total - 100) > 0.1:
                st.error("成分总和必须为100%")
            else:
                recipe_data = {
                    "name": name,
                    "created_by": created_by,
                    "notes": notes,
                    "composition": {
                        "SiO2": SiO2,
                        "Al2O3": Al2O3,
                        "Na2O": Na2O,
                        "K2O": K2O,
                        "CaO": CaO,
                        "MgO": MgO,
                        "Others": Others
                    },
                    "process_params": {
                        "melting_temp": melting_temp,
                        "holding_time": holding_time,
                        "annealing_temp": annealing_temp
                    }
                }
                
                try:
                    response = requests.post(f"{API_BASE}/api/recipes", json=recipe_data, timeout=5)
                    
                    if response.status_code == 200:
                        st.success("配方创建成功！")
                        st.json(response.json())
                    else:
                        st.error(f"创建失败: {response.status_code}")
                
                except Exception as e:
                    st.error(f"发生错误: {str(e)}")

with tab3:
    st.markdown("### 数据统计")
    
    try:
        response = requests.get(f"{API_BASE}/api/recipes/statistics", timeout=5)
        
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("配方总数", stats.get("total_recipes", 0))
            
            with col2:
                st.metric("测试记录", stats.get("total_tests", 0))
            
            with col3:
                tested = stats.get("status_distribution", {}).get("已测试", 0)
                total = stats.get("total_recipes", 1)
                st.metric("测试覆盖率", f"{tested/total*100:.1f}%")
            
            st.markdown("#### 状态分布")
            status_dist = stats.get("status_distribution", {})
            
            if status_dist:
                import plotly.express as px
                
                fig = px.pie(
                    values=list(status_dist.values()),
                    names=list(status_dist.keys()),
                    title="配方状态分布",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error(f"获取统计数据失败: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        st.error("⚠️ 无法连接到后端服务")
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
