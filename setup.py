from setuptools import setup, find_packages

VERSION="0.1.0.dev0"

setup(
    name="Sensors-Balloon",
    version=VERSION,
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=["RPI.GPIO", "adafruit-blinka", "adafruit-circuitpython-sht31d", "adafruit-circuitpython-as726x", "adafruit-circuitpython-fxos8700", "adafruit-circuitpython-fxas21002c"]
    )
