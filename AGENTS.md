# AGENTS.md - Developer Guide for Viewer

## Project Overview

Viewer is a PET/CT medical image whole-body lesion detection software built with PySide6. It provides image analysis, segmentation, and management functionality for medical imaging data.

---

## Build, Lint, and Test Commands

### Installation

```bash
# Using pip
pip install -e .

# Using Poetry
poetry install
```

### Running the Application

```bash
python main.py
```

### Testing

This project uses pytest for testing.

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_filename.py

# Run a single test function
pytest tests/test_filename.py::test_function_name

# Run tests with verbose output
pytest -v
```

Note: Currently, there are no test files in this repository. Tests should be added in a `tests/` directory.

### Dependencies

Core dependencies (from pyproject.toml/setup.py):
- PySide6 >= 6.9.1
- numpy >= 1.26.0
- opencv-python >= 4.8.0
- onnxruntime >= 1.16.0
- pydicom >= 2.4.3
- pandas >= 2.1.0
- pypinyin >= 0.49.0
- SimpleITK >= 2.3.0
- vtk >= 9.2.6
- pyyaml >= 6.0.1

Dev dependencies:
- pytest >= 7.4.0

---

## Code Style Guidelines

### Import Conventions

1. **Standard library imports first**, then third-party, then local:
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

2. **Local imports should use relative imports** based on the project structure:
   - `from app.configs import ...`
   - `from widgets.MainWindow import ...`
   - `from scripts.logger import ...`

3. **Group Qt imports** for readability:
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

### Naming Conventions

- **Classes**: PascalCase (e.g., `MainWindow`, `AppConfig`, `ConfigManager`)
- **Functions/variables**: snake_case (e.g., `setup_logger`, `log_info`, `config_manager`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_LOG_FILES`, `LOG_FORMAT`)
- **Private methods/attributes**: prefix with underscore (e.g., `_config`, `_init_ui`)

### Type Hints

Use type hints for function signatures and variable declarations:

```python
def setup_logger(log_dir: Path = None, name: str = "Viewer") -> logging.Logger:
    ...

def load(self) -> AppConfig:
    ...

def log_info(message: str) -> None:
    ...
```

### Code Organization

1. **Class structure**: Follow the order within classes:
   - Class docstring
   - `__init__` method
   - Properties (`@property`)
   - Public methods
   - Private methods (prefixed with `_`)
   - Event handlers

2. **Keep methods focused**: Each method should do one thing well

3. **Use dataclasses** for configuration and data structures:
   ```python
   @dataclass
   class AppConfig:
       width: int = 1200
       height: int = 800
       theme: str = "dark"
   ```

### Error Handling

1. **Use try/except with specific exceptions**:
   ```python
   try:
       with open(self._config_path, 'r', encoding='utf-8') as f:
           data = yaml.safe_load(f)
   except (FileNotFoundError, yaml.YAMLError):
       pass
   ```

2. **Use logging for error reporting** instead of print statements:
   ```python
   from scripts.logger import log_error, log_warning, log_info
   
   log_error(f"Failed to load file: {e}")
   log_warning("Please input original data first")
   ```

3. **Show user-friendly error dialogs** for GUI errors:
   ```python
   QMessageBox.warning(self, "警告！", "请先输入原始数据！", QMessageBox.Ok)
   ```

### Logging

Use the centralized logging module (`scripts/logger.py`):

```python
from scripts.logger import log_info, log_debug, log_warning, log_error, setup_logger

# Initialize logger at app startup
setup_logger()

# Use appropriate log levels
log_info("应用程序启动")
log_debug(f"Debug info: {variable}")
log_warning("Warning message")
log_error(f"Error occurred: {e}")
```

### GUI Development Patterns

1. **UI files**: Generated from Qt Designer, stored in `ui/` directory
2. **Widget classes**: Inherit from both custom logic and generated UI class:
   ```python
   class MainWindow(QMainWindow, Ui_MainWindow):
       def __init__(self, config: AppConfig, parent=None):
           super().__init__(parent)
           self.setupUi(self)
   ```
3. **Signal/Slot connections**: Use Qt's signal-slot mechanism for event handling
4. **Modal dialogs**: Use `QDialog` with `setWindowModality(Qt.WindowModal)`

### Threading

Use `QThread` for background tasks to keep UI responsive:

```python
class WorkerThread(QThread):
    finished = Signal(...)  # Define signals for results
    
    def run(self):
        # Background work here
        self.finished.emit(result)
```

### File Path Handling

Use `pathlib.Path` for cross-platform path handling:

```python
from pathlib import Path
from path import CACHE_PATH, ICONS_PATH  # Project-specific path constants

cache_path = Path(self.cache_path)
data_folder = cache_path / patient_id
data_folder.mkdir(parents=True, exist_ok=True)
```

### Performance Considerations

1. **Cache expensive computations**: Like the VTK actor cache in MainWindow
2. **Use numpy array operations** instead of Python loops when possible
3. **Lazy load heavy models** (e.g., SAM model loaded in background thread)

---

## Project Structure

```
Viewer/
├── app/               # Application core (configs, app.py, mode.py)
├── models/            # ML models (SAM2)
├── scripts/           # Utility scripts (logger, preprocess, sort_dicom)
├── ui/                # Generated UI files from Qt Designer
├── widgets/           # Custom Qt widgets (MainWindow, Docker panels)
├── stylesheet/        # QSS theme files (light.qss, dark.qss)
├── icons/             # Icon assets
├── logs/              # Log files
├── main.py            # Entry point
├── path.py            # Path constants
├── pyproject.toml     # Poetry config
└── setup.py           # Setuptools config
```

---

## Common Development Tasks

### Running the app in development
```bash
python main.py
```

### Adding a new widget
1. Create widget class in `widgets/` directory
2. Create corresponding UI in Qt Designer, save to `ui/`
3. Generate Python UI with: `pyside6-uci input.ui -o output.py`
4. Import and integrate in `MainWindow`

### Adding a new feature
1. Import necessary modules at the top
2. Add UI elements in Qt Designer if needed
3. Connect signals/slots in `init_connectAction()`
4. Implement logic in appropriate methods
5. Add error handling and logging

---

## Notes for AI Agents

- This is a medical imaging application - ensure any changes maintain patient data confidentiality
- The app uses Chinese language for UI elements
- VTK is used for 3D visualization
- DICOM and NIfTI formats are supported for medical images
- SAM (Segment Anything Model) is used for auto-segmentation
