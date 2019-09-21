import modules.cuda

def emit(writer, **kwargs):
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    rapidsVersion = kwargs["rapidsVersion"]
    writer.packages(["doxygen", "graphviz", "gzip", "libopenblas-dev",
                     "libpthread-stubs0-dev", "tar", "unzip", "zlib1g-dev"])
    writer.condaPackages(["boost", "cmake=3.14.5", "cudf=$rapidsVersion.*",
                          "cython", "dask", "dask-cuda=$rapidsVersion.*",
                          "dask-cudf=$rapidsVersion.*", "dask-ml",
                          "distributed", "libclang=8.0.0", "libcumlprims=0.9.*",
                          "nccl>=2.4", "numba=0.45*", "pytest",
                          "rmm=$rapidsVersion.*", "scikit-learn", "statsmodels",
                          "umap-learn"],
                         channels=["rapidsai", "nvidia", "rapidsai-nightly",
                                   "conda-forge", "defaults"],
                         rapidsVersion=rapidsVersion)
    writer.emit("""ENV CONDA_PREFIX=/opt/conda""")
