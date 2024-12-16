# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GH CLI Wrapper'
copyright = '2024, David Burton'
author = 'David Burton'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # Automatically document code from docstrings
    'sphinx.ext.napoleon',       # Support for Google and NumPy-style docstrings
    'sphinx.ext.viewcode',       # Add links to highlighted source code
    'sphinx.ext.autosummary',    # Create summaries for modules/classes/functions
    'sphinx.ext.doctest',        # Run doctests embedded in documentation
]

autosummary_generate = True  # Automatically generate summary pages

doctest_test_doctest_blocks = 'True'  # Enable testing of doctest blocks in documentation

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

import os
import sys
from pathlib import Path
#https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#usage
sys.path.insert(0, str(Path('..", pyghcli').resolve()))

print(f"path : {sys.path}")
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
