from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "src/**/*.py",  # thêm dấu " ở đầu
        compiler_directives={"language_level": "3"},
    )
)
