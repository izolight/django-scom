import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='django-scom',
	version='1.0',
	packages=['scom'],
	include_package_data=True,
	license='BSD License',
	description='A simple Django app to manager Micrososft System Center\
		Operations Manager Alerts',
	long_description=README,
	author='Gabor Tanz',
	author_email='gabor.tanz@vol.be.ch',
	classifiers=[
		'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
)