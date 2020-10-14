from setuptools import setup, find_packages

setup(
	name = 'project1',
	version = '1.0',
	author = 'Zack White',
	author_email = 'zaq@ou.edu',
	packages = find_packages(exclude=('test', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']
)
