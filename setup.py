# @Time : 2024/8/18 下午2:29
# @Author : hesheng
# @File : setup.py
# @desc:

from setuptools import find_packages,setup
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()
setup(
    name="ApiProxy",
    version="0.0.4",
    description="Proxy server, used for browser proxy access, supports dynamic proxy switching",
    url="https://github.com/test741123/ApiProxy",
    author="hesheng",
    author_email="1296602221@qq.com",
    python_requires=">=3.7",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ApiProxy': ['dependencies/*']
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "requests>=2.28.1"
    ],
)