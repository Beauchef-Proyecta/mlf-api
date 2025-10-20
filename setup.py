from setuptools import setup, find_packages

setup( 
    name= 'mlf-api',
    version = '0.2.5',
    packages=find_packages(),
    install_requires = [
      'aiohttp==3.8.4',
      'aiortc',
      'numpy==1.24.3',
      'opencv-python==4.7.0.72',
      'requests==2.31.0'
      
    ],
)
