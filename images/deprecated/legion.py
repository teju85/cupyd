from __future__ import absolute_import
import modules.cuda_dev
import modules.legion
import modules.runas
import modules.ssh


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.legion.emit(writer)


def images():
    return {
        "legion:10.0": { "cudaVersionFull": "10.0.130",
                        "base": "ubuntu:16.04",
                         "needsContext": True, },
        "legion:10.1": { "cudaVersionFull": "10.1.105",
                        "base": "ubuntu:16.04",
                         "needsContext": True, },
    }
