from __future__ import absolute_import
import modules.dev_env
import modules.cuml_dev
import modules.cuda
import modules.cuda_dev
import os
import json


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


rapidsVersion = "0.14"
def images():
    imgs = {}
    for osVer in ["16.04", "18.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["10.0", "10.1", "10.2"]:
            _, _, short, _ = modules.cuda.shortVersion(cudaVer)
            short = short.replace(".", "")
            imgName = "ml-dev:%s-%s" % (verStr, short)
            imgs[imgName] = {
                "cudaVersion": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
                "rapidsVersion": rapidsVersion,
            }
    rcFile = os.getenv("RC_FILE", default=None)
    if rcFile is not None:
        with open(rcFile) as fp:
            data = json.load(fp)
            for img in data.keys():
                imgs[img] = data[img]
    return imgs
