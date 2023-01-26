from distutils.core import setup

setup(
    name="pat_classifier",
    version="1.1",
    description="patent type classifier",
    author="Leo Liu",
    #  author_email='gward@python.net',
    #  url='https://www.python.org/sigs/distutils-sig/',
    install_requires=["wordcloud", "pandas", "nltk"],
    packages=["pat_classifier"],
    package_data={"pat_classifier": ["*.txt"]},
)
