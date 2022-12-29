from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in one_wiki/__init__.py
from one_wiki import __version__ as version

setup(
	name="one_wiki",
	version=version,
	description="Custom Application to override Frappe Wiki",
	author="One_FM",
	author_email="supporr@one-fm.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
