import streamlit as st

from ui import apply_theme


st.set_page_config(
    page_title="Mindshield 心盾｜香港硕士求职安全",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()

st.session_state.setdefault("api_key", "")
st.session_state.setdefault("model_name", "deepseek-flash")
st.session_state.setdefault("report_language", "简体中文")

with st.sidebar:
    st.markdown("## 🛡️ Mindshield 设置")
    st.text_input(
        "DeepSeek API Key",
        type="password",
        key="api_key",
        help="密钥只用于请求 DeepSeek。不要写入代码或上传 GitHub。",
    )
    st.selectbox(
        "AI 模型",
        ["deepseek-flash", "deepseek-v4-pro"],
        key="model_name",
    )
    st.selectbox(
        "报告语言",
        ["简体中文", "繁體中文", "English", "跟随输入语言"],
        key="report_language",
    )
    st.divider()
    st.caption("上传前请遮盖身份证、护照、银行卡、验证码和家庭地址。")
    st.caption("AI 结果用于风险筛查，不是法律定性。")

st.markdown(
    """
    <div class="ms-brandbar">
      <span class="ms-brand-icon">🛡️</span>
      <span><b>MINDSHIELD</b> <small>心盾 · AI Career Guard</small></span>
      <span class="ms-system-status"><i></i> SYSTEM ONLINE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

pages = [
    st.Page(
        "pages/home.py",
        title="Home 首页",
        icon=":material/home:",
        url_path="home",
        default=True,
    ),
    st.Page(
        "pages/verify.py",
        title="Verify AI 核验",
        icon=":material/verified_user:",
        url_path="verify",
    ),
    st.Page(
        "pages/report.py",
        title="Report 风险报告",
        icon=":material/assessment:",
        url_path="report",
    ),
    st.Page(
        "pages/library.py",
        title="Tactics 反诈知识库",
        icon=":material/library_books:",
        url_path="tactics",
    ),
    st.Page(
        "pages/faq.py",
        title="FAQ 使用帮助",
        icon=":material/help:",
        url_path="faq",
    ),
]

current_page = st.navigation(pages, position="top")
current_page.run()

