import modules.cuda

def emit(writer, **kwargs):
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "ncclVersion" not in kwargs:
        raise Exception("'ncclVersion' is mandatory!")
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    rapidsVersion = kwargs["rapidsVersion"]
    ncclVersion = kwargs["ncclVersion"]
    cudaVersionFull = kwargs["cudaVersionFull"]
    writer.packages(["doxygen", "graphviz", "gzip", "libopenblas-dev",
                     "libpthread-stubs0-dev", "tar", "unzip", "zlib1g-dev"])
    writer.condaPackages(["boost", "cmake=3.14", "cudf=$rapidsVersion.*", "Cython",
                          "dask", "distributed", "libclang", "pytest",
                          "scikit-learn", "umap-learn"],
                         channels=["anaconda", "numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"],
                         rapidsVersion=rapidsVersion)
    writer.emit("""ENV CONDA_PREFIX=/opt/conda""")
    major, minor, _, _, _ = modules.cuda.shortVersion(cudaVersionFull)
    writer.packages(["libnccl2=$ncclVersion-1+cuda$major.$minor",
                     "libnccl-dev=$ncclVersion-1+cuda$major.$minor"],
                    major=major,
                    minor=minor,
                    ncclVersion=ncclVersion)
