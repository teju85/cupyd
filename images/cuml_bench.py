from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.conda_ml_env
import modules.cudf
import modules.cuml
import modules.xgboost


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "ncclVersion" not in kwargs:
        raise Exception("'ncclVersion' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    rapidsVersion = kwargs["rapidsVersion"]
    modules.cuda_dev.emit(writer, cudaVersionFull)
    modules.conda_ml_env.emit(writer)
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.cudf.emit(writer, rapidsVersion=rapidsVersion)
    modules.cuml.emit(writer, rapidsVersion=rapidsVersion)
    modules.xgboost.emit(writer, ncclVersion=ncclVersion)
    writer.emit("""RUN git clone https://github.com/JohnZed/cuml-samples /opt/cuml-samples && \\
    chmod a+x /opt/cuml-samples/*.py""")
    writer.emit("""WORKDIR /opt/cuml-samples""")
    writer.emit("""RUN wget https://developer.nvidia.com/rdp/assets/Nsight_Systems_2019_3_Linux_installer && \\
    chmod +x Nsight_Systems_2019_3_Linux_installer && \\
    ./Nsight_Systems_2019_3_Linux_installer --accept --quiet && \\
    mv NsightSystems-* /usr/local/cuda/NsightSystems && \\
    rm -f Nsight_Systems_2019_3_Linux_installer""")
    writer.emit("""ENV PATH=/usr/local/cuda/NsightSystems/Target-x86_64/x86_64/:$${PATH}
ENV PATH=/usr/local/cuda/NsightSystems/Host-x86_64/:$${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/NsightSystems/Target-x86_64/x86_64/:$${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/NsightSystems/Host-x86_64/:$${LD_LIBRARY_PATH}""")


rapidsVersion = "0.7"
ncclVersion = "2.4.2"
def images():
    return {
        "cuml-bench:9.2": { "cudaVersionFull": "9.2.88",
                            "base": "ubuntu:16.04",
                            "needsContext": True,
                            "rapidsVersion": rapidsVersion,
                            "ncclVersion": ncclVersion },
        "cuml-bench:10.0": { "cudaVersionFull": "10.0.130",
                             "base": "ubuntu:16.04",
                             "needsContext": True,
                             "rapidsVersion": rapidsVersion,
                             "ncclVersion": ncclVersion }
    }
