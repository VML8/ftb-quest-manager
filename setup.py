from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ftb-quest-viewer",
    version="1.0.0",
    author="FTB Quest Viewer Developer",
    author_email="developer@example.com",
    description="A Python tool for viewing and navigating FTB (Feed The Beast) quest data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ftb-quest-viewer",
    packages=find_packages(),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ftb-quest-viewer=cli:main",
            "ftb-viewer=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
