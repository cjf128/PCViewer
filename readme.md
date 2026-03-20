# Viewer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/GUI-PySide6-informational.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)](LICENSE)

Viewer 是一款PET/CT图像全身病灶检测软件，提供了影像分析、分割和管理功能。

---

## 主要功能

- **文件管理**：支持导入、重命名、删除PET/CT数据
- **图像查看**：支持横断面、矢状面、冠状面和3D视图
- **图像分割**：支持手动绘制和SAM（Segment Anything Model）自动分割
- **数据存储**：将导入的文件路径记录到YAML配置文件
- **实时反馈**：运行SAM时显示进度弹窗

---

## 环境要求

- Python 3.12+

### 使用pip安装

```bash
pip install -r requirements.txt
```

---

## TODO

- [ ] infoDocker增加label区域的肿瘤负荷计算，MTV和TLG
- [ ] infoDocker增加xy坐标显示，label显示，数值显示
- [ ] 添加快捷键设置
- [ ] 添加帮助信息
- [ ] 添加SAM Med3D的单点提示
- [ ] 窗宽窗位预设，PET/CT切换
- [ ] 样式表设置
- [X] 运行分割时的弹窗
- [ ] 版本更新拉取
- [ ] 图像左上角加文件名
- [ ] 图像单PT和单CT模式
- [ ] imageDocker添加colorbar选择
- [ ] 3D建模与透明度同步
- [ ] 拖动文件进入软件
- [ ] 标注导入线性重采样
- [ ] CT与PET的不同种维度

---

## 开源协议

本项目采用 **Apache License 2.0** 开源协议。
在遵守许可证条款的前提下，允许自由使用、修改和分发。

---

## 免责声明

本软件仅用于科研与教学目的，
不作为临床诊断或治疗决策的直接依据。

---
