import re
import modules.cuda


def emit(writer, cudaVersion, baseImage="ubuntu:16.04", rcUrl=None):
    major, minor, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersion)
    modules.cuda.emit(writer, cudaVersion, baseImage, rcUrl)
    pkgs = [
        "cuda-command-line-tools-$pkgVersion",
        "cuda-cudart-dev-$pkgVersion",
        "cuda-driver-dev-$pkgVersion",
        "cuda-nvml-dev-$pkgVersion",
        "cuda-nvrtc-dev-$pkgVersion",
        "sudo"
    ]
    short = float(versionShort)
    if versionShort == "9.2":
        pkgs += [
            "cuda-compiler-$pkgVersion",
            "cuda-cupti-$pkgVersion",
            "cuda-nvcc-$pkgVersion"
        ]
    if short >= 10.1:
        pkgs.append("cuda-cupti-$pkgVersion")
        pkgs.append("cuda-compiler-$pkgVersion")
        pkgs.append("cuda-cudart-dev-$pkgVersion")
        pkgs.append("cuda-nvcc-$pkgVersion")
    # devtools
    if short <= 9.0:
        pkgs.append("cuda-nsight-$pkgVersion")
    if short >= 10.0:
        pkgs += [
            "cuda-nsight-compute-$pkgVersion",
            "cuda-nsight-systems-$pkgVersion",
        ]
    # math libraries
    if short < 11.0:
        pkgs += [
            "cuda-cufft-dev-$pkgVersion",
            "cuda-curand-dev-$pkgVersion",
            "cuda-cusolver-dev-$pkgVersion",
            "cuda-cusparse-dev-$pkgVersion",
            "cuda-npp-dev-$pkgVersion",
            "cuda-nvgraph-dev-$pkgVersion",
            "cuda-core-$pkgVersion",
            "cuda-misc-headers-$pkgVersion",
        ]
    else:
        pkgs += [
            "libcufft-dev-$pkgVersion",
            "libcurand-dev-$pkgVersion",
            "libcusolver-dev-$pkgVersion",
            "libcusparse-dev-$pkgVersion",
            "libnpp-dev-$pkgVersion",
        ]
    # cublas
    if short < 10.1:
        pkgs.append("cuda-cublas-dev-$pkgVersion")
    else:
        pkgs.append("libcublas-dev-$pkgVersion")
    writer.packages(pkgs, pkgVersion=pkgVersion,
                    installOpts="--allow-downgrades")
