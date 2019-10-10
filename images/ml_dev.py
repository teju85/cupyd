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
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.conda_ml_env.emit(writer)
    modules.openmpi.emit(writer, devBuild=False, ompiVersion="4.0.2")
    modules.cuml_dev.emit(writer, **kwargs)


rapidsVersion = "0.10"
def images():
    return {
        "ml-dev:9.2": { "cudaVersionFull": "9.2.88",
                        "base": "ubuntu:16.04",
                        "needsContext": True,
                        "rapidsVersion": rapidsVersion },
        "ml-dev:10.0": { "cudaVersionFull": "10.0.130",
                         "base": "ubuntu:16.04",
                         "needsContext": True,
                         "rapidsVersion": rapidsVersion },
        "ml-dev:10.1": { "cudaVersionFull": "10.1.105",
                         "base": "ubuntu:16.04",
                         "needsContext": True,
                         "rapidsVersion": rapidsVersion },
        "ml-dev:10.1-1804": { "cudaVersionFull": "10.1.105",
                              "base": "ubuntu:18.04",
                              "needsContext": True,
                              "rapidsVersion": rapidsVersion }
    }
