from __future__ import absolute_import
import modules.dev_env
import modules.cuml_dev
import modules.cuda
import modules.internal


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.cuda_dev.emit(writer, kwargs["cudaVersion"], kwargs["base"],
                          kwargs["rcUrl"])
    modules.cuml_dev.emit(writer, **kwargs)
    modules.dev_env.emit(writer, **kwargs)


rapidsVersion = "22.04"
def images():
    imgs = {}
    for osVer in ["20.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["11.2", "11.5"]:
            _, _, cu_short, _ = modules.cuda.shortVersion(cudaVer)
            cu_short = cu_short.replace(".", "")
            imgName = "ml-dev:%s-%s" % (verStr, cu_short)
            imgs[imgName] = {
                "cudaVersion": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
                "rapidsVersion": rapidsVersion,
            }
    imgs.update(modules.internal.read_rc())
    return imgs
