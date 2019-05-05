from setuptools import setup, find_packages

setup(
    name="arabicnlp",
    version='0.1.0',
    description="Python package for arabic NLP",
    long_description="Python package for processing arabic language with features like sentiment analysis and part-of-speech tagging",
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
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True
)
