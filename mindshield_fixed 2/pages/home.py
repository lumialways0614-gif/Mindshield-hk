"""Mindshield landing page."""

from __future__ import annotations

import streamlit as st

from ui import notice, section_title


_HOME_CSS = r"""
.ms-home-hero {
  margin: .4rem auto 1.1rem;
  padding: clamp(1.6rem, 4vw, 3.2rem);
  text-align: center;
}
.ms-home-hero::before {
  content: "";
  position: absolute;
  width: 420px;
  height: 420px;
  left: 50%;
  top: 42%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(89, 237, 185, .15), transparent 66%);
  pointer-events: none;
}
.ms-home-content { position: relative; z-index: 1; }
.ms-home-brand {
  margin: 0;
  font-size: clamp(2.65rem, 7vw, 5.4rem);
  line-height: .98;
  color: #f3fff9;
  text-shadow: 0 0 34px rgba(98, 231, 178, .22);
}
.ms-home-brand span { color: #9ef5d2; }
.ms-home-tagline {
  margin: .8rem auto .2rem;
  color: #dbe8ee;
  font-size: clamp(.92rem, 2vw, 1.12rem);
  font-weight: 650;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.ms-home-cn {
  margin: .2rem auto 1.15rem;
  color: #aebfca;
  font-size: .98rem;
}
.ms-shield-wrap {
  display: grid;
  place-items: center;
  width: 152px;
  height: 166px;
  margin: 1.1rem auto .8rem;
  filter: drop-shadow(0 14px 23px rgba(21, 203, 148, .25));
}
.ms-shield-wrap svg { width: 100%; height: 100%; }
.ms-hero-promise {
  max-width: 700px;
  margin: .6rem auto 0;
  color: #b8c9d3;
  font-size: .92rem;
}
.ms-home-stat {
  padding: 1rem 1.05rem;
  border: 1px solid rgba(153, 212, 222, .2);
  border-radius: 14px;
  background: rgba(7, 21, 37, .72);
  text-align: center;
}
.ms-home-stat strong { display: block; color: #f2fff9; font-size: 1.45rem; }
.ms-home-stat span { color: #9fb2bf; font-size: .8rem; }
.ms-trust-strip {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: .55rem;
  margin: 1rem 0 0;
}
.ms-trust-strip span {
  padding: .42rem .7rem;
  border: 1px solid rgba(135, 196, 209, .2);
  border-radius: 999px;
  color: #aebfca;
  background: rgba(6, 19, 34, .55);
  font-size: .75rem;
}
.ms-action-card {
  min-height: 184px;
  padding: 1.18rem;
  border: 1px solid rgba(154, 207, 219, .21);
  border-radius: 17px;
  background: linear-gradient(145deg, rgba(28, 50, 69, .72), rgba(7, 20, 36, .8));
  box-shadow: 0 13px 34px rgba(0, 8, 18, .21);
}
.ms-action-card .ms-action-icon { font-size: 1.7rem; }
.ms-action-card h3 { margin: .62rem 0 .34rem; font-size: 1.05rem; }
.ms-action-card p { margin: 0; color: #aebfca; font-size: .88rem; }
.ms-process-card {
  position: relative;
  min-height: 150px;
  padding: 1rem;
  border-top: 1px solid rgba(98, 231, 178, .42);
  border-radius: 0 0 14px 14px;
  background: rgba(8, 23, 39, .63);
}
.ms-process-card h3 { margin: .65rem 0 .25rem; font-size: 1rem; }
.ms-process-card p { margin: 0; color: #aebfca; font-size: .84rem; }
.ms-home-step-card { min-height: 168px; padding: 1.15rem; border-radius: 16px; }
"""


_SHIELD_SVG = """
<svg viewBox="0 0 180 205" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="shieldFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8effd2" stop-opacity=".92"/>
      <stop offset=".48" stop-color="#228b7c" stop-opacity=".82"/>
      <stop offset="1" stop-color="#102b48" stop-opacity=".96"/>
    </linearGradient>
    <linearGradient id="shieldStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#dbfff0"/>
      <stop offset="1" stop-color="#3ed6b2"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <path d="M90 8C65 23 43 29 24 31v59c0 54 31 88 66 107 35-19 66-53 66-107V31C137 29 115 23 90 8Z" fill="url(#shieldFill)" stroke="url(#shieldStroke)" stroke-width="4" filter="url(#glow)"/>
  <path d="M90 26C71 37 54 42 39 44v47c0 39 21 66 51 84 30-18 51-45 51-84V44c-15-2-32-7-51-18Z" fill="#071c30" fill-opacity=".7" stroke="#8effd2" stroke-opacity=".45" stroke-width="2"/>
  <path d="M60 93 80 113 123 67" fill="none" stroke="#9dffd8" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M90 30v139" stroke="#9affd6" stroke-opacity=".12" stroke-width="2"/>
</svg>
"""


def _go_to_verify(preferred_input: str = "text") -> None:
    st.session_state["preferred_input"] = preferred_input
    st.switch_page("pages/verify.py")


def render() -> None:
    st.markdown(f"<style>{_HOME_CSS}</style>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <section class="ms-home-hero ms-glass">
          <div class="ms-home-content">
            <div class="ms-kicker">AI Career Safety · Hong Kong &amp; Macao</div>
            <h1 class="ms-home-brand">Mindshield <span>心盾</span></h1>
            <p class="ms-home-tagline">AI-powered recruitment security for postgraduates</p>
            <p class="ms-home-cn">面向港澳硕士的 AI 智能求职安全助手</p>
            <div class="ms-shield-wrap">{_SHIELD_SVG}</div>
            <p class="ms-hero-promise">把职位文字、招聘链接或聊天截图交给心盾。先定位可疑证据，再告诉你如何核验、如何反问、下一步做什么。</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    primary, secondary = st.columns(2, gap="medium")
    with primary:
        if st.button(
            "🛡️ 进入 AI 核验中心",
            type="primary",
            use_container_width=True,
            help="分析招聘文字或职位链接",
        ):
            _go_to_verify("text")
    with secondary:
        if st.button(
            "📷 扫描招聘截图",
            use_container_width=True,
            help="上传聊天记录、海报或职位截图",
        ):
            _go_to_verify("image")

    st.markdown(
        """
        <div class="ms-trust-strip" aria-label="产品能力">
          <span>✓ 简体 · 繁體 · English</span>
          <span>✓ 文字 · 链接 · 图片</span>
          <span>✓ 证据定位而非只给分数</span>
          <span>✓ 港澳跨境求职规则</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_title("多源输入，一处核验", "不需要整理成标准格式，选择你手头最方便的材料。", "✦")
    input_cols = st.columns(3, gap="medium")
    input_cards = [
        ("📝", "招聘文字", "粘贴职位描述、邮件、WhatsApp 或微信聊天。支持中英文混合内容。"),
        ("🔗", "职位链接", "尝试提取公开网页正文；若网站要求登录，会提示改用文字或截图。"),
        ("📷", "聊天截图", "识别职位海报与聊天记录里的中英文文字，并允许你先校对再分析。"),
    ]
    for column, (icon, title, body) in zip(input_cols, input_cards):
        with column:
            st.markdown(
                f"""
                <article class="ms-action-card">
                  <div class="ms-action-icon">{icon}</div>
                  <h3>{title}</h3>
                  <p>{body}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )

    section_title("不只判断风险，更帮你行动", "为第一次求职的人，把专业判断翻译成下一步。", "◎")
    value_cols = st.columns(4, gap="small")
    values = [
        ("01", "标出证据", "引用原文中的可疑句子，说明为什么不合理。"),
        ("02", "拆解套路", "识别培训贷、垫资刷单、假高薪、签证诱饵等模式。"),
        ("03", "生成反问", "给你可直接复制给 HR 的中英文核验问题。"),
        ("04", "给出行动", "告诉你先查公司、保存证据，还是停止联系并求助。"),
    ]
    for column, (number, title, body) in zip(value_cols, values):
        with column:
            st.markdown(
                f"""
                <article class="ms-process-card">
                  <span class="ms-step-number">{number}</span>
                  <h3>{title}</h3>
                  <p>{body}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )

    section_title("三步完成一次安全检查", "结果是风险提示，不是对个人或公司的法律定性。", "→")
    step_cols = st.columns(3, gap="medium")
    steps = [
        ("1", "提交材料", "粘贴内容、网址或上传截图。先检查提取文字是否准确。"),
        ("2", "AI 审查", "从费用、身份、沟通、流程、跨境与链接等维度寻找红旗。"),
        ("3", "按建议核验", "使用官方渠道查公司、问清合同主体，并保护个人资料与资金。"),
    ]
    for column, (number, title, body) in zip(step_cols, steps):
        with column:
            st.markdown(
                f"""
                <article class="ms-mini-card ms-home-step-card">
                  <span class="ms-step-number">{number}</span>
                  <h3>{title}</h3>
                  <p>{body}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )

    notice(
        "使用前请知道",
        "AI 可能判断错误，也无法替代警方、律师、学校或政府部门。涉及付款、证件、验证码、出境或扣留护照时，请暂停操作并通过官方渠道核验。",
        "amber",
    )

    st.markdown(
        """
        <footer class="ms-footer-note">
          Mindshield 心盾 · Protecting your first career step<br>
          输入内容会发送给你所配置的 AI 服务商完成分析，请勿提交银行卡密码、验证码或完整证件号码。
        </footer>
        """,
        unsafe_allow_html=True,
    )


render()
