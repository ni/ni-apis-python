"""Sphinx configuration for the data store V2 interfaces."""

import pathlib

import toml

root_path = pathlib.Path(__file__).parent.parent
proj_config = toml.loads((root_path / "pyproject.toml").read_text())
project = proj_config["project"]["name"]
version = proj_config["project"]["version"]
release = version
copyright = "2026, National Instruments"

extensions = ["autoapi.extension", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]
autoapi_dirs = [str(root_path / "src" / "ni")]
autoapi_python_use_implicit_namespaces = True
autoapi_template_dir = "templates/autoapi"
autoapi_python_class_content = "both"
autoapi_file_patterns = ["*.pyi", "*.py"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autodoc_typehints = "description"
exclude_patterns = ["_build", "templates"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": -1}
napoleon_numpy_docstring = False
