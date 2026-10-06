"""Recruitment-safety knowledge library and official resources."""

from __future__ import annotations

import streamlit as st

from ui import notice, page_intro, resource_card, section_title


_LIBRARY_CSS = r"""
.ms-risk-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: .75rem;
  margin: .75rem 0;
}
.ms-risk-row {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: .8rem;
  align-items: start;
  padding: 1rem;
  border: 1px solid rgba(159, 209, 221, .2);
  border-radius: 15px;
  background: rgba(8, 23, 40, .73);
}
.ms-risk-icon {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border: 1px solid rgba(255, 110, 118, .35);
  border-radius: 12px;
  background: rgba(255, 110, 118, .1);
  font-size: 1.15rem;
}
.ms-risk-row h3 { margin: 0 0 .25rem; font-size: .98rem; }
.ms-risk-row p { margin: 0; color: #aebfca; font-size: .84rem; }
.ms-checklist {
  display: grid;
  gap: .65rem;
  margin: .55rem 0;
}
.ms-check-item {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr);
  gap: .75rem;
  padding: .8rem .9rem;
  border-left: 3px solid #62e7b2;
  border-radius: 0 12px 12px 0;
  background: rgba(8, 23, 40, .7);
}
.ms-check-item b { color: #eafff6; }
.ms-check-item p { margin: .1rem 0 0; color: #aebfca; font-size: .84rem; }
.ms-check-number {
  display: grid;
  place-items: center;
  width: 29px;
  height: 29px;
  border-radius: 50%;
  color: #08231b;
  background: #62e7b2;
  font-size: .75rem;
  font-weight: 900;
}
.ms-case-card {
  height: 100%;
  min-height: 185px;
  padding: 1rem;
  border: 1px solid rgba(161, 207, 220, .2);
  border-radius: 15px;
  background: linear-gradient(145deg, rgba(25, 48, 67, .7), rgba(7, 20, 35, .78));
}
.ms-case-card h3 { margin: 0 0 .4rem; font-size: 1rem; }
.ms-case-card p { margin: .2rem 0; color: #aebfca; font-size: .84rem; }
.ms-case-card strong { color: #ffc86b; }
.ms-language-note {
  display: inline-flex;
  margin-top: .6rem;
  padding: .3rem .55rem;
  border: 1px solid rgba(98, 207, 235, .28);
  border-radius: 999px;
  color: #8dddf0;
  background: rgba(39, 111, 137, .14);
  font-size: .72rem;
  font-weight: 750;
}
@media (max-width: 720px) {
  .ms-risk-grid { grid-template-columns: 1fr; }
}
"""


def _risk_library() -> None:
    risks = [
        ("💳", "先付款才能入职", "保证金、培训费、设备费、签证费或“解冻佣金”都值得立即暂停核验。"),
        ("📈", "轻松高薪却不说工作", "只强调日薪、佣金和名额紧张，却回避职责、地点、团队与合同主体。"),
        ("🧾", "索取敏感资料", "在正式流程前索要银行卡密码、验证码、网银登录资料或完整证件照片。"),
        ("💬", "强制转去私人聊天", "要求离开招聘平台，只在私人 WhatsApp、Telegram 或微信账号沟通。"),
        ("⚡", "制造时间压力", "“今天不交钱就取消 offer”“马上下载软件”“不能问学校或家人”。"),
        ("🏢", "公司身份对不上", "联系人邮箱、公司名称、网站域名、办公地址或合同雇主彼此不一致。"),
        ("🌏", "跨境出行与扣证", "以培训、团建、考察为名要求出境，或声称要代管护照及身份证。"),
        ("🛒", "任务返佣与刷单", "先给小额返利建立信任，再要求垫资、充值或完成越来越贵的任务。"),
    ]
    # Keep repeated HTML compact.  Markdown treats indented blocks that follow
    # a blank line as source code, which would expose the second card's tags.
    cards = "".join(
        f'<article class="ms-risk-row"><div class="ms-risk-icon">{icon}</div>'
        f'<div><h3>{title}</h3><p>{body}</p></div></article>'
        for icon, title, body in risks
    )
    st.markdown(f'<div class="ms-risk-grid">{cards}</div>', unsafe_allow_html=True)


def _scenario_cards() -> None:
    hk_tab, macao_tab, cross_border_tab = st.tabs(["香港求职", "澳门求职", "跨境 / 海外机会"])

    with hk_tab:
        columns = st.columns(3, gap="medium")
        cards = [
            (
                "IANG / 签证诱饵",
                "对方把“保证续签、保证永居”当作收费服务，或要求把申请交给不明中介。",
                "先到入境事务处核对 IANG 规则；不要把口头承诺当作批准。",
            ),
            (
                "假冒大型企业 HR",
                "使用免费邮箱或相似域名，跳过正式面试，直接发来带付款要求的 offer。",
                "从公司官网重新找到招聘渠道，独立联系，而不是回复对方提供的号码。",
            ),
            (
                "无牌职业介绍所",
                "声称有内部名额，先收取介绍费或文件处理费，却拒绝提供牌照资料。",
                "在劳工处职业介绍所专题网站核验牌照；费用规则以官方说明为准。",
            ),
        ]
        for column, (title, signal, action) in zip(columns, cards):
            with column:
                st.markdown(
                    f"""
                    <article class="ms-case-card">
                      <h3>{title}</h3>
                      <p><strong>警号：</strong>{signal}</p>
                      <p><strong>先做：</strong>{action}</p>
                      <span class="ms-language-note">HK-specific</span>
                    </article>
                    """,
                    unsafe_allow_html=True,
                )

    with macao_tab:
        columns = st.columns(3, gap="medium")
        cards = [
            (
                "办证费与虚假配额",
                "招聘者要求先支付高额“办证费”，但无法证明实际职位、雇主或外地雇员配额。",
                "向澳门劳工事务局核对规则与职业介绍所许可，不凭私人收据付款。",
            ),
            (
                "MPay / 银行验证码",
                "以兼职工资或返佣为由，要求在陌生网页输入账户密码和短信验证码。",
                "立即停止；验证码等于授权钥匙，正规雇主不需要它来发工资。",
            ),
            (
                "点赞与任务兼职",
                "最初任务简单且可能真的返小额佣金，随后要求充值或垫资才能提现。",
                "不要追加资金，保留聊天与转账记录；有疑问可致电司警防诈骗热线。",
            ),
        ]
        for column, (title, signal, action) in zip(columns, cards):
            with column:
                st.markdown(
                    f"""
                    <article class="ms-case-card">
                      <h3>{title}</h3>
                      <p><strong>警号：</strong>{signal}</p>
                      <p><strong>先做：</strong>{action}</p>
                      <span class="ms-language-note">Macao-specific</span>
                    </article>
                    """,
                    unsafe_allow_html=True,
                )

    with cross_border_tab:
        columns = st.columns(3, gap="medium")
        cards = [
            (
                "“出境培训”陷阱",
                "入职前被要求前往陌生地区，行程、办公室、雇主和返程安排都不透明。",
                "把行程告知家人和学校；无法独立核验前不要出发，更不要交出证件。",
            ),
            (
                "合同主体错位",
                "招聘品牌、面试公司、发薪实体和签约雇主是四个不同名称。",
                "要求书面说明雇佣实体、工作地点、币种、税务与适用法律。",
            ),
            (
                "远程设备采购",
                "对方寄来假支票或要求你先在指定网站购买电脑，承诺之后报销。",
                "等待款项不可撤回地结算；不要使用对方指定的不明供应商。",
            ),
        ]
        for column, (title, signal, action) in zip(columns, cards):
            with column:
                st.markdown(
                    f"""
                    <article class="ms-case-card">
                      <h3>{title}</h3>
                      <p><strong>警号：</strong>{signal}</p>
                      <p><strong>先做：</strong>{action}</p>
                      <span class="ms-language-note">Cross-border</span>
                    </article>
                    """,
                    unsafe_allow_html=True,
                )


def _verification_checklist() -> None:
    items = [
        ("1", "把名字拆开查", "分别核对品牌名、合同雇主、付款账户名称、邮箱域名和办公地址。"),
        ("2", "从官网重新联系", "不要只使用招聘者发来的链接和电话；独立找到公司官网和总机。"),
        ("3", "问清五个事实", "岗位职责、直属经理、工作地点、薪资币种、合同与签证由谁负责。"),
        ("4", "查牌照与登记", "公司登记只能证明登记存在；如涉及中介，还要查职业介绍所牌照。"),
        ("5", "付款前暂停一次", "请朋友、学校就业中心或官方热线复核。正规机会经得起合理核验。"),
    ]
    markup = "".join(
        f'<div class="ms-check-item"><span class="ms-check-number">{number}</span>'
        f'<div><b>{title}</b><p>{body}</p></div></div>'
        for number, title, body in items
    )
    st.markdown(f'<div class="ms-checklist">{markup}</div>', unsafe_allow_html=True)


def _official_resources() -> None:
    rows = [
        (
            (
                "香港警务处 ADCC",
                "查看最新诈骗警示；反诈骗咨询热线 18222 提供全天候咨询。紧急情况请致电 999。",
                "https://www.adcc.gov.hk/",
                "打开 ADCC ↗",
                "香港官方",
            ),
            (
                "Scameter 防骗视伏器",
                "在香港警务处守网者平台查询可疑电话、网址、社交账号和收款资料的风险记录。",
                "https://cyberdefender.hk/en-us/scameter/",
                "使用 Scameter ↗",
                "香港官方",
            ),
            (
                "公司注册处电子查册",
                "核对香港公司的登记名称、状态与公开记录。登记存在不等于招聘一定真实。",
                "https://www.cr.gov.hk/en/electronic/e-servicesportal/e-search.htm",
                "查看查册说明 ↗",
                "香港官方",
            ),
        ),
        (
            (
                "劳工处职业介绍所专题网站",
                "查询香港职业介绍所有效牌照、监管说明与投诉渠道。",
                "https://www.eaa.labour.gov.hk/en/home.html",
                "查询持牌中介 ↗",
                "香港官方",
            ),
            (
                "入境事务处 IANG",
                "核对非本地毕业生留港／回港就业安排和申请要求，以官方规则为准。",
                "https://www.immd.gov.hk/eng/services/visas/IANG.html",
                "查看 IANG 规则 ↗",
                "香港官方",
            ),
            (
                "澳门司法警察局防诈骗热线",
                "24 小时防诈骗查询热线 8800 7777；如需报案，致电司警报案热线 993。",
                "https://www.pj.gov.mo/Web/Policia/crime05.html?lang=en",
                "查看热线说明 ↗",
                "澳门官方",
            ),
        ),
        (
            (
                "澳门劳工事务局职业介绍所",
                "查阅澳门职业介绍所活动许可、法规、表格和联络资料。",
                "https://www.dsal.gov.mo/en/text/employment_recruitment_agency.html",
                "查看许可资料 ↗",
                "澳门官方",
            ),
            (
                "ADCC 18222 热线说明",
                "了解香港反诈骗咨询热线的用途。若已经受骗，应到警署报案；紧急情况致电 999。",
                "https://www.adcc.gov.hk/en-hk/contact-us.html",
                "查看求助方式 ↗",
                "香港官方",
            ),
            (
                "澳门劳工事务局网上服务",
                "查看招聘、职业介绍所牌照状态及劳动权益相关网上服务入口。",
                "https://www.dsal.gov.mo/en/standard/online_services.html",
                "打开网上服务 ↗",
                "澳门官方",
            ),
        ),
    ]
    for row in rows:
        columns = st.columns(3, gap="medium")
        for column, args in zip(columns, row):
            with column:
                resource_card(*args)
        st.write("")


def render() -> None:
    st.markdown(f"<style>{_LIBRARY_CSS}</style>", unsafe_allow_html=True)
    page_intro(
        "Safety Library · 求职安全库",
        "看懂套路，才能主动核验",
        "为港澳硕士整理的招聘红旗、跨境风险与官方查询入口。先学会识别，再把可疑内容交给 AI 分析。",
    )

    section_title("八类高频招聘红旗", "单一迹象不一定等于诈骗；多个迹象同时出现时应立即暂停。", "⚠")
    _risk_library()

    section_title("港澳与跨境场景", "同一种话术在不同地区，应该使用不同官方渠道核验。", "⌖")
    _scenario_cards()

    section_title("收到 Offer 后的 5 分钟核验", "先独立找资料，再向招聘方提出具体问题。", "✓")
    _verification_checklist()
    notice(
        "查到公司登记，不代表招聘者就是真的",
        "诈骗者可能冒用真实公司名称、员工照片和公开登记资料。还要核对联系渠道、合同主体、邮箱域名、付款账户与招聘流程是否一致。",
        "amber",
    )

    section_title("官方核验与求助资源", "这些链接指向香港或澳门政府及警方网站；打开后仍请核对浏览器域名。", "↗")
    _official_resources()

    st.markdown(
        """
        <footer class="ms-footer-note">
          资源页面会随政府网站更新而变化；法律、签证和费用问题请以对应部门的最新说明为准。<br>
          Mindshield 提供教育性风险提示，不构成法律意见或官方认证。
        </footer>
        """,
        unsafe_allow_html=True,
    )


render()
