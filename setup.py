from setuptools import setup

setup(
    name='zzcpdf',
    version='0.1.0',
    description='pdf tools',
    author='zhangzhechun',
    author_email='zhangzhechun_721@163.com',
    url='https://github.com/openwintop/zzcpdf',
    packages=['your_library'],
    install_requires=[
        'fpd>=1.7.2',
        'fitz>=0.0.1.dev2',
        'PyMuPDF>=1.23.18',
        'argparse>=1.4.0'        
    ],
)