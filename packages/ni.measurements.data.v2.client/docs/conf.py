"""Sphinx configuration for the V2 client package."""

import datetime
import pathlib

import autoapi.extension
import toml

extensions = [
    "autoapi.extension",
    "m2r2",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

root_path = pathlib.Path(__file__).parent.parent
project_config = toml.loads((root_path / "pyproject.toml").read_text(encoding="utf-8"))

project = project_config["project"]["name"]
company = "National Instruments"
copyright = f"2025-%Y, {company}"
if datetime.datetime.now().year == 2025:
    copyright = f"%Y, {company}"

version = project_config["project"]["version"]
release = ".".join(version.split(".")[:2])
htmlhelp_basename = f"{project}doc"

autoapi_options = list(autoapi.extension._DEFAULT_OPTIONS)
autoapi_options.remove("private-members")
autoapi_dirs = [root_path / "src" / "ni"]
autoapi_python_use_implicit_namespaces = True
autoapi_template_dir = "templates/autoapi"
autoapi_python_class_content = "both"
autoapi_type = "python"
autodoc_typehints = "description"
autoapi_file_patterns = ["*.py"]
suppress_warnings = ["autoapi.python_import_resolution"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "__init__.py"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "grpc": ("https://grpc.github.io/grpc/python/", None),
}
html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": -1}
templates_path = ["templates"]
napoleon_numpy_docstring = False
