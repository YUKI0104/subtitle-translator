---
name: stylekit-generator
description: "基于 StyleKit 120 种设计风格，一键生成 DESIGN.md 设计规范文件、UI 组件库展示页、以及完整落地页。触发词：设计风格生成、生成风格页面、StyleKit、stylekit、风格组件库、设计规范生成、风格展示页、组件库展示、DESIGN.md 生成、风格落地页、挑选风格、选风格做页面、用 StyleKit 生成、generate style、style generator、UI kit generator。工作流：当用户唤起此技能时，首先展示 4 大类别让用户选择，然后列出类别下的所有风格供用户挑选，最后基于用户选取的具体风格依次生成 3 个交付物。"
---

# StyleKit Generator — 风格页面生成器

> **版本说明**: 此版本为小红书兼容版，所有文件仅使用 `.md` 和 `.txt` 格式。StyleKit 风格数据已内置在 `references/style-prompts.txt` 中，无需安装其他依赖技能。

## 概述

基于 StyleKit 120 种设计风格数据，通过交互式选择完成风格定位，自动生成：
1. **DESIGN.md** — 设计规范文件（设计哲学、色彩系统、排版规则、组件规范、Do/Don't）
2. **组件库展示页** — 3:4 比例卡片式组件展示 HTML（14 种组件 + 5 色色板）
3. **落地页** — 完整品牌落地页 HTML（Hero + Features + CTA）

所有脚本和数据文件均以 `.txt` 格式提供（Python 脚本重命名为 `.txt`），运行时使用 `python3` 命令即可，Python 不限制文件扩展名。

## 文件结构

```
stylekit-generator/
├── SKILL.md                      # 本文件（技能定义 + 工作流说明）
├── scripts/
│   ├── list_categories.txt       # 列出 4 大类及风格数量
│   ├── list_styles.txt           # 列出某类别下的所有风格
│   └── fetch_style.txt           # 提取指定风格的完整数据 JSON
└── references/
    ├── DESIGN_TEMPLATE.md         # DESIGN.md 生成模板
    ├── COMPONENT_SPEC.md          # 组件展示页规范
    ├── LANDING_SPEC.md            # 落地页规范
    └── style-prompts.txt          # StyleKit 120 种风格完整数据（内置，无外部依赖）
```

## 交互工作流

严格按以下 3 步执行，每步等待用户确认后再进入下一步。

### 第 1 步：选择大类

运行脚本展示 4 个大类：

```bash
python3 {技能目录}/scripts/list_categories.txt
```

将其输出以清晰格式呈现给用户，让用户从以下 4 类中选择：

| 类别 | 标签 | 典型风格 |
|------|------|---------|
| expressive | 表现力 | 赛博朋克霓虹、故障艺术、蒸汽朋克、波普艺术… |
| modern | 现代 | 玻璃拟态、科幻HUD、Apple流动玻璃、仪表盘… |
| retro | 复古 | 像素艺术、合成波、孟菲斯、VHS美学… |
| minimal | 极简 | 侘寂风、北欧极简、编辑杂志风、水墨画风… |

**重要**: 只需用户在 4 个大类中选择一个。用简短的分类描述帮助用户决策，但不要列出所有风格名——那留给第 2 步。

### 第 2 步：选择风格

根据用户在第 1 步选择的类别，运行：

```bash
python3 {技能目录}/scripts/list_styles.txt {category}
```

将输出以清晰编号列表呈现给用户。每行显示格式：`编号. [slug] 中文名 (关键词标签)`。

如果风格数量超过 20 个，可以分组展示以便阅读。让用户通过编号或 slug 选择具体风格。

### 第 3 步：生成交付物

用户选定风格后，运行脚本获取完整风格数据：

```bash
python3 {技能目录}/scripts/fetch_style.txt {slug}
```

脚本返回 JSON 格式的完整风格数据，包含：
- `name`, `nameEn`, `category`, `tags`, `keywords`
- `colors` (primary, secondary, accent[])
- `philosophy`, `doList`, `dontList`, `aiRules`
- `components` (button, card, input, nav, hero, footer 等模板代码)
- `examplePrompts`

拿到数据后，**顺序生成以下 3 个文件**。每生成一个文件后告知用户进度，但不需要等待确认——直接继续生成下一个。

#### 3a. DESIGN.md

文件命名: `{slug}-DESIGN.md`

内容结构（参考 `references/DESIGN_TEMPLATE.md`）：

```markdown
# {风格中文名} ({风格英文名}) — 设计规范

## 设计哲学
{从 philosophy 字段提取，保持原文}

## 色彩系统
| 角色 | 色值 | 预览 |
|------|------|------|
| 主色 | {colors.primary} | ██ |
| 辅色 | {colors.secondary} | ██ |
| 强调色 | {colors.accent 逐个列出} | ██ ██ ██ |

## 排版规范
- 根据 tags/keywords/aiRules 推断字体策略
- 字号阶梯: h1/h2/h3/body/caption
- 字重映射
- 行高规则

## 组件规范
从 components 字段的 JSX 代码中提取每个组件的关键 CSS 类名和参数：
- Button: 尺寸、圆角、边框样式、hover/active 行为
- Card: 背景、模糊度、边框发光参数、角标装饰
- Input: 边框色、focus 光晕、placeholder 样式
- Navigation: 高度、分割线、状态指示器
- 其他可用组件按相同方式记录

## Do ✅
{从 doList 提取，转为 Markdown 列表}

## Don't ❌
{从 dontList 提取，转为 Markdown 列表}

## AI Rules
{aiRules 原文保留}
```

#### 3b. 组件库展示页

文件命名: `{slug}-components.html`

**页面规范**:
- 3:4 比例容器 (750x1000px)，白色/浅色背景
- 标题：风格名称 + 分类标签
- **必须包含以下 14 种组件**：

| # | 组件 | 说明 |
|---|------|------|
| 1 | Button Primary | 主按钮，含 hover/active 态 |
| 2 | Button Secondary | 次要按钮 |
| 3 | Button Outline | 描边按钮 |
| 4 | Button Ghost | 幽灵按钮 |
| 5 | Input Search | 搜索输入框，含图标和焦点态 |
| 6 | Toggle | On/Off 开关 |
| 7 | Content Card | 内容卡片，含标题+描述+装饰 |
| 8 | Progress Circle | 圆形进度条 |
| 9 | Progress Bar | 长条形进度条 |
| 10 | Tabs | 选项卡切换 |
| 11 | Badge | 徽标/标签 |
| 12 | Navigation Bar | 导航栏 |
| 13 | Color Palette | 5 色色板 |
| 14 | Accordion | 手风琴折叠面板 |

- 严格按照 `aiRules` 的 MUST USE / MUST AVOID 规则实现
- 使用 Tailwind CSS CDN
- 自行发挥补全 StyleKit 数据中未提供的组件（Toggle、Progress、Tabs、Badge、Accordion 等），但严格遵循该风格的色彩、圆角、阴影、动效规则
- 不从 StyleKit 数据中随意发散——未定义的组件应从 aiRules 中推断参数

#### 3c. 落地页

文件命名: `{slug}-landing.html`

**页面结构**（自上而下）:
1. **Navigation Bar** — 品牌标识 + 导航链接 + CTA 按钮
2. **Hero Section** — 大标题 + 副标题 + 主 CTA 按钮 + 视觉元素
3. **Features Grid** — 3-6 个特性卡片
4. **Stats / Social Proof** — 数据指标或客户 Logo
5. **CTA Section** — 行动号召区域
6. **Footer** — 链接 + 版权信息

**设计约束**:
- 严格按照 `aiRules` 的 MUST USE / MUST AVOID 规则
- 遵循 `doList` / `dontList` 中的所有条目
- 响应式设计（移动端 + 桌面端）
- 所有动效使用 `motion-reduce:transition-none` 支持无障碍
- 使用 Tailwind CSS CDN
- 自行发挥合理补全页面内容（文案、图片示意等），但视觉规则不得偏离

## 生成原则

1. **严格遵循设计规范**: 色彩、圆角、阴影、字体、动效参数必须与 StyleKit 数据一致
2. **AI Slop 防范**: 禁止紫蓝渐变、禁止 emoji 图标、禁止过度光晕、禁止无意义装饰
3. **质量优先**: 宁可多花 token 把组件做细致，也不要凑合拼凑
4. **完整性**: 14 个组件一个不能少，落地页 6 个 section 一个不能少
5. **无障碍**: focus-visible、prefers-reduced-motion、语义化 HTML、44px 触控目标
