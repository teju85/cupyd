import conda_ml_env


def emit(writer):
    conda_ml_env.emit(writer)
    writer.condaPackages(["boost", "cffi", "cmake=3.13", "Cython", "distributed",
                          "llvmlite", "numba", "nvstrings=0.3.0", "pandas>=0.23.4",
                          "pyarrow", "pytest"],
                         channels=["numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"])
    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV CONDA_PREFIX=/opt/conda""")
    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cudf" /opt/cudf && \\
    cd /opt/cudf && \\
    mkdir -p cpp/build && \\
    cd cpp/build && \\
    cmake .. -DCMAKE_INSTALL_PREFIX=$${CONDA_PREFIX} -DCMAKE_CXX11_ABI=ON && \\
    make -j && \\
    make install && \\
    make python_cffi && \\
    make install_python && \\
    cd ../../python && \\
    python setup.py build_ext --inplace && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/cudf""")
    writer.emit("""RUN git clone "https://github.com/rapidsai/dask-cudf" /opt/dask-cudf && \\
    cd /opt/dask-cudf && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/dask-cudf""")
