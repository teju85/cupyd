import re
import cuda


def emit(writer, cudaVersionFull):
    major, minor, subminor, versionShort, pkgVersion = cuda.shortVersion(cudaVersionFull)
    cuda.emit(writer, cudaVersionFull)
    if versionShort == "9.2":
        writer.packages(["cuda-compiler-$pkgVersion",
                         "cuda-cupti-$pkgVersion",
                         "cuda-nvcc-$pkgVersion"],
                        pkgVersion=pkgVersion)
    short = float(versionShort)
    if short < 10.1:
        cublas = "cuda-cublas-dev-$pkgVersion"
    else:
        cublas = "libcublas-dev=%s.0.%s-1" % (versionShort, subminor)
    writer.packages(["cuda-command-line-tools-$pkgVersion",
                     "cuda-core-$pkgVersion",
                     cublas,
                     "cuda-cudart-dev-$pkgVersion",
                     "cuda-cufft-dev-$pkgVersion",
                     "cuda-curand-dev-$pkgVersion",
                     "cuda-cusolver-dev-$pkgVersion",
                     "cuda-cusparse-dev-$pkgVersion",
                     "cuda-driver-dev-$pkgVersion",
                     "cuda-misc-headers-$pkgVersion",
                     "cuda-npp-dev-$pkgVersion",
                     "cuda-nvgraph-dev-$pkgVersion",
                     "cuda-nvml-dev-$pkgVersion",
                     "cuda-nvrtc-dev-$pkgVersion"],
                    pkgVersion=pkgVersion,
                    installOpts="--allow-downgrades")
    if float(versionShort) <= 9.0:
        writer.packages(["cuda-nsight-$pkgVersion"], pkgVersion=pkgVersion)
    if float(versionShort) >= 10.0:
        writer.packages(["cuda-nsight-compute-$pkgVersion"], pkgVersion=pkgVersion)
