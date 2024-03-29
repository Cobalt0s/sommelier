from setuptools import setup, find_packages

setup(
    name='sommelier',
    version='1.2.29',
    packages=find_packages(),
    license='MIT',
    description='Testing wrapper of Behave library',
    long_description=open('README.txt').read(),
    install_requires=[
        'behave==1.2.6',
        'confluent-kafka==1.7.0',
        'requests>=2.28.1',
        'flask>=2.2.2',
        'websockets>=10.4',
        'urllib3==1.26.6'
    ],
    url='https://github.com/Cobalt0s/sommelier',
    author='Constantin Koval',
    author_email='constantin.y.koval@gmail.com'
)
