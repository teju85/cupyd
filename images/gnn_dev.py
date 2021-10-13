from __future__ import absolute_import
import modules.dev_env
import modules.gnn_dev
import modules.cuda
import modules.cudnn_dev
import modules.internal


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    if "cudnnVersion" not in kwargs:
        raise Exception("'cudnnVersion' is mandatory!")
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.cudnn_dev.emit(writer, kwargs["cudnnVersion"],
                           kwargs["cudaVersion"], kwargs["base"],
                           kwargs["rcUrl"])
    modules.gnn_dev.emit(writer, **kwargs)
    modules.dev_env.emit(writer, **kwargs)


def images():
    imgs = {}
    for osVer in ["20.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["11.2"]:
            for cudnnVer in ["8.0"]:
                _, _, cu_short, _ = modules.cuda.shortVersion(cudaVer)
                cu_short = cu_short.replace(".", "")
                _, _, short = modules.cudnn_dev.shortVersion(cudnnVer)
                short = short.replace(".", "")
                imgName = "gnn-dev:%s-%s-%s" % (verStr, cu_short, short)
                imgs[imgName] = {
                    "cudaVersion": cudaVer,
                    "cudnnVersion": cudnnVer,
                    "base": "ubuntu:%s" % osVer,
                    "needsContext": True,
                }
    imgs.update(modules.internal.read_rc())
    return imgs
