import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DLex-DeaL",
    version="0.0.2",
    author="Dai Ling",
    author_email="dialing57@163.com",
    description="DL's Lex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dailing57/DLex",
    project_urls={
        "Bug Tracker": "https://github.com/dailing57/DLex/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
