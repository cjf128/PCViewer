# AGENTS.md — Viewer 开发者指南（项目定制版）

## 概述

Viewer 是基于 PySide6 的 PET/CT 医学影像查看与分析工具，包含影像读取、可视化、分割（使用 MedSAM2/SAM 变体）、以及影像管理与预处理功能。

本文件面向团队开发者与贡献者，涵盖：快速上手、依赖与运行、代码约定、常见开发任务、模型与资源管理，以及与 AI 代理/自定义指令相关的注意事项。

---

## 快速开始

安装（开发环境）：

```bash
pip install -e .
```

运行应用：

```bash
python main.py
```

配置虚拟环境并安装可选依赖（建议）：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 主要依赖（来自 pyproject.toml / requirements.txt）

- PySide6 >= 6.9
- numpy >= 1.26
- opencv-python >= 4.8
- onnxruntime >= 1.16
- pydicom >= 2.4
- pypinyin
- SimpleITK
- vtk (用于 3D 可视化)
- pyyaml

模型/检查点目录：`models/checkpoints/`（例如 MedSAM2 编码器/解码器 onnx 文件）

---

**重要说明**：涉及患者数据时务必遵守隐私与合规要求（脱敏、访问控制、日志审计）。

---

## 代码风格与约定

- 导入顺序：标准库 → 第三方库 → 本地模块。
- 本地模块尽量使用相对或基于项目根的显式导入（例如 `from app.configs import AppConfig`）。
- 命名：类 PascalCase；函数/变量 snake_case；常量 UPPER_SNAKE_CASE。
- 在公共 API 与模块边界处添加类型提示。
- 每个类保持关注点单一：文档字符串 → `__init__` → 属性 → 公共方法 → 私有方法。

错误与日志：使用 `scripts/logger.py` 提供的集中化日志函数，不要使用 print；针对外部依赖的操作（文件读取、模型加载）要有明确的异常处理与日志记录。

界面字符串使用中文；保持 Qt Designer 生成的 UI 文件放在 `ui/`，相应逻辑类放在 `widgets/`。

---

## GUI 开发与 UI 文件

- 将 Qt Designer 的 `.ui` 文件放入 `ui/`，对应的 Python UI 文件放入同目录（或通过生成脚本）。
- 窗口类通常继承自 `QMainWindow`/`QDialog` 并组合生成的 UI 类，例如在 `widgets/MainWindow.py` 中集成 `ui/MainWindow_ui.py`。
- 信号/槽的连接集中在初始化方法（如 `init_connectAction()`）。

---

## 多线程与后台任务

- 对于重型模型加载和推理（例如加载 ONNX 模型或执行大图像处理），应使用 `QThread` 或工作线程，并通过 Signal 返回结果给主线程以保持 UI 响应性。
- 在 `widgets/WorkerThread.py` 中实现可复用的线程类，尽量把 I/O 与 CPU 密集型任务放到后台。

---

## 模型与资源管理

- 模型文件放在 `models/checkpoints/`，加载逻辑在 `models/medsam2.py`、`models/sam2.py` 等模块中实现。
- 大模型建议延迟加载（按需）并在后台线程中初始化；提供进度与超时处理。
- 对于可重复实验，记录模型版本与推理配置（例如 ONNX runtime flags）。

---

## 项目结构（简要）

```
Viewer/
├── app/           # 应用启动、配置和模式
├── models/        # 模型加载与推理封装
├── scripts/       # 辅助脚本（logger、preprocess、sort_dicom）
├── ui/            # Qt Designer 的 UI 文件及生成的 Python UI
├── widgets/       # 界面逻辑与窗口部件
├── icons/         # 主题图标（dark/ light）
├── logs/          # 运行日志
├── models/checkpoints/  # 模型权重（ONNX）
├── main.py        # 程序入口
├── path.py        # 路径常量
└── requirements.txt / pyproject.toml
```

---

## 常见开发任务（速览）

- 运行应用：`python main.py`。
- 生成 UI：使用 `pyside6-uic`（或项目已有生成脚本）把 `.ui` 转为 Python。
- 添加新窗口：在 `widgets/` 新建类并在 `ui/` 增加对应 `.ui`，在 `MainWindow` 集成。

---

## 调试与测试

- 将日志级别配置为 `DEBUG` 以便排查问题；在关键模块加入可开关的详细日志。
- 对于模型推理与预处理，编写小型单元测试或脚本放在 `assert/` 或 `example/` 下以验证数据流与可重现性。

---

## AI 代理与自定义指令注意事项

- 本仓库提供给 AI 助手（例如用于代码改写、生成补丁等）的上下文应避免包含真实患者数据；测试示例请使用 `example/` 下的匿名数据集。
- 如果为 VS Code Copilot 或自定义 agent 编写 instruction 文件（例如 `AGENTS.md`、`.instructions.md`），请：
    - 在 `description` 中包含明确触发关键词，便于检索。
    - 避免使用宽泛的 `applyTo: "**"`，仅在确实全局适用时使用。
    - 保证 YAML frontmatter 格式正确（使用空格，不使用 tab）。

---

## 贡献与代码审查

- 在提交前确保通过静态检查（如 flake8/ruff）及基本单元测试。
- 代码变更应附带说明，界面改动附带截图或短录屏。

---

如果你希望我把本文件拆分为更小的 `CONTRIBUTING.md` / `DEVELOPMENT.md` / `MODEL_GUIDE.md`，或者把运行/打包说明写到 `README.md`，告诉我下一步需求。
### 依赖项

核心依赖（来自 pyproject.toml/setup.py）：

- PySide6 >= 6.9.1
- numpy >= 1.26.0
- opencv-python >= 4.8.0
- onnxruntime >= 1.16.0
- pydicom >= 2.4.3
- pypinyin >= 0.49.0
- SimpleITK >= 2.3.0
- vtk >= 9.2.6
- pyyaml >= 6.0.1

---

## 代码风格指南

### 导入约定

1. **标准库导入优先**，然后是第三方库，最后是本地模块：

   ```python
   import os
   import sys
   from pathlib import Path

   import cv2
   import numpy as np
   from PySide6.QtCore import Qt
   from PySide6.QtWidgets import QApplication

   from app.configs import AppConfig
   from widgets.MainWindow import MainWindow
   ```
2. **本地导入应使用相对导入**，基于项目结构：

   - `from app.configs import ...`
   - `from widgets.MainWindow import ...`
   - `from scripts.logger import ...`
3. **分组 Qt 导入**以提高可读性：

   ```python
   from PySide6.QtCore import Qt, Signal
   from PySide6.QtGui import QIcon, QImage, QPixmap
   from PySide6.QtWidgets import (
       QApplication,
       QDialog,
       QFileDialog,
       QMainWindow,
       QMessageBox,
   )
   ```

### 命名约定

- **类**：PascalCase（例如 `MainWindow`、`AppConfig`、`ConfigManager`）
- **函数/变量**：snake_case（例如 `setup_logger`、`log_info`、`config_manager`）
- **常量**：UPPER_SNAKE_CASE（例如 `MAX_LOG_FILES`、`LOG_FORMAT`）
- **私有方法/属性**：以下划线开头（例如 `_config`、`_init_ui`）

### 类型提示

在函数签名和变量声明中使用类型提示：

```python
def setup_logger(log_dir: Path = None, name: str = "Viewer") -> logging.Logger:
    ...

def load(self) -> AppConfig:
    ...

def log_info(message: str) -> None:
    ...
```

### 代码组织

1. **类结构**：遵循类中的顺序：

   - 类文档字符串
   - `__init__` 方法
   - 属性（`@property`）
   - 公共方法
   - 私有方法（以 `_` 开头）
   - 事件处理器
2. **保持方法专注**：每个方法应该只做好一件事
3. **使用数据类**处理配置和数据结构：

   ```python
   @dataclass
   class AppConfig:
       width: int = 1200
       height: int = 800
       theme: str = "dark"
   ```

### 错误处理

1. **使用 try/except 处理特定异常**：

   ```python
   try:
       with open(self._config_path, 'r', encoding='utf-8') as f:
           data = yaml.safe_load(f)
   except (FileNotFoundError, yaml.YAMLError):
       pass
   ```
2. **使用日志进行错误报告**，而不是 print 语句：

   ```python
   from scripts.logger import log_error, log_warning, log_info

   log_error(f"Failed to load file: {e}")
   log_warning("Please input original data first")
   ```
3. **显示用户友好的错误对话框**处理 GUI 错误：

   ```python
   QMessageBox.warning(self, "警告！", "请先输入原始数据！", QMessageBox.Ok)
   ```

### 日志记录

使用集中式日志模块（`scripts/logger.py`）：

```python
from scripts.logger import log_info, log_debug, log_warning, log_error, setup_logger

# 在应用启动时初始化日志
setup_logger()

# 使用适当的日志级别
log_info("应用程序启动")
log_debug(f"Debug info: {variable}")
log_warning("Warning message")
log_error(f"Error occurred: {e}")
```

### GUI 开发模式

1. **UI 文件**：从 Qt Designer 生成，存储在 `ui/` 目录
2. **窗口部件类**：同时继承自定义逻辑和生成的 UI 类：
   ```python
   class MainWindow(QMainWindow, Ui_MainWindow):
       def __init__(self, config: AppConfig, parent=None):
           super().__init__(parent)
           self.setupUi(self)
   ```
3. **信号/槽连接**：使用 Qt 的信号-槽机制进行事件处理
4. **模态对话框**：使用 `QDialog` 配合 `setWindowModality(Qt.WindowModal)`

### 多线程

使用 `QThread` 处理后台任务以保持 UI 响应：

```python
class WorkerThread(QThread):
    finished = Signal(...)  # 定义结果信号
  
    def run(self):
        # 后台工作
        self.finished.emit(result)
```

### 文件路径处理

使用 `pathlib.Path` 进行跨平台路径处理：

```python
from pathlib import Path
from path import CACHE_PATH, ICONS_PATH  # 项目特定的路径常量

cache_path = Path(self.cache_path)
data_folder = cache_path / patient_id
data_folder.mkdir(parents=True, exist_ok=True)
```

### 性能考虑

1. **缓存昂贵的计算**：如 MainWindow 中的 VTK actor 缓存
2. **尽可能使用 numpy 数组操作**而不是 Python 循环
3. **延迟加载重型模型**（例如在后台线程中加载 SAM 模型）

---

## 项目结构

```
Viewer/
├── app/               # 应用核心（configs、app.py、mode.py）
├── models/            # 机器学习模型（SAM2）
├── scripts/           # 工具脚本（logger、preprocess、sort_dicom）
├── ui/                # 从 Qt Designer 生成的 UI 文件
├── widgets/           # 自定义 Qt 窗口部件（MainWindow、Docker 面板）
├── stylesheet/        # QSS 主题文件（light.qss、dark.qss）
├── icons/             # 图标资源
├── logs/              # 日志文件
├── main.py            # 入口点
├── path.py            # 路径常量
├── pyproject.toml     # Poetry 配置
└── setup.py           # Setuptools 配置
```

---

## 常见开发任务

### 在开发环境中运行应用

```bash
python main.py
```

### 添加新窗口部件

1. 在 `widgets/` 目录中创建窗口部件类
2. 在 Qt Designer 中创建对应的 UI，保存到 `ui/`
3. 使用以下命令生成 Python UI：`pyside6-uci input.ui -o output.py`
4. 在 `MainWindow` 中导入并集成

### 添加新功能

1. 在顶部导入必要的模块
2. 如果需要，在 Qt Designer 中添加 UI 元素
3. 在 `init_connectAction()` 中连接信号/槽
4. 在适当的方法中实现逻辑
5. 添加错误处理和日志记录

---

## AI 代理注意事项

- 这是一个医学影像应用程序 - 确保任何更改都保持患者数据的机密性
- 应用程序的 UI 元素使用中文语言
- VTK 用于 3D 可视化
- 支持 DICOM 和 NIfTI 格式的医学图像
- SAM（Segment Anything Model）用于自动分割