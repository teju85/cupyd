import cudf


def emit(writer, **kwargs):
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    rapidsVersion = kwargs["rapidsVersion"]
    writer.packages(["clang", "clang-format", "doxygen", "graphviz", "gzip",
                     "libopenblas-dev", "libpthread-stubs0-dev", "tar", "unzip",
                     "zlib1g-dev"])
    writer.condaPackages(["boost", "cudf=$rapidsVersion.*", "cmake=3.13", "Cython",
                          "dask", "distributed", "scikit-learn"],
                         channels=["anaconda", "numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"],
                         rapidsVersion=rapidsVersion)
