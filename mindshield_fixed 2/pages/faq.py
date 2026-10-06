"""Frequently asked questions for Mindshield."""

from __future__ import annotations

import streamlit as st

from ui import notice, page_intro, section_title


_FAQ_CSS = r"""
.ms-help-banner {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 1rem;
  align-items: center;
  margin: .6rem 0 1.2rem;
  padding: 1.1rem 1.2rem;
  border: 1px solid rgba(255, 200, 107, .32);
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(103, 65, 24, .32), rgba(8, 23, 40, .78));
}
.ms-help-banner .ms-help-icon {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255, 200, 107, .14);
  font-size: 1.45rem;
}
.ms-help-banner h3 { margin: 0 0 .2rem; font-size: 1rem; }
.ms-help-banner p { margin: 0; color: #c2cdd4; font-size: .86rem; }
.ms-question-kit {
  display: grid;
  gap: .65rem;
  margin: .65rem 0;
}
.ms-question-item {
  padding: .85rem .95rem;
  border: 1px solid rgba(155, 206, 219, .2);
  border-radius: 13px;
  background: rgba(7, 22, 38, .72);
}
.ms-question-item strong { display: block; margin-bottom: .22rem; color: #ecfff7; }
.ms-question-item span { color: #9ff0d0; font-size: .82rem; }
.ms-emergency-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: .75rem;
  margin: .8rem 0;
}
.ms-emergency-card {
  padding: 1rem;
  border: 1px solid rgba(255, 110, 118, .25);
  border-radius: 15px;
  background: rgba(64, 21, 31, .34);
}
.ms-emergency-card h3 { margin: 0 0 .35rem; font-size: 1rem; }
.ms-emergency-card p { margin: 0; color: #c4ccd2; font-size: .84rem; }
.ms-emergency-card b { color: #ffb9bd; }
@media (max-width: 720px) {
  .ms-emergency-grid { grid-template-columns: 1fr; }
}
"""


def _product_questions() -> None:
    with st.expander("心盾可以分析哪些内容？", expanded=True):
        st.markdown(
            """
            可以分析招聘广告、职位描述、HR 邮件与聊天记录，并支持三种输入：

            - 直接粘贴文字；
            - 输入可公开访问的职位网页链接；
            - 上传招聘海报、职位页或聊天截图，先用 OCR 提取文字。

            如果材料很长，建议只保留职位描述、薪资、入职流程、付款要求和关键聊天内容。
            """
        )

    with st.expander("支持中文、繁体中文和英文吗？"):
        st.markdown(
            """
            支持简体中文、繁體中文、English 以及中英混合内容。报告可以按页面提供的语言选项输出。

            不过，俚语、公司内部缩写和模糊截图仍可能被误解。看到金额、公司名、电话号码或签证类别时，请先检查提取文字是否准确。
            """
        )

    with st.expander("为什么有些 BOSS 直聘、LinkedIn 或 JobsDB 链接读不到？"):
        st.markdown(
            """
            有些招聘网站需要登录、使用 App 打开、由 JavaScript 动态加载，或限制自动读取。链接失败不代表链接一定危险，也不代表程序坏了。

            最简单的替代方式是：复制职位文字，或截取包含公司名、职责、薪资和联系方法的页面上传。
            """
        )

    with st.expander("风险分数等于“诈骗概率”吗？"):
        st.markdown(
            """
            **不等于。** 风险分数只是把文本中观察到的红旗集中表达，方便你决定核验优先级。它不是司法结论，也不是统计意义上的诈骗概率。

            - 高风险：存在付款、敏感资料、身份矛盾、异常流程等强红旗；
            - 中风险：信息不足或出现若干异常，需要进一步核验；
            - 低风险：目前没有看到明显红旗，但仍不代表招聘一定真实。
            """
        )

    with st.expander("AI 会不会判断错误？"):
        st.markdown(
            """
            会。AI 可能遗漏暗语，也可能把正常的行业流程误判为风险。因此结果页应该重点看“引用了哪句话”和“建议如何核验”，不要只看颜色或分数。

            遇到付款、签证、证件、出境或法律问题，应再向官方部门、学校就业中心或合资格专业人士确认。
            """
        )


def _privacy_questions() -> None:
    with st.expander("我的 DeepSeek API Key 会保存在哪里？", expanded=True):
        st.markdown(
            """
            心盾的设计不会把 API Key 写进源代码或分析报告。Key 通常只存在当前 Streamlit 会话中，用来向你选择的 AI 服务发出请求。

            仍请注意：如果你把应用部署到第三方服务器，服务器运营方和 AI 服务商各自的隐私政策也适用。不要把 Key 放进 GitHub、截图或公开聊天。
            """
        )

    with st.expander("上传截图后会发生什么？"):
        st.markdown(
            """
            图片先用于 OCR 文字识别。你应在页面里检查、修改识别结果；开始 AI 分析后，提取出的文字会发送给你配置的 AI 服务商。

            上传前请遮盖完整身份证号、护照号、银行卡号、住址、验证码、密码和与判断无关的私人对话。
            """
        )

    with st.expander("可以直接上传身份证、合同或完整聊天记录吗？"):
        st.markdown(
            """
            不建议上传完整敏感文件。为了识别招聘风险，通常只需要：

            - 公司和职位名称；
            - 薪资、地点与合同主体；
            - 对方要求付款、提供资料或转移平台的句子；
            - 入职、签证与面试流程。

            先裁剪截图或打码，只保留必要内容。
            """
        )

    with st.expander("如何安全保管 API Key？"):
        st.markdown(
            """
            - 本地测试时，在网页的密码输入框临时填写；
            - 部署时使用 Streamlit Secrets 或主机提供的环境变量；
            - 不要写进 `app.py`、`requirements.txt` 或 GitHub；
            - 怀疑泄露时立即到服务商后台撤销并重新生成。
            """
        )


def _job_questions() -> None:
    with st.expander("查到公司注册记录，就能证明招聘是真的吗？", expanded=True):
        st.markdown(
            """
            不能。诈骗者可能冒用真实公司名称、地址、员工照片和登记号码。公司存在，只能说明该登记主体存在。

            你还要独立核对联系人邮箱域名、公司官网招聘页、合同雇主、办公地点、付款账户，以及该公司是否真的发布过这个职位。
            """
        )

    with st.expander("招聘者说要先付培训费、签证费或设备费，正常吗？"):
        st.markdown(
            """
            这是强风险信号。不要因为对方发来 offer、收据或公司登记截图就付款。先通过政府网站核实规则，再从公司官网独立联系正式 HR。

            如果对方要求使用加密货币、礼品卡、个人账户或陌生支付网页，风险更高，应立即暂停。
            """
        )

    with st.expander("对方要求 WhatsApp / 微信面试，是否一定是诈骗？"):
        st.markdown(
            """
            不一定。一些小公司或跨境团队确实会用即时通讯工具，但以下组合值得警惕：只有文字聊天、拒绝视频或正式邮箱、没有明确面试官身份、立即录用、同时要求付款或敏感资料。

            你可以要求使用公司邮箱发送面试邀请，并通过公司官网或总机确认面试官身份。
            """
        )

    with st.expander("IANG、工作签证或永居承诺应该怎样核验？"):
        st.markdown(
            """
            先查看香港入境事务处或澳门相关政府部门的最新规则。招聘者可以说明公司愿意提供哪些文件，但不能代表政府保证批准申请，更不应以“保证获批”为由收取不透明费用。

            要求对方写明雇佣实体、工作地点、合同期限、由谁申请、由谁承担费用，以及申请不获批时如何处理。
            """
        )

    with st.expander("怎样向招聘方反向核验，又不会显得冒犯？"):
        st.markdown(
            """
            保持具体、礼貌，并要求可独立验证的信息。正规招聘者通常能理解求职者需要核对合同和身份。

            不要问笼统的“你们是不是骗子”；改问公司邮箱、合同主体、面试官职位、办公室地址和收费依据。
            """
        )


def _emergency_help() -> None:
    st.markdown(
        """
        <div class="ms-emergency-grid">
          <article class="ms-emergency-card">
            <h3>🇭🇰 香港</h3>
            <p><b>反诈骗咨询：</b>ADCC 18222（全天候）<br><b>紧急求助：</b>999<br>如怀疑已经受骗，应尽快联络银行并到警署报案。</p>
          </article>
          <article class="ms-emergency-card">
            <h3>🇲🇴 澳门</h3>
            <p><b>防诈骗查询：</b>司法警察局 8800 7777（24 小时）<br><b>报案热线：</b>993<br>尽快联络付款机构，并保存聊天、网址和交易记录。</p>
          </article>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notice(
        "已经转账或交出验证码？不要等待 AI 结果",
        "立即联系银行或支付平台尝试止付，修改相关密码，冻结受影响账户，并通过警方官方渠道报案。不要再向声称能追回款项的人支付“解冻费”或“律师费”。",
        "red",
    )


def _question_kit() -> None:
    st.markdown(
        """
        <div class="ms-question-kit">
          <div class="ms-question-item"><strong>请问最终与我签订雇佣合同的法律实体全名是什么？</strong><span>What is the full legal name of the entity that will employ and pay me?</span></div>
          <div class="ms-question-item"><strong>可以使用公司正式邮箱发送职位说明和面试邀请吗？</strong><span>Could you send the job description and interview invitation from your official company email?</span></div>
          <div class="ms-question-item"><strong>招聘或入职过程中是否有任何需要我支付的费用？请提供书面依据。</strong><span>Are there any fees I must pay during recruitment or onboarding? Please provide the policy in writing.</span></div>
          <div class="ms-question-item"><strong>我的工作地点、直属经理、薪资币种和试用期分别是什么？</strong><span>What are the work location, reporting manager, salary currency and probation terms?</span></div>
          <div class="ms-question-item"><strong>如涉及签证，公司会提供哪些文件？申请由哪个官方部门审批？</strong><span>What documents will the company provide for the visa, and which authority makes the decision?</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.markdown(f"<style>{_FAQ_CSS}</style>", unsafe_allow_html=True)
    page_intro(
        "Help Centre · 常见问题",
        "第一次求职，也能安心核验",
        "这里解释心盾能做什么、不能做什么，以及遇到付款、证件与跨境风险时应怎样处理。",
    )

    st.markdown(
        """
        <section class="ms-help-banner">
          <div class="ms-help-icon">⚡</div>
          <div><h3>如果对方正在催你转账、提供验证码或立即出境</h3><p>先停止操作。不要因为“名额只剩一个”而跳过核验，也不要继续与对方争辩。</p></div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    product_tab, privacy_tab, job_tab, help_tab = st.tabs(
        ["产品与分析", "隐私与 API Key", "求职核验", "已经遇到风险"]
    )
    with product_tab:
        _product_questions()
    with privacy_tab:
        _privacy_questions()
    with job_tab:
        _job_questions()
    with help_tab:
        _emergency_help()

    section_title("可以直接复制的反向核验问题", "专业的核验问题，比直接问“是不是骗子”更有效。", "❝")
    _question_kit()

    section_title("准备检查一条招聘信息？", "文字、链接和截图都可以从核验中心开始。", "🛡")
    if st.button("进入 AI 核验中心", type="primary", use_container_width=True):
        st.switch_page("pages/verify.py")

    st.markdown(
        """
        <footer class="ms-footer-note">
          Mindshield 心盾只提供教育性风险提示，不保证识别所有诈骗，也不替代警方、法律或政府部门意见。
        </footer>
        """,
        unsafe_allow_html=True,
    )


render()
