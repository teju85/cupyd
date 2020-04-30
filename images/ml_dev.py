from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.cuml_dev
import modules.cuda


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.cuml_dev.emit(writer, **kwargs)


rapidsVersion = "0.14"
def images():
    imgs = {}
    for osVer in ["16.04", "18.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["10.0.130", "10.1.105"]:
            _, _, _, short, _ = modules.cuda.shortVersion(cudaVer)
            short = short.replace(".", "")
            imgName = "ml-dev:%s-%s" % (verStr, short)
            imgs[imgName] = {
                "cudaVersionFull": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
                "rapidsVersion": rapidsVersion,
            }
    return imgs
