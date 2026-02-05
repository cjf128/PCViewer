import os
import logging
import time
import sys

def get_logger(log_dir):
    """配置日志记录器，像 nnU-Net 一样同时输出到控制台和文件"""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"train_{time.strftime('%Y%m%d_%H%M%S')}.log")
    
    logger = logging.getLogger("Train")
    logger.setLevel(logging.INFO)
    
    # 格式：2024-05-20 10:00:00 - INFO - 消息
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    # 文件句柄
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    
    # 控制台句柄
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
