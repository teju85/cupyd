import re
import modules.cuda_dev
import modules.cuda


def _emitHeader(writer, osVer,
                rcUrl="http://developer.download.nvidia.com/compute/machine-learning/repos"):
    writer.emit("""
RUN echo "deb $rcUrl/$osVer/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list""",
                rcUrl=rcUrl, osVer=osVer)


def shortVersion(cudnnVersion):
    # eg: 8.0
    versionRegex = re.compile(r"^(\d+)[.](\d+)$")
    match = versionRegex.search(cudnnVersion)
    if match is None:
        raise Exception("Bad cudnnVersion passed! [%s]" % cudnnVersion)
    major = match.group(1)
    minor = match.group(2)
    versionShort = "%s.%s" % (major, minor)
    return major, minor, versionShort


def emit(writer, cudnnVersion, cudaVersion, baseImage="ubuntu:18.04",
         rcUrl=None):
    modules.cuda_dev.emit(writer, cudaVersion, baseImage, rcUrl)
    _emitHeader(writer, osVer)
    major, _, _ = shortVersion(cudnnVersion)
    pkgs = []
    pkgs.append("libcudnn$major-dev")
    writer.packages(pkgs, major=major)
