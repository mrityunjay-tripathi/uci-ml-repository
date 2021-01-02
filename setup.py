import setuptools
with open("README.md", "r") as f:
    long_description = f.read()
setuptools.setup(
    name='uci-ml-datasets',  
    version='0.1',
    # scripts=['downloader.py'] ,
    author="Mrityunjay Tripathi",
    author_email="mrityunjay2668@gmail.com",
    description="A utility to download all the datasets from UCI ML Repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrityunjayTripathi/uci-ml-repository",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: Apache License 2.0",
                 "Operating System :: OS Independent",
                ])
