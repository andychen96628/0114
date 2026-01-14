import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 設定頁面基礎 ---
st.set_page_config(
    page_title="針安心 NeedleGuard",
    page_icon="🛡️",
    layout="centered"
)

# --- 2. 初始化變數 (Session State) ---
# Streamlit 每次點擊按鈕都會重跑程式，所以必須用 session_state 記住數字
if 'needles_in' not in st.session_state:
    st.session_state.needles_in = 0
if 'needles_out' not in st.session_state:
    st.session_state.needles_out = 0
if 'history' not in st.session_state:
    st.session_state.history = []  # 暫存歷史紀錄

# --- 3. 定義功能函數 ---
def reset_session():
    """結案並重置"""
    # 儲存紀錄
    record = {
        "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "施針數": st.session_state.needles_in,
        "拔針數": st.session_state.needles_out,
        "狀態": "核對無誤"
    }
    st.session_state.history.insert(0, record) # 新的排前面
    
    # 歸零
    st.session_state.needles_in = 0
    st.session_state.needles_out = 0
    st.success("療程結束，紀錄已儲存！")

# --- 4. UI 介面設計 ---
st.title("🛡️ 針安心 (NeedleGuard)")
st.caption("中醫針灸計數防呆系統 - Web MVP")

# 使用 Tabs 分頁切換模式
tab1, tab2, tab3 = st.tabs(["📌 施針模式", "✅ 拔針核對", "📜 歷史紀錄"])

# === Tab 1: 施針模式 ===
with tab1:
    st.header("施針計數")
    
    # 大大的數字顯示
    st.metric(label="目前施針總數 (IN)", value=st.session_state.needles_in)
    
    # 超大按鈕 (Streamlit 預設按鈕較小，這通常夠用)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("➕ 加一針", type="primary", use_container_width=True):
            st.session_state.needles_in += 1
            st.rerun() # 強制刷新畫面
    with col2:
        if st.button("➖ 修改 (減針)", use_container_width=True):
            if st.session_state.needles_in > 0:
                st.session_state.needles_in -= 1
                st.rerun()

# === Tab 2: 拔針核對 ===
with tab2:
    st.header("拔針與結案")
    
    # 數據對比
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("已施針 (IN)", st.session_state.needles_in)
    with col_b:
        st.metric("已拔針 (OUT)", st.session_state.needles_out)
    
    # 計算差異
    remaining = st.session_state.needles_in - st.session_state.needles_out
    
    if remaining > 0:
        st.error(f"⚠️ 警告：尚有 {remaining} 支針未拔除！")
        bg_color = "red"
    elif remaining < 0:
        st.warning("⚠️ 異常：拔針數大於施針數，請確認！")
    else:
        if st.session_state.needles_in > 0:
            st.success("✅ 安全：數量相符，可以結案。")
        else:
            st.info("尚無數據")

    st.divider()
    
    # 拔針按鈕
    if st.button("📤 拔出一針", use_container_width=True):
        st.session_state.needles_out += 1
        st.rerun()

    st.divider()

    # 結案按鈕 (防呆邏輯)
    can_finish = (st.session_state.needles_in == st.session_state.needles_out) and (st.session_state.needles_in > 0)
    
    if st.button("長按結束療程 (模擬)", disabled=not can_finish, type="primary", use_container_width=True):
        reset_session()
        st.rerun()

# === Tab 3: 歷史紀錄 ===
with tab3:
    st.header("施針日誌")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.text("暫無紀錄")
