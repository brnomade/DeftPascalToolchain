import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="DeftPascalToolchain",
        version="0.1.0",
        author="andre ballista",
        author_email="https://github.com/brnomade/DeftPascalToolchain/issues",
        description="A Python tool chain to automate the build (compile & link) of Deft Pascal projects for the Tandy (Radio Shack) TRSCOLOR (a.k.a. CoCo) ",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/brnomade/DeftPascalToolchain",
        packages=["dptc"],
        install_requires=['configargparse'],
        scripts=['utils/dptcc.py', 'utils/dptcl.py'],
        package_data={'dptc': ['deft_pascal_compile_script_template.lua', "deft_pascal_link_script_template.lua"]},
        include_package_data=True,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
)
