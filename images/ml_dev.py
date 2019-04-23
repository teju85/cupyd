from __future__ import absolute_import
import modules.cuda_dev
import modules.cudf
import modules.cuml_dev
import modules.ssh
import modules.openmpi


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    cudaVersion = kwargs["cudaVersion"]
    modules.cuda_dev.emit(writer, cudaVersion)
    modules.cudf.emit(writer)
    modules.cuml_dev.emit(writer)
    modules.ssh.emit(writer)
    modules.openmpi.emit(writer, devBuild=True, m4Version="1.4.18",
                         autoconfVersion="2.69", automakeVersion="1.16",
                         libtoolVersion="2.4.6", flexVersion="2.6.4")
    writer.packages(["clang", "clang-format", "gzip", "libpthread-stubs0-dev",
                     "tar", "unzip", "zlib1g-dev"])


def images():
    return {
        "ml-dev:9.2": { "cudaVersion": "9.2.88",
                        "base": "ubuntu:16.04",
                        "needsContext": True }
    }
