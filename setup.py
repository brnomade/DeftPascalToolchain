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
        packages=setuptools.find_packages(),
        classifiers=(
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ),
)
