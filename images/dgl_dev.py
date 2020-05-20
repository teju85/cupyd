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
    writer.condaPackages(["cudatoolkit=$cudaVersion", "dgl-cuda$cudaVersion",
                          "nltk", "notebook", "pytorch", "torchvision"],
                         channels=["pytorch", "dglteam"],
                         cudaVersion=cudaVersion)
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


def images():
    return {
        "dgl-dev:1804-102": {
            "cudaVersion": "10.2",
            "base": "nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04",
            "needsContext": True,
        }
    }
