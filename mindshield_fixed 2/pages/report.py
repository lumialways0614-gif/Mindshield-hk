"""MindShield detailed recruitment-risk report page."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from ui import safe_text


REPORT_CSS = """
<style>
    .report-kicker {
        color: #72f2c5;
        font-size: .78rem;
        font-weight: 750;
        letter-spacing: .16em;
        margin-bottom: .5rem;
        text-transform: uppercase;
    }
    .report-title {
        color: #f5fffc;
        font-size: clamp(2rem, 4vw, 3.15rem);
        font-weight: 760;
        letter-spacing: -.035em;
        line-height: 1.05;
        margin: 0;
        text-shadow: 0 0 24px rgba(90, 236, 188, .16);
    }
    .report-subtitle {
        color: #adbec8;
        font-size: 1rem;
        margin: .7rem 0 1.6rem;
    }
    .glass-panel {
        background: linear-gradient(145deg, rgba(22, 42, 56, .83), rgba(10, 24, 36, .76));
        border: 1px solid rgba(145, 220, 205, .22);
        border-radius: 18px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, .04), 0 18px 48px rgba(0, 8, 18, .18);
        color: #e7f5f2;
        min-height: 100%;
        padding: 1.15rem 1.2rem;
    }
    .panel-label {
        color: #7ee9c1;
        font-size: .76rem;
        font-weight: 780;
        letter-spacing: .12em;
        margin-bottom: .85rem;
        text-transform: uppercase;
    }
    .audit-row {
        align-items: flex-start;
        border-bottom: 1px solid rgba(162, 210, 204, .11);
        display: flex;
        gap: .7rem;
        justify-content: space-between;
        padding: .55rem 0;
    }
    .audit-row:last-child { border-bottom: 0; }
    .audit-key { color: #8fa7b2; font-size: .83rem; }
    .audit-value {
        color: #edfdf8;
        font-size: .88rem;
        font-weight: 650;
        max-width: 68%;
        overflow-wrap: anywhere;
        text-align: right;
    }
    .score-panel { text-align: center; }
    .risk-gauge {
        height: 92px;
        margin: .3rem auto .15rem;
        max-width: 220px;
        overflow: hidden;
        position: relative;
    }
    .risk-gauge::before {
        background: conic-gradient(
            from 270deg at 50% 100%,
            var(--risk-color) 0deg,
            var(--risk-color) var(--risk-angle),
            rgba(147, 177, 184, .18) var(--risk-angle),
            rgba(147, 177, 184, .18) 180deg,
            transparent 180deg
        );
        border-radius: 220px 220px 0 0;
        content: "";
        inset: 0;
        position: absolute;
    }
    .risk-gauge::after {
        background: #102432;
        border-radius: 170px 170px 0 0;
        bottom: 0;
        content: "";
        height: 58px;
        left: 30px;
        position: absolute;
        right: 30px;
    }
    .score-number {
        color: #f8fffd;
        font-size: 2.45rem;
        font-weight: 800;
        line-height: 1;
        margin-top: -.12rem;
    }
    .score-number span { color: #8099a6; font-size: .9rem; font-weight: 600; }
    .risk-pill {
        border: 1px solid color-mix(in srgb, var(--risk-color) 58%, transparent);
        border-radius: 999px;
        color: var(--risk-color);
        display: inline-block;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .08em;
        margin: .55rem 0 .7rem;
        padding: .33rem .68rem;
        text-transform: uppercase;
    }
    .summary-text { color: #bed0d5; font-size: .9rem; line-height: 1.55; }
    .section-heading {
        color: #f1fcf8;
        font-size: 1.25rem;
        font-weight: 720;
        margin: 2rem 0 .25rem;
    }
    .section-caption { color: #839ca7; font-size: .86rem; margin-bottom: 1rem; }
    .evidence-card {
        background: rgba(10, 25, 36, .72);
        border: 1px solid rgba(244, 105, 98, .2);
        border-left: 3px solid #ff746d;
        border-radius: 12px;
        color: #dcebe9;
        margin: .55rem 0;
        padding: .8rem .9rem;
    }
    .evidence-quote { color: #fff4f1; font-weight: 700; margin-bottom: .32rem; }
    .evidence-reason { color: #9eb3bb; font-size: .86rem; line-height: 1.5; }
    .action-row {
        align-items: flex-start;
        background: rgba(10, 25, 36, .62);
        border: 1px solid rgba(126, 233, 193, .14);
        border-radius: 12px;
        display: flex;
        gap: .75rem;
        margin: .55rem 0;
        padding: .78rem .86rem;
    }
    .action-index {
        align-items: center;
        background: rgba(75, 224, 175, .14);
        border: 1px solid rgba(75, 224, 175, .28);
        border-radius: 9px;
        color: #74f0c4;
        display: flex;
        flex: 0 0 29px;
        font-size: .78rem;
        font-weight: 800;
        height: 29px;
        justify-content: center;
    }
    .action-copy { color: #d9e9e6; font-size: .89rem; line-height: 1.5; }
    .privacy-good, .privacy-stop {
        border-radius: 13px;
        min-height: 178px;
        padding: .9rem 1rem;
    }
    .privacy-good {
        background: rgba(43, 198, 143, .08);
        border: 1px solid rgba(84, 225, 177, .19);
    }
    .privacy-stop {
        background: rgba(239, 92, 84, .08);
        border: 1px solid rgba(255, 111, 104, .19);
    }
    .privacy-title { color: #edf9f6; font-size: .92rem; font-weight: 750; margin-bottom: .55rem; }
    .privacy-item { color: #adc1c5; font-size: .85rem; line-height: 1.5; margin: .35rem 0; }
    .source-preview {
        background: rgba(4, 15, 25, .62);
        border: 1px solid rgba(143, 199, 192, .13);
        border-radius: 12px;
        color: #a9bec5;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: .76rem;
        line-height: 1.52;
        margin-top: .9rem;
        max-height: 150px;
        overflow: auto;
        padding: .75rem .85rem;
        white-space: pre-wrap;
    }
    .empty-report {
        background: rgba(15, 34, 48, .72);
        border: 1px dashed rgba(111, 230, 190, .34);
        border-radius: 20px;
        color: #d9ece7;
        margin: 2rem 0 1rem;
        padding: 2rem;
        text-align: center;
    }
    .empty-icon { font-size: 2.4rem; margin-bottom: .5rem; }
    @media (max-width: 760px) {
        .report-title { font-size: 2rem; }
        .glass-panel { padding: 1rem; }
        .audit-value { max-width: 62%; }
    }
</style>
"""


BILINGUAL_QUESTIONS = [
    (
        "请确认招聘及入职过程中是否需要我支付任何培训费、押金、设备费或其他费用？",
        "Could you confirm whether I need to pay any training, deposit, equipment, or other fees during recruitment or onboarding?",
    ),
    (
        "请提供发出 Offer 的雇佣实体全名、公司注册编号及官方网站，方便我通过官方渠道核验。",
        "Please provide the full legal name, registration number, and official website of the employing entity so I can verify them independently.",
    ),
    (
        "我可以通过公司官网公布的电话或正式域名邮箱确认这次招聘吗？",
        "May I confirm this recruitment through the phone number or corporate-domain email published on your official website?",
    ),
    (
        "请问正式合同会否写明工作地点、薪酬、试用期、汇报对象及签证责任？",
        "Will the formal contract state the work location, compensation, probation period, reporting line, and visa responsibilities?",
    ),
]


OFFER_CHECKLIST = [
    "已从官方公司注册处核验雇佣实体 / Employer verified via an official company registry",
    "招聘邮箱域名与公司官网一致 / Recruiter email domain matches the official website",
    "Offer 写明职位、地点、薪酬、试用期和合同主体 / Offer states role, location, pay, probation, and legal employer",
    "已通过独立官方渠道回拨确认 / Recruitment confirmed through an independently found official channel",
    "没有预付培训费、押金、设备费或转账 / No advance training, deposit, equipment payment, or transfer",
    "IANG、签证或跨境安排已查阅政府官方资料 / IANG, visa, or cross-border claims checked against official guidance",
]


def _as_list(value: Any) -> list[Any]:
    """Return a predictable list for loosely structured model output."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _score(value: Any) -> int:
    try:
        return max(0, min(100, int(float(value))))
    except (TypeError, ValueError):
        return 50


def _risk_style(level: str, score: int) -> tuple[str, str, str]:
    normalized = level.casefold()
    if "高" in level or "high" in normalized or score >= 70:
        return "#ff6b63", "HIGH RISK · 高风险", "🔴"
    if "低" in level or "low" in normalized or score < 35:
        return "#54e0b0", "LOW RISK · 低风险", "🟢"
    return "#ffc65b", "MEDIUM RISK · 中风险", "🟠"


def _value(value: Any, fallback: str = "待核实") -> str:
    text = str(value or "").strip()
    return text or fallback


def _render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-report">
            <div class="empty-icon">🛡️</div>
            <h3>还没有可显示的风险报告</h3>
            <p>请先到“职位核验”页面提交招聘文字、链接或截图，并完成一次 AI 审查。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/verify.py", label="前往职位核验中心", icon="🔎", use_container_width=True)


def _render_audit_focus(
    analysis: dict[str, Any], source_text: str, source_url: str, source_type: str
) -> None:
    language = _value(analysis.get("language_detected"), "未识别")
    flags = len(_as_list(analysis.get("red_flags")))
    categories = len(_as_list(analysis.get("categories")))
    origin = source_url or "未提供网址"
    excerpt = source_text[:620].strip()
    if len(source_text) > 620:
        excerpt += "…"

    st.markdown(
        f"""
        <div class="glass-panel">
            <div class="panel-label">Audit focus · 审查重点</div>
            <div class="audit-row"><span class="audit-key">材料类型</span><span class="audit-value">{safe_text(source_type)}</span></div>
            <div class="audit-row"><span class="audit-key">检测语言</span><span class="audit-value">{safe_text(language)}</span></div>
            <div class="audit-row"><span class="audit-key">风险线索</span><span class="audit-value">{flags} 条红旗 · {categories} 个维度</span></div>
            <div class="audit-row"><span class="audit-key">来源链接</span><span class="audit-value">{safe_text(origin)}</span></div>
            <div class="source-preview">{safe_text(excerpt or "本次分析未保存原始文本预览。")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_gauge(analysis: dict[str, Any]) -> None:
    score = _score(analysis.get("risk_score"))
    level = _value(analysis.get("risk_level"), "中风险")
    color, display_level, dot = _risk_style(level, score)
    summary = _value(analysis.get("summary"), "已完成风险扫描，请结合下方证据进行人工核验。")

    st.markdown(
        f"""
        <div class="glass-panel score-panel" style="--risk-color:{color}; --risk-angle:{score * 1.8}deg;">
            <div class="panel-label">Risk gauge · 风险量表</div>
            <div class="risk-gauge" role="img" aria-label="风险评分 {score} 分"></div>
            <div class="score-number">{score}<span>/100</span></div>
            <div class="risk-pill">{dot} {safe_text(display_level)}</div>
            <div class="summary-text">{safe_text(summary)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_deep_dive(analysis: dict[str, Any]) -> None:
    st.markdown('<div class="section-heading">风险类型深挖 · Scam deep dive</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">逐项查看模型依据。没有证据不等于已经核验安全。</div>',
        unsafe_allow_html=True,
    )
    categories = _as_list(analysis.get("categories"))
    if not categories:
        st.info("本次结果没有返回风险类别明细，建议重新分析或进行人工核验。")
        return

    for index, item in enumerate(categories, start=1):
        if not isinstance(item, dict):
            item = {"name": str(item), "level": "待核实", "explanation": ""}
        name = _value(item.get("name"), f"风险维度 {index}")
        item_level = _value(item.get("level"), "待核实")
        evidence = _value(item.get("evidence"), "未发现可直接引用的原文证据")
        explanation = _value(item.get("explanation"), "仍需通过公司官方渠道核验。")
        icon = "🔴" if ("高" in item_level or "high" in item_level.casefold()) else "🟡"
        if "低" in item_level or "未发现" in item_level or "low" in item_level.casefold():
            icon = "🟢"
        with st.expander(f"{icon} {index}. 风险维度详情", expanded=index <= 2):
            st.markdown(
                f'<p><strong>{safe_text(name)}</strong> · {safe_text(item_level)}</p>'
                f'<p><strong>原文证据</strong>：{safe_text(evidence)}</p>'
                f'<p><strong>为什么要注意</strong>：{safe_text(explanation)}</p>',
                unsafe_allow_html=True,
            )

    red_flags = _as_list(analysis.get("red_flags"))
    if red_flags:
        st.markdown("#### 可疑原文证据")
        for flag in red_flags:
            if isinstance(flag, dict):
                quote = _value(flag.get("quote"), "未提供原文")
                reason = _value(flag.get("reason"), "需要进一步核验")
            else:
                quote, reason = str(flag), "需要进一步核验"
            st.markdown(
                f'<div class="evidence-card"><div class="evidence-quote">“{safe_text(quote)}”</div>'
                f'<div class="evidence-reason">{safe_text(reason)}</div></div>',
                unsafe_allow_html=True,
            )


def _render_questions(analysis: dict[str, Any]) -> None:
    st.markdown('<div class="section-heading">双语反向质询 · Bilingual verification</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">直接复制给招聘方；正规招聘者通常愿意提供可独立核验的信息。</div>',
        unsafe_allow_html=True,
    )
    custom_tab, bilingual_tab = st.tabs(["AI 定制问题", "中英双语话术库"])
    with custom_tab:
        custom_questions = _as_list(analysis.get("verification_questions"))
        if custom_questions:
            for index, question in enumerate(custom_questions, start=1):
                st.caption(f"问题 {index}")
                st.code(str(question), language=None)
        else:
            st.info("本次没有返回定制问题，可使用旁边的双语话术库。")
    with bilingual_tab:
        for index, (zh_question, en_question) in enumerate(BILINGUAL_QUESTIONS, start=1):
            st.caption(f"核验问题 {index}")
            st.code(f"中文：{zh_question}\nEnglish: {en_question}", language=None)


def _render_offer_checklist(analysis: dict[str, Any]) -> None:
    st.markdown('<div class="section-heading">Offer 核验清单 · Offer safeguard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">逐项完成后再签约、提交敏感资料或安排跨境行程。勾选状态只保存在当前会话。</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2)
    for index, item in enumerate(OFFER_CHECKLIST):
        target = left if index % 2 == 0 else right
        with target:
            st.checkbox(item, key=f"offer_check_{index}")

    missing = _as_list(analysis.get("missing_information"))
    if missing:
        with st.expander("本次报告特别建议补充核实"):
            for item in missing:
                st.text(f"• {item}")


def _render_actions_and_privacy(analysis: dict[str, Any]) -> None:
    st.markdown('<div class="section-heading">下一步行动 · What to do now</div>', unsafe_allow_html=True)
    actions = _as_list(analysis.get("actions"))
    if not actions:
        actions = [
            "暂停付款和提交敏感资料。",
            "从公司官网独立寻找联系方式，不要只使用招聘者提供的号码。",
            "向学校就业中心、招聘平台或相关政府部门核验。",
        ]
    for index, action in enumerate(actions, start=1):
        st.markdown(
            f'<div class="action-row"><div class="action-index">{index:02d}</div>'
            f'<div class="action-copy">{safe_text(action)}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">隐私保护清单 · Privacy guard</div>', unsafe_allow_html=True)
    share = _as_list(analysis.get("safe_to_share")) or ["去敏后的简历", "公开作品集", "一般工作经历"]
    protect = _as_list(analysis.get("do_not_share")) or ["验证码和密码", "银行卡完整资料", "未遮盖的身份证或护照"]
    share_html = "".join(f'<div class="privacy-item">✓ {safe_text(item)}</div>' for item in share)
    protect_html = "".join(f'<div class="privacy-item">✕ {safe_text(item)}</div>' for item in protect)
    col_good, col_stop = st.columns(2)
    with col_good:
        st.markdown(
            f'<div class="privacy-good"><div class="privacy-title">✅ 通常可提供 / Usually okay</div>{share_html}</div>',
            unsafe_allow_html=True,
        )
    with col_stop:
        st.markdown(
            f'<div class="privacy-stop"><div class="privacy-title">⛔ 暂时不要提供 / Do not share yet</div>{protect_html}</div>',
            unsafe_allow_html=True,
        )


def _render_download(
    analysis: dict[str, Any], source_text: str, source_url: str, source_type: str
) -> None:
    st.markdown('<div class="section-heading">保存报告 · Export</div>', unsafe_allow_html=True)
    st.caption("下载内容包含原始招聘文字，请先确认其中没有不希望保存或分享的个人资料。")
    payload = {
        "product": "MindShield / 心盾",
        "source_type": source_type,
        "source_url": source_url,
        "source_text": source_text,
        "analysis": analysis,
    }
    data = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    st.download_button(
        "下载 JSON 风险报告",
        data=data,
        file_name="mindshield-risk-report.json",
        mime="application/json",
        icon="⬇️",
        use_container_width=True,
    )


st.markdown(REPORT_CSS, unsafe_allow_html=True)

analysis = st.session_state.get("latest_analysis")
source_text = str(
    st.session_state.get("source_text")
    or st.session_state.get("analysis_source_text")
    or ""
)
source_url = str(
    st.session_state.get("source_url")
    or st.session_state.get("analysis_source_url")
    or ""
)
source_type = str(
    st.session_state.get("source_type")
    or st.session_state.get("analysis_source_type")
    or "未记录"
)

st.markdown('<div class="report-kicker">MindShield intelligence report</div>', unsafe_allow_html=True)
st.markdown('<h1 class="report-title">详细风险报告</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="report-subtitle">Detailed content report · 从风险判断走向可执行的求职核验</div>',
    unsafe_allow_html=True,
)

if not isinstance(analysis, dict) or not analysis:
    _render_empty_state()
    st.stop()

focus_column, gauge_column = st.columns([1.45, 1], gap="medium")
with focus_column:
    _render_audit_focus(analysis, source_text, source_url, source_type)
with gauge_column:
    _render_gauge(analysis)

_render_deep_dive(analysis)

question_column, checklist_column = st.columns([1.08, .92], gap="large")
with question_column:
    _render_questions(analysis)
with checklist_column:
    _render_offer_checklist(analysis)

_render_actions_and_privacy(analysis)

reply_template = _value(
    analysis.get("reply_template"),
    "为保障求职安全，请通过公司正式邮箱提供雇佣实体、职位详情及完整合同，我会通过官方渠道独立核验。",
)
st.markdown('<div class="section-heading">可复制的核验回复 · Reply template</div>', unsafe_allow_html=True)
st.code(reply_template, language=None)

_render_download(analysis, source_text, source_url, source_type)

st.divider()
st.caption(
    safe_text(
        _value(
            analysis.get("disclaimer"),
            "AI 报告只用于风险筛查，不构成法律结论，也不能替代警方、学校就业中心、招聘平台或公司官方渠道的核验。",
        )
    )
)
