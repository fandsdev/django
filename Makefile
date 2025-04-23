bootstrap:
	rm -rf testproject

	uvx cookiecutter --no-input --keep-project-on-failure ./
