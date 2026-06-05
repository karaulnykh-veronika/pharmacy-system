from setuptools import setup, find_packages

setup(
    name="pharmacy-core",
    version="0.1.0",
    description="Reusable core module for pharmacy management system",
    author="karaulnykh-veronika",
    author_email="",
    packages=find_packages(where="packages"),
    package_dir={"": "packages"},
    install_requires=[],  # нет внешних зависимостей
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
