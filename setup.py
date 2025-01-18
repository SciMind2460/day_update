from setuptools import setup, find_packages

setup(
    name="dayupdate",
    version="1.0.0",
    description="A script that syncs a daily test update.",
    author="Kurt Heiritz",
    author_email="saarthkarkera@gmail.com",
    url="https://github.com/SciMind2460/chronos",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "requests>=2.32.3"
    ],
    classifiers=[
        "Praogramming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
