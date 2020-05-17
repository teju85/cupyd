import re
import modules.cuda


def emit(writer, cudaVersionFull, baseImage="ubuntu:16.04"):
    major, minor, subminor, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersionFull)
    modules.cuda.emit(writer, cudaVersionFull, baseImage)
    if pkgVersion != "":
        pkgVersion = "-" + pkgVersion
    pkgs = ["cuda-command-line-tools$pkgVersion",
            "cuda-core$pkgVersion",
            "cuda-cudart-dev$pkgVersion",
            "cuda-cufft-dev$pkgVersion",
            "cuda-curand-dev$pkgVersion",
            "cuda-cusolver-dev$pkgVersion",
            "cuda-cusparse-dev$pkgVersion",
            "cuda-driver-dev$pkgVersion",
            "cuda-misc-headers$pkgVersion",
            "cuda-npp-dev$pkgVersion",
            "cuda-nvgraph-dev$pkgVersion",
            "cuda-nvml-dev$pkgVersion",
            "cuda-nvrtc-dev$pkgVersion",
            "sudo"]
    short = float(versionShort)
    if versionShort == "9.2":
        pkgs += [
            "cuda-compiler$pkgVersion",
            "cuda-cupti$pkgVersion",
            "cuda-nvcc$pkgVersion"
        ]
    if short >= 10.1:
        pkgs.append("cuda-cupti$pkgVersion")
        pkgs.append("cuda-compiler$pkgVersion")
        pkgs.append("cuda-cudart-dev$pkgVersion")
        pkgs.append("cuda-nvcc$pkgVersion")
    # devtools
    if short <= 9.0:
        pkgs.append("cuda-nsight$pkgVersion")
    if short >= 10.0:
        pkgs += [
            "cuda-nsight-compute$pkgVersion",
            "cuda-nsight-systems$pkgVersion",
        ]
    # cublas
    if short < 10.1:
        pkgs.append("cuda-cublas-dev$pkgVersion")
        tmpVersion = ""
    else:
        tmpVersion = "=%s.0.%s-1" % (versionShort, subminor)
        pkgs.append("libcublas-dev$tmpVersion")
    writer.packages(pkgs, pkgVersion=pkgVersion, tmpVersion=tmpVersion,
                    installOpts="--allow-downgrades")
