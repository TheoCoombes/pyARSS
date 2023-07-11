from setuptools import setup

setup(
    name="pyARSS",
    version="0.1.0",
    description="A Python wrapper for the Analysis & Resynthesis Sound Spectrograph (ARSS)",
    url="https://github.com/TheoCoombes/pyARSS",
    author="Theo Coombes",
    author_email="theocoombes06@gmail.com",
    license="MIT",
    packages=["pyARSS"],
    requires=["pydub"]
)