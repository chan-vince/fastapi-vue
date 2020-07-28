import toml

pyproject = toml.load("./pyproject.toml")
__version__ = pyproject["tool"]["poetry"]["version"]