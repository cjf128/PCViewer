from setuptools import setup, find_packages

setup(
    name="viewer",
    version="0.1.0",
    description="PET/CT图像全身病灶检测软件",
    author="Jinfr",
    author_email="2998747137@qq.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PySide6>=6.9.1",
        "numpy>=1.26.0",
        "opencv-python>=4.8.0",
        "onnxruntime>=1.16.0",
        "pydicom>=2.4.3",
        "pandas>=2.1.0",
        "pypinyin>=0.49.0",
        "SimpleITK>=2.3.0",
        "vtk>=9.2.6",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "viewer=main:main",
        ],
    },
)