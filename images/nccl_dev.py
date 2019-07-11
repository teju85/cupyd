from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.openmpi
import modules.cuda


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "ompiVersion" not in kwargs:
        raise Exception("'ompiVersion' is mandatory!")
    if "ncclVersion" not in kwargs:
        raise Exception("'ncclVersion' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    ompiVersion = kwargs["ompiVersion"]
    ncclVersion = kwargs["ncclVersion"]
    modules.cuda_dev.emit(writer, cudaVersionFull)
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.openmpi.emit(writer, devBuild=False, ompiVersion=ompiVersion)
    major, minor, _, _, _ = modules.cuda.shortVersion(cudaVersionFull)
    writer.packages(["libnccl2=$ncclVersion-1+cuda$major.$minor",
                     "libnccl-dev=$ncclVersion-1+cuda$major.$minor"],
                    major=major,
                    minor=minor,
                    ncclVersion=ncclVersion)


ompiVersion = "3.1.3"
ncclVersion = "2.4.7"
def images():
    return {
        "nccl-dev:2.4.7" : { "cudaVersionFull": "10.0.130",
                             "base": "ubuntu:16.04",
                             "needsContext": True,
                             "ompiVersion": ompiVersion,
                             "ncclVersion": ncclVersion,}
    }
