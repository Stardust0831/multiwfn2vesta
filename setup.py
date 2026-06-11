from setuptools import setup, find_packages

setup(
    name="multiwfn-vesta-interface",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # 没有额外依赖
    python_requires='>=3.7',  # 指定Python版本
    entry_points={
        'console_scripts': [
            'multiwfn-vesta=multiwfn_vesta.main:main',
            'multiwfn2vesta=multiwfn2vesta.cli:main',
            'multiwfn2vesta-discover=multiwfn2vesta.executables:main',
            'multiwfn2vesta-abacus-molden=multiwfn2vesta.abacus_molden:main',
            'multiwfn2vesta-molden-check=multiwfn2vesta.molden_check:main',
            'multiwfn2vesta-cube-vesta=multiwfn2vesta.cube_vesta:main',
            'multiwfn2vesta-cube-preset=multiwfn2vesta.cube_preset:main',
            'multiwfn2vesta-cube-arith=multiwfn2vesta.cube_arith:main',
            'multiwfn2vesta-iri-run=multiwfn2vesta.multiwfn_iri:main',
            'multiwfn2vesta-igmh-run=multiwfn2vesta.multiwfn_igmh:main',
            'multiwfn2vesta-igm-run=multiwfn2vesta.multiwfn_igmh:main_igm',
            'multiwfn2vesta-migm-run=multiwfn2vesta.multiwfn_igmh:main_migm',
            'multiwfn2vesta-aigm-run=multiwfn2vesta.multiwfn_aigm:main',
            'multiwfn2vesta-amigm-run=multiwfn2vesta.multiwfn_aigm:main_amigm',
            'multiwfn2vesta-grid-run=multiwfn2vesta.multiwfn_grid:main',
            'multiwfn2vesta-fukui-run=multiwfn2vesta.multiwfn_fukui:main',
            'multiwfn2vesta-stm-run=multiwfn2vesta.multiwfn_stm:main',
            'multiwfn2vesta-domain-run=multiwfn2vesta.multiwfn_domain:main',
            'multiwfn2vesta-multiwfn-atom-color=multiwfn2vesta.multiwfn_atom_table:main',
            'multiwfn2vesta-aim-run=multiwfn2vesta.multiwfn_aim:main',
            'multiwfn2vesta-aim-pdb=multiwfn2vesta.aim_vesta:main',
            'multiwfn2vesta-aim-igmh=multiwfn2vesta.aim_igmh_vesta:main',
            'multiwfn2vesta-examples=multiwfn2vesta.examples:main',
        ],
    },
)
