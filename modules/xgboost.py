import conda_ml_env


def emit(writer, ncclVersion):
    conda_ml_env.emit(writer)
    writer.packages(["cmake", "git",
                     "libnccl2=$ncclVersion-1+cuda$$CUDA_VERSION_SHORT",
                     "libnccl-dev=$ncclVersion-1+cuda$$CUDA_VERSION_SHORT",
                     "make"], ncclVersion=ncclVersion)
    writer.emit("""RUN git clone --recursive https://github.com/dmlc/xgboost /opt/xgboost && \\
    cd /opt/xgboost && \\
    mkdir build && \\
    cd build && \\
    cmake .. -DUSE_CUDA=ON -DUSE_NCCL=ON && \\
    make -j && \\
    cd ../python-package && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/xgboost""")
    writer.condaPackages(["dask", "distributed"])
    writer.emit("""RUN git clone https://github.com/dask/dask-xgboost /opt/dask-xgboost && \\
    cd /opt/dask-xgboost && \\
    python setup.py install && \\
    cd /opt && \\
    rm -rf /opt/dask-xgboost""")
