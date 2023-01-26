from distutils.core import setup

setup(
    name="pat_classifier",
    version="1.0",
    description="patent type classifier",
    author="Leo Liu",
    install_requires=["wordcloud", "pandas", "nltk"],
    packages=["pat_classifier"],
    package_data={"pat_classifier": ["*.txt"]},
)
