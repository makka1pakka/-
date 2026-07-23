<p align="center">
  <img src="./logo.jpeg" alt="Compliant Video Ops Logo" width="200" />
</p>

<h1 align="center">我的世界皓宸自动化模组</h1>
<p align="center">
  <em>YouTube / INS ➡️ Douyin 合规发布助手</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Video%20Processing-FFmpeg-orange?logo=ffmpeg&logoColor=white" alt="FFmpeg" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 项目简介

这是一个合规的视频处理与发布助手项目，旨在为内容创作者和运营团队提供安全、自动化的工作流。

### 🎯 核心目标

- **📥 自动拉取**：支持拉取你有授权的素材（或本地素材）。
- **🎬 本地处理**：本地进行视频处理（转码、尺寸适配、品牌水印标记）。
- **🛡️ 去重指纹**：自动生成去重指纹（SHA256、pHash），防止重复投放。
- **🚀 一键发布**：生成抖音发布包，供人工复核后一键发布。

> ⚠️ **合规声明**：本项目不包含也不建议用于：未授权搬运、去除他人水印、篡改 MD5 规避平台规则。请严格遵守各大平台的内容规范。

---

## 🛠️ 环境要求

| 项目 | 说明 |
|------|------|
| 💻 操作系统 | Windows / macOS / Linux |
| 🐍 Python | 3.11+ |
| ⚙️ FFmpeg | 确保命令行可用 `ffmpeg` |
| 📦 可选 | yt-dlp（用于授权地址下载） |

---

## 🚀 快速上手

### 2.1 克隆项目

```bash
git clone <你的项目仓库地址>
cd <你的项目文件夹名称>
```

### 2.2 安装依赖

建议使用虚拟环境进行隔离：

```bash
# 创建并激活虚拟环境 (以 Windows 为例)
python -m venv venv
.env\Scriptsctivate

# 安装项目依赖
pip install -r requirements.txt
```

### 2.3 启动服务（Windows）

```powershell
.
un.ps1
```

启动成功后，可通过以下地址访问：

- 🩺 **Health Check**: http://127.0.0.1:8000/health
- 📖 **Swagger API 文档**: http://127.0.0.1:8000/docs

---

## ⚙️ 配置说明

复制 `.env.example` 为 `.env`，可根据需求修改以下配置：

| 配置项 | 说明 |
|--------|------|
| `RAW_DIR` | 原始下载目录 |
| `PROCESSED_DIR` | 处理后目录 |
| `PUBLISH_DIR` | 发布包目录 |
| `BRAND_TEXT` | 视频左下角品牌标记 |

---

## 🌐 API 交互指南

本项目使用 FastAPI 构建，提供了自动化的交互式 API 文档。

### 4.1 如何使用 Swagger UI

1. 启动服务后，在浏览器访问 http://127.0.0.1:8000/docs。
2. 你会看到如下界面，包含所有可用的 API 接口：
   - **Assets**: 素材入库与管理
   - **Publish**: 发布包生成
3. 点击任意接口（如 `POST /assets/ingest`）展开详情。
4. 点击 **"Try it out"** 按钮。
5. 填写请求参数（如 `source_url`），然后点击 **"Execute"**。
6. 在下方的 **Response body** 中查看返回结果。

### 4.2 核心接口说明

#### 📥 素材入库

| 项目 | 内容 |
|------|------|
| **路径** | `POST /assets/ingest` |
| **功能** | 提交视频源地址（本地路径或网络链接），触发下载与处理流程。 |

**示例参数：**

```json
{
  "source_url": "D:/videos/demo.mp4",
  "source_platform": "self",
  "license_note": "self-owned",
  "owner_name": "your_name"
}
```

#### 📦 生成发布包

| 项目 | 内容 |
|------|------|
| **路径** | `POST /publish/prepare` |
| **功能** | 基于处理好的素材 ID，生成适配抖音的发布包（含视频与元数据）。 |

**示例参数：**

```json
{
  "asset_id": 1,
  "title": "今天的短视频",
  "hashtags": "#原创 #教程"
}
```

---

## 📂 项目结构

```text
src/
├── main.py                    # FastAPI 入口
├── config.py                  # 配置管理
├── db.py                      # 数据库初始化
├── models.py                  # 数据模型
├── schemas.py                 # 请求/响应模型
├── pipeline/
│   └── orchestrator.py        # 核心编排：下载 -> 处理 -> 指纹 -> 去重 -> 发布包
└── services/
    ├── downloader.py          # 下载器（yt-dlp / 本地复制）
    ├── video_processor.py     # FFmpeg 视频处理
    ├── fingerprint.py         # SHA256 + pHash 指纹生成
    └── publisher.py           # 发布包生成器
```

---

## 🌟 后续扩展建议

- 🔗 对接实际可用的抖音开放平台发布 API
- 🔄 增加任务队列（Celery / RQ）支持批量并发
- 🛡️ 增加审核规则（敏感词、音频版权、黑白名单）
- 📊 增加可视化前端和运营数据报表

---

<p align="center">
  <i>如果这个项目对你有帮助，欢迎点个 ⭐ Star 支持一下！</i>
</p>
