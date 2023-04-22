import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

print(setuptools.find_packages())
setuptools.setup(
    name="pyclash",
    version="0.0.1",
    author="Maze",
    author_email="3257575985@qq.com",
    description=("A command line tools for linux like clash."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meet-slut/pyclash",
    project_urls={
        "Bug Tracker": "https://github.com/meet-slut/pyclash/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "clash = pyclash.cli:main",
        ]
    }
)