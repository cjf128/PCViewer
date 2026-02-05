import os
import sys

def resource_path(*relative_path):
    """
    获取资源的绝对路径，兼容开发环境和打包后的 exe。

    参数:
        relative_path: str 或多段路径，资源相对于项目根目录的路径
    返回:
        绝对路径字符串
    """
    if getattr(sys, "frozen", False):
        # 打包后的 exe，资源在临时目录
        base_path = sys._MEIPASS
    else:
        # 开发环境，以项目根目录为基准
        # 假设本文件在项目根目录下
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, *relative_path)
