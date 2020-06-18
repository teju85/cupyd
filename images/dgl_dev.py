from __future__ import absolute_import
import modules.dev_env
import modules.conda
import modules.jupyter
import modules.cuda


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    cudaVersion = kwargs["cudaVersion"]
    modules.conda.emit(writer)
    writer.condaPackages(["cmake", "cudatoolkit=$cudaVersion", "nltk",
                          "notebook", "pytorch", "torchvision"],
                         channels=["pytorch"], cudaVersion=cudaVersion)
    modules.jupyter.emit(writer, **kwargs)
    modules.dev_env.emit(writer, **kwargs)
    _, _, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersion)
    short = float(versionShort)
    pkgs = []
    if short >= 10.0:
        pkgs += [
            "cuda-nsight-compute-$pkgVersion",
            "cuda-nsight-systems-$pkgVersion",
        ]
    writer.packages(pkgs, pkgVersion=pkgVersion,
                    installOpts="--allow-downgrades")
    writer.emit("COPY contexts/dgl-dev /dgl-dev")


def images():
    return {
        "dgl-dev:1804-102": {
            "cudaVersion": "10.2",
            "base": "nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04",
            "needsContext": True,
        },
        "dgl-dev:1804-110rc": {
            "cudaVersion": "11.0",
            "base": "nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04-rc",
            "needsContext": True,
        }
    }
