import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UbuntuBIOSSettingsChecker",
    version="0.0.1",
    author="Li-Hao Liao (Leon Liao)",
    author_email="lihow731@gmail.com",
    description="Provide a API to check BIOS setting for Ubuntu installer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lihow731/ubuntu-bios-settings-checker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPUv2 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)