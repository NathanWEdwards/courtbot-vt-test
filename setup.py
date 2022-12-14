from setuptools import setup

def long_description():
    with open('README.md') as readme:
        return readme.read()

setup(
    name='courtbot-vt',
    version='0.0.1',
    description='Test support for an application that extracts court events from a file and uploads court calendar information to database storage for a free service that will send you a text message reminder the day before your court hearing.',
    license='MIT',
    long_description=long_description(),
    long_description_content_type='text/plain',
    url='https://github.com/codeforbtv/courtbot-vt',
    author='CodeForAmerica',
    package_dir={'courtbot':'courtbot'},
    packages=['courtbot'],
    include_package_data=True
)