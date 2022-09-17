from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='LIFE_SIMULATION',
    version='1',
    packages=['LIFE_SIMULATION'],
    url='https://github.com/NativeApkDev/ANCIENT_INVASION',
    license='MIT',
    author='NativeApkDev',
    author_email='nativeapkdev2021@gmail.com',
    description='This package contains implementation of the offline adventure game '
                '"LIFE_SIMULATION" on command line interface.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "ANCIENT_INVASION=ANCIENT_INVASION.ancient_invasion:main",
        ]
    }
)