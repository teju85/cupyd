from __future__ import absolute_import
import modules.build_essential
import modules.cuda_dev
import modules.conda
import modules.conda_ml_env
import modules.dev_env
import modules.internal


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
    modules.conda.emit(writer)
    modules.conda_ml_env.emit(writer)
    modules.dev_env.emit(writer, **kwargs)


def images():
    imgs = {}
    for osVer in ["18.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["10.0", "10.1", "10.2", "11.0", "11.1", "11.2"]:
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
