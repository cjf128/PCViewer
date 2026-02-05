# NViewer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/GUI-PySide6-informational.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](LICENSE)

NViewer 是一款面向鼻咽癌（Nasopharyngeal Carcinoma, NPC）研究场景的
PET/CT 桌面影像分析与分割工具。

系统集成了从原始 DICOM 数据处理、PET SUV 定量计算、多模态融合可视化，
到基于 nnU-Net 的自动分割完整流程，适用于医学影像科研与
计算机辅助分析任务。

---

## 环境要求

- Python 3.10（推荐）
- 支持 CT / PET DICOM（含 Siemens `.IMA`）

```bash
conda create -n nviewer python=3.10
conda activate nviewer
```

---

## 安装




---

## 运行

```bash
python main.py
```

---

## 项目结构

```text
NViewer/
├── checkpoints/        nnU-Net 训练模型权重
├── data/
│   ├── cache/          DICOM 处理与转换缓存
│   └── segmentation/   分割结果（Mask）输出目录
├── scripts/            影像预处理与格式转换核心逻辑
├── ui/                 Qt Designer 界面资源
├── widgets/            PySide6 自定义界面组件
├── icons/              静态资源
└── main.py             程序主入口
```

---

## 开源协议

本项目采用 **Apache License 2.0** 开源协议。
在遵守许可证条款的前提下，允许自由使用、修改和分发。

---

## 免责声明

本软件仅用于科研与教学目的，
不作为临床诊断或治疗决策的直接依据。
