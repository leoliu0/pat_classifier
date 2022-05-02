from distutils.core import setup

setup(
    name="pat_classifier",
    version="1.0",
    description="patent type classifier",
    author="Leo Liu",
    #  author_email='gward@python.net',
    #  url='https://www.python.org/sigs/distutils-sig/',
    packages=["pat_classifier"],
    package_data={"pat_classifier": ["*.txt"]},
    install_requires=["wordcloud", "loguru", "pyspark", "pandas"],
)
