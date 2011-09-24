
from setuptools import setup, find_packages
 
setup(
    name='django-zendesk-import',
    version='0.1dev',
    description="A mapping of zendesk's XML format to Django models and an importer",
    author='Gabriel Grant',
    author_email='g@briel.ca',
    url='https://github.com/gabrielgrant/django-zendesk-import/',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['setuptools', 'iso8601'],
)
