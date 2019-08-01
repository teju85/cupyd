import modules.conda_ml_env
import modules.cudf


def emit(writer, rapidsVersion):
    modules.conda_ml_env.emit(writer)
    modules.cudf.emit(writer, rapidsVersion)
    writer.packages(["doxygen", "graphviz", "gzip",
                     "libopenblas-dev", "libpthread-stubs0-dev", "tar", "unzip",
                     "zlib1g-dev"])
    writer.condaPackages(["boost", "cmake=3.13", "Cython", "dask", "distributed",
                          "libclang", "pytest", "scikit-learn", "umap-learn"],
                         channels=["anaconda", "numba", "conda-forge",
                                   "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                                   "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                                   "defaults"],
                         rapidsVersion=rapidsVersion)
    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV CONDA_PREFIX=/opt/conda""")
    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cuml" /opt/cuml && \\
    cd /opt/cuml && \\
    mkdir -p cpp/build && \\
    cd cpp/build && \\
    cmake .. -DCMAKE_INSTALL_PREFIX=$${CONDA_PREFIX} -DCMAKE_CXX11_ABI=ON && \\
    make -j && \\
    make install && \\
    cd ../../python && \\
    python setup.py build_ext --inplace && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/cuml""")
