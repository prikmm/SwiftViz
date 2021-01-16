import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swiftviz",
    version="0.0.1",
    author="Priyam Mehta",
    author_email="priyam145@gmail.com",
    license="MIT",
    description="SwiftViz is a Package containing random classes for Swift EDA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com//prikmm//SwiftViz",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'seaborn', 'plotly'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.6',
)