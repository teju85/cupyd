from __future__ import absolute_import
import modules.dev_env
import modules.conda
import modules.jupyter
import modules.cuda_dev
import modules.internal


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    cudaVersion = kwargs["cudaVersion"]
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.cuda_dev.emit(writer, kwargs["cudaVersion"], kwargs["base"],
                          kwargs["rcUrl"])
    modules.conda.emit(writer)
    writer.condaPackages(["cmake", "cudatoolkit=$cudaVersion", "nltk",
                          "notebook", "pytorch", "torchvision"],
                         channels=["pytorch"], cudaVersion=cudaVersion)
    modules.jupyter.emit(writer, **kwargs)
    modules.dev_env.emit(writer, **kwargs)
    writer.emit("COPY contexts/dgl-dev /dgl-dev")


def images():
    imgs = {
        "dgl-dev:1804-102": {
            "cudaVersion": "10.2",
            "base": "ubuntu:18.04",
            "needsContext": True,
        },
        "dgl-dev:1804-110": {
            "cudaVersion": "11.0",
            "base": "ubuntu:18.04",
            "needsContext": True,
        }
    }
    imgs.update(modules.internal.read_rc())
    return imgs
