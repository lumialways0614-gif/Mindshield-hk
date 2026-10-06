"""Shared presentation helpers for the Mindshield Streamlit application.

Only static, trusted markup is emitted by this module.  Any dynamic value that is
placed inside HTML must pass through :func:`safe_text` first.
"""

from __future__ import annotations

import base64
import html
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


APP_ROOT = Path(__file__).resolve().parent
BACKGROUND_IMAGE = APP_ROOT / "assets" / "hong-kong-night.png"


def safe_text(value: object) -> str:
    """Return an HTML-safe representation of ``value``.

    User supplied job text, URLs, model output and filenames must never be
    interpolated into ``unsafe_allow_html`` blocks without this helper.
    """

    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def safe_url(value: object) -> str:
    """Return an escaped HTTP(S) URL, or an empty string for unsafe schemes."""

    candidate = str(value or "").strip()
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return safe_text(candidate)


@lru_cache(maxsize=4)
def _image_data_uri(path: str) -> str:
    image_path = Path(path)
    if not image_path.is_file():
        return ""
    suffix = image_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def apply_theme() -> None:
    """Apply the shared night-Hong-Kong glassmorphism theme."""

    background = _image_data_uri(str(BACKGROUND_IMAGE))
    background_rule = f"url('{background}')" if background else "none"
    css = _THEME_CSS.replace("__BACKGROUND_IMAGE__", background_rule)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_intro(kicker: str, title: str, subtitle: str) -> None:
    """Render a consistent page heading using escaped text values."""

    st.markdown(
        f"""
        <section class="ms-page-intro">
          <div class="ms-kicker">{safe_text(kicker)}</div>
          <h1>{safe_text(title)}</h1>
          <p>{safe_text(subtitle)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = "", icon: str = "") -> None:
    """Render a compact section title."""

    icon_markup = f'<span class="ms-section-icon">{safe_text(icon)}</span>' if icon else ""
    subtitle_markup = f"<p>{safe_text(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="ms-section-heading">
          {icon_markup}
          <div><h2>{safe_text(title)}</h2>{subtitle_markup}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def resource_card(
    title: str,
    description: str,
    url: str,
    label: str = "访问官方网页 ↗",
    badge: str = "官方资源",
) -> None:
    """Render an external-resource card with a validated URL."""

    checked_url = safe_url(url)
    link = (
        f'<a class="ms-card-link" href="{checked_url}" target="_blank" '
        f'rel="noopener noreferrer">{safe_text(label)}</a>'
        if checked_url
        else ""
    )
    st.markdown(
        f"""
        <article class="ms-resource-card">
          <span class="ms-badge">{safe_text(badge)}</span>
          <h3>{safe_text(title)}</h3>
          <p>{safe_text(description)}</p>
          {link}
        </article>
        """,
        unsafe_allow_html=True,
    )


def notice(title: str, body: str, tone: str = "mint") -> None:
    """Render a safe informational callout."""

    tone_class = tone if tone in {"mint", "amber", "red", "blue"} else "mint"
    st.markdown(
        f"""
        <aside class="ms-notice ms-notice-{tone_class}">
          <strong>{safe_text(title)}</strong>
          <span>{safe_text(body)}</span>
        </aside>
        """,
        unsafe_allow_html=True,
    )


_THEME_CSS = r"""
:root {
  color-scheme: dark;
  --ms-bg: #06101f;
  --ms-panel: rgba(15, 31, 51, 0.68);
  --ms-panel-strong: rgba(11, 24, 42, 0.86);
  --ms-border: rgba(171, 218, 228, 0.24);
  --ms-border-strong: rgba(103, 234, 194, 0.58);
  --ms-text: #f5fbff;
  --ms-muted: #afc1ce;
  --ms-mint: #62e7b2;
  --ms-cyan: #62cfeb;
  --ms-amber: #ffc86b;
  --ms-red: #ff6e76;
  --ms-shadow: 0 24px 70px rgba(0, 7, 18, 0.42);
}

html, body, [class*="css"] {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI",
    "PingFang HK", "PingFang SC", "Noto Sans CJK TC", "Microsoft JhengHei", sans-serif;
}

[data-testid="stAppViewContainer"] {
  color: var(--ms-text);
  background:
    linear-gradient(180deg, rgba(2, 15, 30, 0.36), rgba(3, 11, 25, 0.88)),
    linear-gradient(110deg, rgba(0, 80, 111, 0.18), rgba(4, 17, 34, 0.38)),
    __BACKGROUND_IMAGE__ center center / cover fixed;
}

[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 32% 12%, rgba(65, 218, 188, 0.12), transparent 30%),
    radial-gradient(circle at 83% 56%, rgba(80, 164, 240, 0.13), transparent 34%);
  z-index: 0;
}

[data-testid="stMain"] { position: relative; z-index: 1; }
[data-testid="stHeader"] { background: rgba(4, 17, 32, 0.72); backdrop-filter: blur(16px); }
[data-testid="stToolbar"] { right: 1rem; }

.stMainBlockContainer,
.block-container {
  max-width: 1180px;
  padding-top: 2rem;
  padding-bottom: 4rem;
}

h1, h2, h3, p { color: inherit; }
h1, h2, h3 { letter-spacing: -0.025em; }
p, li { line-height: 1.7; }
a { color: var(--ms-mint); }

/* Streamlit navigation */
[data-testid="stSidebar"] {
  background: rgba(3, 14, 27, 0.88);
  border-right: 1px solid var(--ms-border);
  backdrop-filter: blur(18px);
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
  border-radius: 12px;
  color: #d9e7ef;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
  background: rgba(98, 231, 178, 0.10);
}

/* Inputs */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea {
  background: rgba(5, 17, 31, 0.76) !important;
  border-color: rgba(161, 208, 221, 0.25) !important;
  color: var(--ms-text) !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color: var(--ms-mint) !important;
  box-shadow: 0 0 0 2px rgba(98, 231, 178, 0.16) !important;
}

/* Buttons */
.stButton > button,
.stLinkButton > a,
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"] {
  min-height: 3rem;
  border-radius: 12px;
  border: 1px solid rgba(98, 231, 178, 0.62);
  color: #edfff9;
  background: linear-gradient(135deg, rgba(38, 128, 111, 0.66), rgba(24, 89, 107, 0.68));
  box-shadow: 0 9px 28px rgba(25, 185, 143, 0.12);
  font-weight: 700;
  transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
}
.stButton > button:hover,
.stLinkButton > a:hover {
  color: white;
  border-color: #8effd2;
  transform: translateY(-1px);
  box-shadow: 0 12px 32px rgba(25, 185, 143, 0.2);
}
.stButton > button:focus-visible,
.stLinkButton > a:focus-visible,
.ms-card-link:focus-visible {
  outline: 3px solid rgba(255, 200, 107, 0.95);
  outline-offset: 3px;
}

/* Tabs and expanders */
.stTabs [data-baseweb="tab-list"] {
  gap: .55rem;
  border-bottom: 1px solid var(--ms-border);
}
.stTabs [data-baseweb="tab"] {
  height: 3rem;
  color: var(--ms-muted);
  border-radius: 10px 10px 0 0;
}
.stTabs [aria-selected="true"] { color: var(--ms-mint) !important; }
.stExpander {
  background: rgba(10, 26, 43, 0.68);
  border: 1px solid var(--ms-border) !important;
  border-radius: 14px !important;
  overflow: hidden;
}

/* Shared components */
.ms-page-intro {
  padding: 1.1rem 0 1.3rem;
  text-align: center;
}
.ms-page-intro h1 {
  margin: .35rem 0 .4rem;
  color: #f5fffb;
  font-size: clamp(2.15rem, 5vw, 4.1rem);
  line-height: 1.08;
  text-shadow: 0 0 28px rgba(98, 231, 178, 0.17);
}
.ms-page-intro p {
  max-width: 720px;
  margin: 0 auto;
  color: var(--ms-muted);
  font-size: 1.04rem;
}
.ms-kicker {
  display: inline-flex;
  padding: .38rem .72rem;
  border: 1px solid rgba(98, 231, 178, .33);
  border-radius: 999px;
  color: var(--ms-mint);
  background: rgba(20, 79, 69, .28);
  font-size: .76rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.ms-glass {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--ms-border);
  border-radius: 22px;
  background: linear-gradient(145deg, rgba(37, 60, 79, .62), rgba(9, 23, 40, .78));
  box-shadow: var(--ms-shadow), inset 0 1px 0 rgba(255,255,255,.08);
  backdrop-filter: blur(20px) saturate(130%);
  -webkit-backdrop-filter: blur(20px) saturate(130%);
}
.ms-glass::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(115deg, rgba(255,255,255,.07), transparent 32%);
}
.ms-brandbar {
  display: flex;
  align-items: center;
  gap: .65rem;
  margin: -.45rem 0 .8rem;
  padding: .62rem .8rem;
  border: 1px solid rgba(152, 205, 218, .18);
  border-radius: 14px;
  background: rgba(5, 19, 34, .62);
  backdrop-filter: blur(14px);
}
.ms-brand-icon { font-size: 1.3rem; }
.ms-brandbar b { color: #f1fff9; letter-spacing: .08em; }
.ms-brandbar small { margin-left: .36rem; color: #99adba; }
.ms-system-status {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  margin-left: auto;
  color: #87dabb;
  font-size: .68rem;
  font-weight: 800;
  letter-spacing: .08em;
}
.ms-system-status i,
.ms-panel-title i {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--ms-mint);
  box-shadow: 0 0 10px rgba(98, 231, 178, .8);
}
.ms-page-heading {
  margin: .45rem 0 1rem;
  padding: clamp(1.25rem, 3vw, 2rem);
  text-align: center;
}
.ms-page-heading h1 {
  margin: .5rem 0 .35rem;
  color: #f5fffb;
  font-size: clamp(2rem, 4vw, 3.2rem);
}
.ms-page-heading p { margin: 0 auto; color: var(--ms-muted); }
.ms-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .45rem;
  padding: .55rem .65rem;
  border: 1px solid rgba(154, 205, 218, .18);
  border-radius: 10px;
  color: #b9c8d1;
  background: rgba(5, 19, 34, .62);
  font-size: .74rem;
  font-weight: 650;
}
.ms-status i { width: 7px; height: 7px; border-radius: 50%; }
.ms-status i.green { background: var(--ms-mint); box-shadow: 0 0 10px rgba(98, 231, 178, .75); }
.ms-status i.amber { background: var(--ms-amber); box-shadow: 0 0 10px rgba(255, 200, 107, .7); }
.ms-panel-title {
  display: flex;
  align-items: center;
  gap: .55rem;
  margin: 1.05rem 0 .65rem;
  color: #dff7ed;
  font-size: .78rem;
  font-weight: 850;
  letter-spacing: .1em;
}
.ms-rule { height: 1px; margin: 1.2rem 0; background: rgba(156, 205, 218, .18); }
.ms-section-heading {
  display: flex;
  align-items: center;
  gap: .8rem;
  margin: 2.25rem 0 .85rem;
}
.ms-section-heading h2 { margin: 0; font-size: 1.42rem; }
.ms-section-heading p { margin: .12rem 0 0; color: var(--ms-muted); font-size: .92rem; }
.ms-section-icon {
  display: grid;
  place-items: center;
  width: 2.4rem;
  height: 2.4rem;
  border: 1px solid rgba(98, 231, 178, .3);
  border-radius: 12px;
  background: rgba(98, 231, 178, .09);
}
.ms-badge {
  display: inline-flex;
  color: var(--ms-mint);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.ms-resource-card {
  min-height: 230px;
  padding: 1.2rem;
  border: 1px solid var(--ms-border);
  border-radius: 17px;
  background: linear-gradient(145deg, rgba(27, 51, 70, .72), rgba(8, 22, 38, .78));
  box-shadow: 0 15px 38px rgba(0, 8, 18, .2);
}
.ms-resource-card h3 { margin: .55rem 0 .4rem; font-size: 1.08rem; }
.ms-resource-card p { min-height: 5.1rem; margin: 0 0 .9rem; color: var(--ms-muted); font-size: .9rem; }
.ms-card-link {
  display: inline-flex;
  padding: .58rem .75rem;
  border: 1px solid rgba(98, 231, 178, .38);
  border-radius: 10px;
  color: #a2fbd7 !important;
  background: rgba(35, 118, 99, .22);
  font-size: .84rem;
  font-weight: 750;
  text-decoration: none !important;
}
.ms-notice {
  display: flex;
  flex-direction: column;
  gap: .25rem;
  margin: .8rem 0;
  padding: .9rem 1rem;
  border: 1px solid var(--ms-border);
  border-left-width: 4px;
  border-radius: 12px;
  background: rgba(8, 23, 40, .75);
}
.ms-notice span { color: var(--ms-muted); font-size: .9rem; line-height: 1.55; }
.ms-notice-mint { border-left-color: var(--ms-mint); }
.ms-notice-amber { border-left-color: var(--ms-amber); }
.ms-notice-red { border-left-color: var(--ms-red); }
.ms-notice-blue { border-left-color: var(--ms-cyan); }
.ms-mini-card {
  height: 100%;
  padding: .82rem .9rem;
  border: 1px solid var(--ms-border);
  border-radius: 13px;
  background: rgba(8, 24, 41, .74);
}
.ms-mini-card .ms-icon { font-size: 1.65rem; }
.ms-mini-card h3 { margin: .6rem 0 .3rem; font-size: 1.03rem; }
.ms-mini-card p { margin: 0; color: var(--ms-muted); font-size: .88rem; }
.ms-mini-card b { display: block; color: #eafbf5; font-size: .86rem; }
.ms-mini-card span { display: block; margin-top: .18rem; color: var(--ms-muted); font-size: .75rem; }
.ms-step-number {
  display: inline-grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  color: #052018;
  background: var(--ms-mint);
  font-size: .8rem;
  font-weight: 900;
}
.ms-chip-row { display: flex; flex-wrap: wrap; justify-content: center; gap: .45rem; }
.ms-chip {
  padding: .38rem .66rem;
  border: 1px solid rgba(155, 205, 218, .22);
  border-radius: 999px;
  color: #c8d9e3;
  background: rgba(8, 23, 39, .65);
  font-size: .76rem;
}
.ms-footer-note {
  margin-top: 2.5rem;
  padding-top: 1.15rem;
  border-top: 1px solid rgba(152, 200, 213, .16);
  color: #91a6b5;
  text-align: center;
  font-size: .78rem;
}

@media (max-width: 720px) {
  .stMainBlockContainer, .block-container { padding: 1.15rem 1rem 3rem; }
  .ms-page-intro h1 { font-size: 2.2rem; }
  .ms-resource-card { min-height: auto; }
  .ms-resource-card p { min-height: auto; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
}
"""
