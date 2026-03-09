# Viewer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/GUI-PySide6-informational.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](LICENSE)

Viewer 是一款鼻咽癌PET/CT图像全身病灶检测软件，提供了影像分析、分割和管理功能。

---

## 主要功能

- **文件管理**：支持导入、重命名、删除PET/CT数据
- **图像查看**：支持横断面、矢状面、冠状面和3D视图
- **图像分割**：支持手动绘制和SAM（Segment Anything Model）自动分割
- **数据存储**：将导入的文件路径记录到YAML配置文件
- **实时反馈**：运行SAM时显示进度弹窗

---

## 环境要求

- Python 3.8+（推荐Python 3.10）
- 支持 CT / PET DICOM（含 Siemens `.IMA`）和NIfTI格式

```bash
conda create -n viewer python=3.10
conda activate viewer
```

---

## 安装

### 使用pip安装

```bash
pip install -r requirements.txt
```

### 使用Poetry安装

```bash
pip install poetry
poetry install
```

---

## 运行

```bash
python main.py
```

---

## TODO
- [ ] infoDocker增加label区域的肿瘤负荷计算，MTV和TLG
- [ ] infoDocker增加xy坐标显示
- [ ] 添加快捷键设置
- [ ] 添加帮助信息
- [ ] 改为medsam2

---

## 使用说明

1. **导入数据**：点击"导入"按钮，选择PET和CT文件
2. **查看数据**：在图像区域查看不同视图的图像
3. **分割功能**：
   - 手动绘制：选择"绘制"工具，在图像上绘制
   - SAM分割：选择"SAM"工具，在图像上框选区域
4. **文件管理**：在"文件设置"面板中管理已导入的数据
   - 双击数据项重新导入
   - 右键点击数据项可以重命名或删除

---

## 开源协议

本项目采用 **Apache License 2.0** 开源协议。
在遵守许可证条款的前提下，允许自由使用、修改和分发。

---

## 免责声明

本软件仅用于科研与教学目的，
不作为临床诊断或治疗决策的直接依据。

---