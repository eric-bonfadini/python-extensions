from distutils.core import Extension, setup

from Cython.Build import cythonize

if __name__ == "__main__":

    setup(
        name="ETL Cython extension",
        ext_modules=cythonize(
            [
                Extension(
                    "impl_cython.cython_python_ext",
                    sources=["impl_cython/cython_python_ext.pyx"],
                    include_dirs=[],
                    language="c++",
                )
            ],
            compiler_directives={"language_level": "3"},
            annotate=True,
        ),
    )
