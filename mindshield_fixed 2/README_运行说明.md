# Mindshield 心盾·跳转修复版

这是一个面向香港、澳门及大湾区硕士毕业生的多页面招聘反诈 MVP。

## 页面

- Home 首页
- Verify AI 核验
- Report 风险报告
- Tactics 反诈知识库
- FAQ 使用帮助

## 第一次运行（macOS）

重点：必须打开整个 `mindshield_fixed` 文件夹，不要只打开一个 Python 文件。

1. 先在旧网站的终端按 `Control + C`，停止旧服务。
2. 把新 ZIP 解压成一个全新文件夹；不要直接覆盖旧版本。
3. 打开 VS Code。
4. 点击顶部菜单“文件 → 打开文件夹”。
5. 选择解压后的 `mindshield_fixed` 文件夹。
6. 点击“终端 → 新建终端”。
7. 确认终端提示符最后是 `mindshield_fixed %`，再逐行执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
python -m streamlit run app.py
```

这些命令的意思：

- 第 1 行：创建一个只属于本项目的 Python 小环境。
- 第 2 行：进入这个小环境。
- 第 3–4 行：安装网页、AI、网页提取和图片识别组件。
- 第 5 行：启动网站。

浏览器没有自动打开时，访问：

```text
http://localhost:8501
```

## 以后再次运行

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

停止网站：回到终端，同时按 `Control + C`。

## 如果出现“File does not exist”

这不是 Python 代码错误，而是终端所在的文件夹不对。先用 VS Code 打开整个 `mindshield_fixed` 文件夹，再新建终端。

## 如果浏览器仍显示旧的空白页

1. 确认旧终端已用 `Control + C` 停止。
2. 关闭旧的浏览器标签页。
3. 在新文件夹里重新运行 `python -m streamlit run app.py`。
4. 打开终端显示的新 `Local URL`。
5. 如果页面被浏览器缓存，按 `Command + Shift + R` 强制刷新。

## 使用顺序

1. 点击左上角侧栏按钮，输入 DeepSeek API Key。
2. 在首页点击进入 AI 核验中心。
3. 选择招聘文字、职位链接或聊天截图。
4. 检查提取出的文字。
5. 点击 `RUN AI AUDIT`。
6. 系统会自动打开风险报告页面。

## 安全提醒

- 不要把 API Key 写进 Python 文件或上传 GitHub。
- 上传截图前请遮盖身份证、护照、银行卡、验证码和家庭住址。
- AI 结果仅用于风险筛查，不是法律定性。
