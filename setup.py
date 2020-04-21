import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fantraxpy", # Replace with your own username
    version="0.0.1",
    author="Jay Hennessy",
    author_email="tjay.hennessy@gmail.com",
    description="This is an unofficial Fantrax API client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayHennessy/fantraxAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)