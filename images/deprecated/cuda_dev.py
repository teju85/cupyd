from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.build_essential
import modules.cmake


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    if "cmakeVersionFull" not in kwargs:
        raise Exception("'cmakeVersionFull' is mandatory!")
    cmakeVersionFull = kwargs["cmakeVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.build_essential.emit(writer)
    modules.cmake.emit(writer, cmakeVersionFull)
    writer.packages(["ca-certificates", "doxygen"])


def images():
    return {
        "cuda-dev:10.0": { "cudaVersionFull": "10.0.130",
                           "base": "ubuntu:16.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.14.7" },
        "cuda-dev:10.1": { "cudaVersionFull": "10.1.105",
                           "base": "ubuntu:16.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.14.7" },
        "cuda-dev:10.1-1804": { "cudaVersionFull": "10.1.105",
                                "base": "ubuntu:18.04",
                                "needsContext": True,
                                "cmakeVersionFull": "3.14.7" }
    }
