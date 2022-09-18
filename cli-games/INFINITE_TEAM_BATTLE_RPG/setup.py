from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='INFINITE_TEAM_BATTLE_RPG',
    version='1',
    packages=['INFINITE_TEAM_BATTLE_RPG'],
    url='https://github.com/SoftwareApkDev/SoftwareApkDev.github.io/tree/main/cli-games/INFINITE_TEAM_BATTLE_RPG',
    license='MIT',
    author='SoftwareApkDev',
    author_email='softwareapkdev2022@gmail.com',
    description='This package contains implementation of the offline turn-based strategy RPG '
                '"INFINITE_TEAM_BATTLE_RPG" on command line interface.',
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
            "INFINITE_TEAM_BATTLE_RPG=INFINITE_TEAM_BATTLE_RPG.infinite_team_battle_rpg:main",
        ]
    }
)