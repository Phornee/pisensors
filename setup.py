import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PiSensors",
    version="0.0.3",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Sensors script for Temperature & Humidity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/PiSensors",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'baseutils_phornee>=0.0.3',
        'dbutils_phornee>0.0.3',
        'adafruit-circuitpython-dht>=3.5.1'
    ],
    python_requires='>=3.6',
)