
# Courtesy: https://github.com/StanfordLegion/legion/blob/stable/docker/Dockerfile.gasnet-cuda
def emit(writer, **kwargs):
    writer.emit("""ENV DEBIAN_FRONTEND noninteractive""")
    writer.emit("""RUN apt-get update -qq && \\
    apt-get install -qq software-properties-common && \\
    add-apt-repository ppa:ubuntu-toolchain-r/test -y && \\
    add-apt-repository ppa:pypy/ppa -y && \\
    apt-get update -qq && \\
    apt-get install -qq \\
        build-essential git python-pip pypy time wget \\
        g++-4.8 g++-4.9 g++-5 g++-6 \\
        gcc-4.9-multilib g++-4.9-multilib \\
        libaio1 \\
        libncurses5-dev \\
        zlib1g-dev \\
        mpich libmpich-dev \\
        mesa-common-dev \\
        libblas-dev liblapack-dev libhdf5-dev \\
        module-init-tools \\
        gdb \\
        openmpi-bin openssh-client openssh-server libopenmpi-dev && \\
    apt-get clean""")
    writer.packages([
        "dapl2-utils",
        "ibutils",
        "ibverbs-utils",
        "infiniband-diags",
        "libdapl-dev",
        "libibcm-dev",
        "libibverbs1-dbg",
        "libibverbs-dev",
        "libmlx4-1-dbg",
        "libmlx4-dev",
        "libmlx5-1-dbg",
        "libmlx5-dev",
        "librdmacm-dev",
        "opensm"])
    writer.emit("""RUN git clone https://github.com/StanfordLegion/gasnet.git \\
        /opt/gasnet && \\
    cd /opt/gasnet && \\
    make -e CONDUIT=ibv""")
    writer.emit("""RUN wget http://releases.llvm.org/3.8.1/llvm-3.8.1.src.tar.xz && \\
    tar -xf llvm-3.8.1.src.tar.xz && \\
    wget http://releases.llvm.org/3.8.1/cfe-3.8.1.src.tar.xz && \\
    tar -xf cfe-3.8.1.src.tar.xz && \\
    mv cfe-3.8.1.src llvm-3.8.1.src/tools/clang && \\
    mkdir llvm-build && cd llvm-build && \\
    ../llvm-3.8.1.src/configure --enable-optimized --disable-assertions --disable-terminfo --disable-libedit --disable-zlib && \\
    make -j 20 && make install""")
    writer.emit("""RUN git clone https://github.com/StanfordLegion/legion.git \\
        /opt/legion && \\
    LLVM_CONFIG=llvm-config \\
        GASNET=/opt/gasnet/release \\
        CONDUIT=ibv \\
        /opt/legion/language/install.py --rdir=auto --gasnet --cuda""")
    writer.emit("RUN ln -s /lib/x86_64-linux-gnu/libaio.so.1 /lib/x86_64-linux-gnu/libaio.so")
