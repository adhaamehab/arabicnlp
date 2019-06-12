from setuptools import setup, find_packages

setup(
    name="arabicnlp",
    version='0.1.7',
    description="Python package for arabic NLP",
    long_description="Python package for processing arabic language and the backbone of texblob-ar\nFeatuers:\n-POS tagger\n-Tokenization\n-Stemming\n-Spelling correction",
    # The project URL.
    url='https://github.com/adhaamehab/arabicnlp',

    # Author details
    author='Adham Ehab',
    author_email='adhaamehab7@gmail.com',

    classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Intended Audience :: Developers',
         'Natural Language :: English',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python',
         'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=[
        'keras',
        'tensorflow'
    ],
    include_package_data=True,
    package_data={
        '': ['*.h5', '*.bin'],
        'data': ['*.h5', '*.bin']
    }
)
