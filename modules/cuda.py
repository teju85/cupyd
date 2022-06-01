import re


# https://forums.developer.nvidia.com/t/notice-cuda-linux-repository-key-rotation/
KEYRING_VERSION = "1.0-1"


def _emitHeaderRC(writer, osVer, rcUrl):
    writer.emit("""
RUN curl --output cuda-keyring.deb $rcUrl/$osVer/x86_64/cuda-keyring_${KEYRING_VERSION}_all.deb && \\
    dpkg -i cuda-keyring.deb && \\
    rm -f cuda-keyring.deb""",
                osVer=osVer, rcUrl=rcUrl, KEYRING_VERSION=KEYRING_VERSION)


def emitHeader(writer, baseImage, rcUrl):
    writer.emit("LABEL maintainer=\"NVIDIA CORPORATION <cudatools@nvidia.com>\"")
    osVer = re.sub(":", "", baseImage)
    osVer = re.sub("[.]", "", osVer)
    writer.packages(["ca-certificates", "curl", "gnupg2"])
    _emitHeaderRC(writer, osVer, rcUrl)


def shortVersion(cudaVersion):
    # eg: 9.0
    versionRegex = re.compile(r"^(\d+)[.](\d+)$")
    match = versionRegex.search(cudaVersion)
    if match is None:
        raise Exception("Bad cudaVersion passed! [%s]" % cudaVersion)
    major = match.group(1)
    minor = match.group(2)
    versionShort = "%s.%s" % (major, minor)
    pkgVersion = "%s-%s" % (major, minor)
    return major, minor, versionShort, pkgVersion


def emitSetup(writer, cudaVersion):
    major, minor, versionShort, pkgVersion = shortVersion(cudaVersion)
    writer.emit("RUN ln -s cuda-$versionShort /usr/local/cuda", versionShort=versionShort)
    writer.emit("""RUN echo "/usr/local/cuda/lib64" >> /etc/ld.so.conf.d/cuda.conf && \\
    echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \\
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf && \\
    ldconfig
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:$${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:$${LD_LIBRARY_PATH}
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs:$${LIBRARY_PATH}
ENV CUDA_VERSION_SHORT $versionShort

LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="$cudaVersion"

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=$versionShort"
""",
         cudaVersion=cudaVersion,
         versionShort=versionShort)


def emit(writer, cudaVersion, baseImage, rcUrl=None):
    if rcUrl is None:
        rcUrl = "https://developer.download.nvidia.com/compute/cuda/repos"
    major, minor, versionShort, pkgVersion = shortVersion(cudaVersion)
    emitHeader(writer, baseImage, rcUrl)
    writer.emit("ENV CUDA_VERSION $cudaVersion", cudaVersion=cudaVersion)
    pkgs = [
        "cuda-cudart-$pkgVersion",
        "cuda-nvrtc-$pkgVersion"
    ]
    short = float(versionShort)
    # math libraries
    if short < 11.0:
        pkgs += [
            "cuda-cufft-$pkgVersion",
            "cuda-curand-$pkgVersion",
            "cuda-cusolver-$pkgVersion",
            "cuda-cusparse-$pkgVersion",
            "cuda-npp-$pkgVersion",
            "cuda-nvgraph-$pkgVersion",
        ]
    else:
        pkgs += [
            "libcufft-$pkgVersion",
            "libcurand-$pkgVersion",
            "libcusolver-$pkgVersion",
            "libcusparse-$pkgVersion",
            "libnpp-$pkgVersion",
        ]
    # cublas
    if short < 10.1:
        pkgs.append("cuda-cublas-$pkgVersion")
    elif short < 11.0:
        pkgs.append("libcublas$major")
    else:
        pkgs.append("libcublas-$pkgVersion")
    writer.packages(pkgs, pkgVersion=pkgVersion, major=major)
    emitSetup(writer, cudaVersion)
