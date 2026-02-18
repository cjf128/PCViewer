import logging
import time
import sys
from pathlib import Path

_logger = None

def setup_logger(log_dir=None, name="Viewer"):
    """配置全局日志记录器，同时输出到控制台和文件"""
    global _logger
    
    if _logger is not None:
        return _logger
    
    if log_dir is None:
        log_dir = Path(__file__).resolve().parent.parent / "logs"
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"viewer_{time.strftime('%Y%m%d_%H%M%S')}.log"
    
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    fh = logging.FileHandler(str(log_file), encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    
    _logger.addHandler(fh)
    _logger.addHandler(sh)
    
    return _logger

def get_logger():
    """获取全局日志记录器"""
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger

def log_info(message):
    """记录信息级别日志"""
    get_logger().info(message)

def log_debug(message):
    """记录调试级别日志"""
    get_logger().debug(message)

def log_warning(message):
    """记录警告级别日志"""
    get_logger().warning(message)

def log_error(message):
    """记录错误级别日志"""
    get_logger().error(message)
