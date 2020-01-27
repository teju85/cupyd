from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.cusignal


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.cusignal.emit(writer)


def images():
    return {
        "cusignal:10.1": { "cudaVersionFull": "10.1.105",
                           "base": "ubuntu:18.04",
                           "needsContext": True, },
    }
