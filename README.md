> **免责声明**
> 本项目为粉丝自制作品，与 Atlus Co., Ltd. 或 SEGA Corporation 无关，未经其认可或赞助。
> 本仓库中的所有视觉素材均为作者原创。视觉风格受游戏《Persona 3》启发，但不包含任何
> 来自游戏的受版权保护的素材、商标或专有材料。
>
> *Persona 3* 及 *Persona* 系列为 Atlus Co., Ltd. 的商标。

[English](./README.en.md) | **中文**

# P3 Moonlight — Persona 3 风格 fcitx5 输入法皮肤

受《Persona 3》UI 风格启发的 fcitx5 输入法皮肤。

- 深蓝色矩形输入面板
- 选中候选为青色矩形 + 黑色文字
- 仅使用 `panel.svg` 与 `highlight.svg` 两个矢量资源
- 所有 SVG 素材由 `scripts/generate_assets.py` 参数化生成
- 可安全开源分发（不包含任何官方游戏素材）

## 预览

![P3 Moonlight fcitx5 皮肤预览](./docs/preview.png)

## 安装

```bash
# 1. 克隆或下载本仓库

# 2. 生成素材（可选 —— dist/ 下已有预生成文件）
python scripts/generate_assets.py

# 3. 复制皮肤到 fcitx5 主题目录
mkdir -p ~/.local/share/fcitx5/themes/
cp -r dist/p3-skin ~/.local/share/fcitx5/themes/p3-moonlight

# 4. 设置主题
# 方式 A：使用 fcitx5-configtool
fcitx5-configtool
#    → 附加组件 → 经典用户界面 → 主题 → 选择 "P3 Moonlight"

# 方式 B：直接编辑配置文件
# ~/.config/fcitx5/conf/classicui.conf
# Theme=p3-moonlight
# DarkTheme=p3-moonlight

# 5. 重启 fcitx5
fcitx5 -r
```

## 推荐字体

皮肤本身不捆绑字体。要获得最佳效果，推荐安装 **M+ Fonts**：

```bash
# Fedora
sudo dnf install mplus-1c-fonts mplus-1m-fonts

# Arch Linux
sudo pacman -S otf-mplus
```

然后在 `~/.config/fcitx5/conf/classicui.conf` 中设置：

```ini
Font="M+ 1c bold 13"
MenuFont="M+ 1c bold 13"
TrayFont="M+ 1c bold 10"
```

M+ Fonts 风格最接近 Persona 3 官方使用的 Rodin / Skip 的 Square Gothic 感。

## 开发

编辑 `scripts/generate_assets.py` 可调整颜色、面板尺寸等参数：

```bash
python scripts/generate_assets.py
cp -r dist/p3-skin ~/.local/share/fcitx5/themes/p3-moonlight
fcitx5 -r
```

## 项目结构

```text
p3-skin/
├── scripts/
│   └── generate_assets.py      # 参数化 SVG 生成器
├── dist/
│   └── p3-skin/                # 可直接安装的 fcitx5 主题
│       ├── theme.conf
│       ├── panel.svg           # 输入面板背景
│       └── highlight.svg       # 选中候选高亮
├── docs/
│   └── preview.png             # 截图预览
├── images/
│   └── result.jpg              # 风格参考图
├── README.md                   # 中文
└── README.en.md                # 英文
```

## 许可证

MIT 许可证。详见 [LICENSE](./LICENSE)。
