import cudf


def emit(writer):
    writer.packages(["clang", "clang-format", "doxygen", "graphviz", "gzip",
                     "libopenblas-dev", "libpthread-stubs0-dev", "tar", "unzip",
                     "zlib1g-dev"])
    writer.condaPackages(["cudf=0.7.*", "scikit-learn"],
                         channels=["anaconda", "numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"])
