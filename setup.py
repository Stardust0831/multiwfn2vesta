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
            'multiwfn2vesta=multiwfn2vesta.cli:main',
            'multiwfn2vesta-discover=multiwfn2vesta.executables:main',
            'multiwfn2vesta-abacus-molden=multiwfn2vesta.abacus_molden:main',
            'multiwfn2vesta-molden-check=multiwfn2vesta.molden_check:main',
            'multiwfn2vesta-cube-vesta=multiwfn2vesta.cube_vesta:main',
            'multiwfn2vesta-aim-run=multiwfn2vesta.multiwfn_aim:main',
            'multiwfn2vesta-aim-pdb=multiwfn2vesta.aim_vesta:main',
            'multiwfn2vesta-aim-igmh=multiwfn2vesta.aim_igmh_vesta:main',
        ],
    },
)
