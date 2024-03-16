from setuptools import setup, find_packages

setup(
    name='lab2048',
    version='0.1.0',
    url='https://github.com/lab2048/lab2048',
    author='Jilung Hsieh',
    author_email='jirlong@gmail.com',
    description='Tools for my lab(2048)',
    package_data={'lab2048': [
        'data/stopwords_cn.txt', 
        'data/stopwords_tw.txt',
        'data/userdict.txt',
        ]},
    include_package_data=True,
    packages=find_packages(),    
    install_requires=[
        'bokeh>=3.0',
        'pandas>=2.0',
        'gensim>=4.0',
    ]
)