import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knij",  # Replace with your own username
    version="1.0.1",
    author="Jacobtread",
    author_email="jacobtread@gmail.com",
    description=" KAMAR Notices Interface - A way to access notices from KAMAR in a bunch of languages (Python)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobtread/KNI-Py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
