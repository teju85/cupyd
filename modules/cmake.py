import re
import build_essential


def shortVersion(cmakeVersionFull):
    # 3.13.4
    regex = re.compile(r"^(\d+)[.](\d+)[.](\d+)$")
    match = regex.search(cmakeVersionFull)
    if match is None:
        raise Exception("Bad cmake version '%s'!" % cmakeVersionFull)
    major = match.group(1)
    minor = match.group(2)
    short = "%s.%s" % (major, minor)
    return major, minor, short


def emit(writer, cmakeVersionFull):
    major, minor, short = shortVersion(cmakeVersionFull)
    build_essential.emit(writer)
    writer.packages(["curl", "libcurl4-openssl-dev", "zlib1g-dev"])
    writer.emit("""ENV CMAKE_SHORT_VERSION $short
ENV CMAKE_LONG_VERSION  $full

# somehow I'm unable to get the cmake-provided curl library support https protocol!
RUN wget --no-check-certificate \\
        "https://cmake.org/files/v$short/cmake-$full.tar.gz" && \\
    tar xf cmake-$full.tar.gz && \\
    cd cmake-$full && \\
    ./bootstrap --system-curl && \\
    make -j && \\
    make install && \\
    cd .. && \\
    rm -rf cmake-$full.tar.gz cmake-$full""",
                short=short, full=cmakeVersionFull)
