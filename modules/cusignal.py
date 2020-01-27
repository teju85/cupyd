import modules.conda_ml_env


def emit(writer, jupyterPort="8888"):
    modules.conda_ml_env.emit(writer)
    writer.packages(["git", "gzip", "tar", "unzip",])
    writer.emit("""COPY contexts/jupyter /opt/jupyter""")
    writer.emit("""EXPOSE $jupyterPort""", jupyterPort=jupyterPort)
    writer.condaPackages(["nb_conda",
                          "scipy",
                          "numpy",
                          "'cudatoolkit>=9.2,<10.2'",
                          "boost",
                          "matplotlib",
                          "numba",
                          "pytest",
                          "cupy>=6.2.0",
                          "pytorch",
                          "cudf",
                          "cuml",
                          "cugraph",
                          "pandas",
                          "sphinx",
                          "sphinx_rtd_theme",
                          "numpydoc",
                          "ipython"],
                         channels=["conda-forge"," nvidia", "rapidsai", "pytorch",
                                   "defaults", "numba"])
    writer.emit("""RUN git clone --recursive https://github.com/rapidsai/cusignal \\
        /opt/cusignal && \\
    cd /opt/cusignal && \\
    ./build.sh""")
