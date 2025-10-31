from setuptools import setup, find_packages

setup(
    name="multiwfn-vesta-interface",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # 没有额外依赖
    python_requires='>=3.6',  # 指定Python版本
    entry_points={
        'console_scripts': [
            'multiwfn-vesta=multiwfn_vesta.main:main',
        ],
    },
)