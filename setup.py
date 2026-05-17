from setuptools import setup
from setuptools.command.build_ext import build_ext
import sys

class BuildExt(build_ext):
    def get_source_files(self):
        # Override to avoid cython_sources error
        return []

setup(
    name="rasa-bot",
    version="1.0.0",
    cmdclass={'build_ext': BuildExt},
)
