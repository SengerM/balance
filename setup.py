import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "balance",
	version = "0.0.0",
	author = "Matias H. Senger",
	author_email = "m.senger@hotmail.com",
	description = "Package for analyze my money",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/SengerM/myplotlib",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
