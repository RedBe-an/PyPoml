from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as f: 
	  long_description = f.read()

setup(
	name='PyPoml',
	version='1.0.0',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	description='Plain Object Markup Language',
	author='Poml', 
	author_email='buildten0@gmail.com', 
	url='https://github.com/POML-project/poml',  
	python_requires='>=3.11', 
	packages=find_packages(exclude=[]),
)