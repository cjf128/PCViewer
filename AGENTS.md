# AGENTS.md - Viewer 开发者指南

## 项目概述

Viewer 是一款基于 PySide6 构建的 PET/CT 医学图像全身病灶检测软件。提供医学影像数据的图像分析、分割和管理功能。

---

## 构建、检查和测试命令

### 安装

```bash
# 使用 pip
pip install -e .

# 使用 Poetry
poetry install
```

### 运行应用程序

```bash
python main.py
```

### 测试

本项目使用 pytest 进行测试。

```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_filename.py

# 运行单个测试函数
pytest tests/test_filename.py::test_function_name

# 运行测试并显示详细输出
pytest -v
```

注意：当前仓库中没有测试文件。测试应添加在 `tests/` 目录中。

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

开发依赖：

- pytest >= 7.4.0

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