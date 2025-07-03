from __future__ import absolute_import
import modules.build_essential
import modules.cuda_dev
import modules.conda
import modules.dev_env
import modules.internal
import modules.openmpi


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.build_essential.emit(writer)
    modules.cuda_dev.emit(writer, kwargs["cudaVersion"], kwargs["base"],
                          kwargs["rcUrl"])
    writer.packages(["build-essential", "ca-certificates", "git", "wget",
                     "python3", "python3-pip"])
    writer.emit("RUN pip3 install matplotlib numpy pandas")
    modules.openmpi.emit(writer)
    ncclVersions = {
        "11.8": "2.16.5",
        "12.0": "2.18.1",
        "12.1": "2.18.3",
        "12.2": "2.19.3",
        "12.3": "2.19.3",
    }
    ncclVersion = ncclVersions[kwargs["cudaVersion"]]
    writer.packages(["libnccl2=$ncclVersion-1+cuda$$CUDA_VERSION_SHORT",
                     "libnccl-dev=$ncclVersion-1+cuda$$CUDA_VERSION_SHORT"],
                    ncclVersion=ncclVersion)
    modules.dev_env.emit(writer, **kwargs)


def images():
    imgs = {}
    for osVer in ["20.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["10.0", "10.1", "10.2",
                        "11.0", "11.1", "11.2", "11.4", "11.5", "11.6", "11.8",
                        "12.0", "12.1"]:
            _, _, short, _ = modules.cuda.shortVersion(cudaVer)
            short = short.replace(".", "")
            imgName = "ubench:%s-%s" % (verStr, short)
            imgs[imgName] = {
                "cudaVersion": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
            }
    imgs.update(modules.internal.read_rc())
    return imgs
