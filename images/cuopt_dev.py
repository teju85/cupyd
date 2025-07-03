from __future__ import absolute_import
import modules.dev_env
import modules.cuopt_dev
import modules.cuda


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.cuda_dev.emit(writer, kwargs["cudaVersion"], kwargs["base"],
                          kwargs["rcUrl"])
    modules.cuopt_dev.emit(writer, **kwargs)
    modules.dev_env.emit(writer, **kwargs)


cuoptVersion = "25.08"
def images():
    imgs = {}
    for osVer in ["22.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["12.8"]:
            _, _, cu_short, _ = modules.cuda.shortVersion(cudaVer)
            cu_short = cu_short.replace(".", "")
            imgName = "cuopt-dev:%s-%s" % (verStr, cu_short)
            imgs[imgName] = {
                "cudaVersion": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
                "cuoptVersion": cuoptVersion,
            }
    return imgs
