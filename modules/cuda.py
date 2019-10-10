import re

# shamelessly copied and modified from nvidia's dockerfiles on gitlab!
GPGKEY_SUM="d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5"
GPGKEY_FPR="ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80"


def _emitHeader1804(writer, osVer):
    writer.packages(["ca-certificates", "curl", "gnupg2"])
    writer.emit("""
RUN curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/$osVer/x86_64/7fa2af80.pub | apt-key add - && \\
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/$osVer/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \\
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/$osVer/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list""",
                osVer=osVer)


def emitHeader(writer, baseImage):
    writer.emit("LABEL maintainer=\"NVIDIA CORPORATION <cudatools@nvidia.com>\"")
    osVer = re.sub(":", "", baseImage)
    osVer = re.sub("[.]", "", osVer)
    if osVer == "ubuntu1804":
        _emitHeader1804(writer, osVer)
        return
    writer.emit("""
RUN apt-key adv --fetch-keys "http://developer.download.nvidia.com/compute/cuda/repos/$osVer/x86_64/7fa2af80.pub" && \\
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \\
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \\
    echo "deb http://developer.download.nvidia.com/compute/cuda/repos/$osVer/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \\
    echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/$osVer/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list""",
                NVIDIA_GPGKEY_SUM=GPGKEY_SUM,
                NVIDIA_GPGKEY_FPR=GPGKEY_FPR,
                osVer=osVer)


def shortVersion(cudaVersionFull):
    # eg: 9.0.170
    versionRegex = re.compile(r"^(\d+)[.](\d+)[.](\d+)$")
    match = versionRegex.search(cudaVersionFull)
    if match is None:
        raise Exception("Bad cudaVersionFull passed! [%s]" % cudaVersionFull)
    major = match.group(1)
    minor = match.group(2)
    subminor = match.group(3)
    versionShort = "%s.%s" % (major, minor)
    pkgVersion = "%s-%s=%s-1" % (major, minor, cudaVersionFull)
    return major, minor, subminor, versionShort, pkgVersion


def emit(writer, cudaVersionFull, baseImage):
    major, minor, subminor, versionShort, pkgVersion = shortVersion(cudaVersionFull)
    emitHeader(writer, baseImage)
    writer.emit("ENV CUDA_VERSION $cudaVersionFull", cudaVersionFull=cudaVersionFull)
    short = float(versionShort)
    if short < 10.1:
        cublas = "cuda-cublas-$pkgVersion"
    else:
        cublas = "libcublas%s=%s.0.%s-1" % (major, versionShort, subminor)
    pkgs = [cublas,
            "cuda-cudart-$pkgVersion",
            "cuda-cufft-$pkgVersion",
            "cuda-curand-$pkgVersion",
            "cuda-cusolver-$pkgVersion",
            "cuda-cusparse-$pkgVersion",
            "cuda-npp-$pkgVersion",
            "cuda-nvgraph-$pkgVersion",
            "cuda-nvrtc-$pkgVersion"]
    if short >= 10.1:
        pkgs.append("cuda-cupti-$pkgVersion")
        pkgs.append("cuda-compiler-$pkgVersion")
        pkgs.append("cuda-cudart-dev-$pkgVersion")
        pkgs.append("cuda-nvcc-$pkgVersion")
    writer.packages(pkgs, pkgVersion=pkgVersion)
    writer.emit("RUN ln -s cuda-$versionShort /usr/local/cuda""", versionShort=versionShort)
    writer.emit("""RUN echo "/usr/local/cuda/lib64" >> /etc/ld.so.conf.d/cuda.conf && \\
    echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \\
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf && \\
    ldconfig
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:$${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:$${LD_LIBRARY_PATH}
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs:$${LIBRARY_PATH}
ENV CUDA_VERSION_SHORT $versionShort

LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="$cudaVersionFull"

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=$versionShort"
""",
         cudaVersionFull=cudaVersionFull,
         versionShort=versionShort)
