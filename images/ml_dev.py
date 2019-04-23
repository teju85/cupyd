from __future__ import absolute_import
import modules.cuda_dev
import modules.cuml_dev
import modules.conda_ml_env
import modules.runas
import modules.ssh
import modules.openmpi


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull)
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.conda_ml_env.emit(writer)
    modules.openmpi.emit(writer, devBuild=True, m4Version="1.4.18",
                         autoconfVersion="2.69", automakeVersion="1.16",
                         libtoolVersion="2.4.6", flexVersion="2.6.4")
    modules.cuml_dev.emit(writer, **kwargs)


def images():
    return {
        "ml-dev:9.2": { "cudaVersionFull": "9.2.88",
                        "base": "ubuntu:16.04",
                        "needsContext": True,
                        "rapidsVersion": "0.7" },
        "ml-dev:10.0": { "cudaVersionFull": "10.0.130",
                         "base": "ubuntu:16.04",
                         "needsContext": True,
                         "rapidsVersion": "0.7" }
    }
