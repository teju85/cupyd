import conda_ml_env


def emit(writer, rapidsVersion):
    conda_ml_env.emit(writer)
    writer.condaPackages(["boost", "cffi", "cmake=3.13", "Cython", "distributed",
                          "llvmlite", "numba", "nvstrings=$rapidsVersion.*",
                          "pandas>=0.23.4", "pyarrow", "pytest",
                          "rmm=$rapidsVersion.*"],
                         channels=["numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"],
                         rapidsVersion=rapidsVersion)
    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV CONDA_PREFIX=/opt/conda""")
    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cudf" /opt/cudf && \\
    cd /opt/cudf && \\
    ./build.sh libcudf && \\
    ./build.sh cudf && \\
    cd /opt && \\
    rm -rf /opt/cudf""")
    writer.emit("""RUN git clone "https://github.com/rapidsai/dask-cudf" /opt/dask-cudf && \\
    cd /opt/dask-cudf && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/dask-cudf""")
