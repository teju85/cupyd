import re


def emit(writer, devBuild=False, m4Version="1.4.18", autoconfVersion="2.69",
         automakeVersion="1.16", libtoolVersion="2.4.6", flexVersion="2.6.4",
         ompiVersion="3.1.3"):
    if not devBuild:
        ompiRegex = re.compile(r"^(\d+)[.](\d+)")
        match = ompiRegex.search(ompiVersion)
        if match is None:
            raise Exception("Incorrect ompiVersion passed! [%s]" % ompiVersion)
        ompiShort = "%s.%s" % (match.group(1), match.group(2))
        writer.emit("""RUN wget "https://download.open-mpi.org/release/open-mpi/v$ompiShort/openmpi-$ompiVersion.tar.gz" \\
        -O /opt/openmpi.tar.gz && \\
    cd /opt && \\
    tar xf /opt/openmpi.tar.gz && \\
    cd /opt/openmpi-$ompiVersion && \\
    ./configure --with-cuda && \\
    make -j all && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/openmpi.tar.gz && \\
    rm -rf /opt/opempi-$ompiVersion""", ompiVersion=ompiVersion, ompiShort=ompiShort)
        return

    toolsdir = "/opt/autotools"
    writer.emit("ENV PATH=$toolsdir/bin:$${PATH}", toolsdir=toolsdir)
    writer.emit("""RUN wget "ftp://ftp.gnu.org/gnu/m4/m4-$m4Version.tar.gz" -O /opt/m4.tar.gz && \\
    cd /opt && \\
    tar xf /opt/m4.tar.gz && \\
    cd /opt/m4-$m4Version && \\
    ./configure --prefix=$toolsdir && \\
    make -j && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/m4.tar.gz && \\
    rm -rf /opt/m4-$m4Version""", m4Version=m4Version, toolsdir=toolsdir)
    writer.emit("""RUN wget "ftp://ftp.gnu.org/gnu/autoconf/autoconf-$autoconfVersion.tar.gz" \\
        -O /opt/autoconf.tar.gz && \\
    cd /opt && \\
    tar xf /opt/autoconf.tar.gz && \\
    cd /opt/autoconf-$autoconfVersion && \\
    ./configure --prefix=$toolsdir && \\
    make -j && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/autoconf.tar.gz && \\
    rm -rf /opt/autoconf-$autoconfVersion""",
                autoconfVersion=autoconfVersion, toolsdir=toolsdir)
    writer.emit("""RUN wget "ftp://ftp.gnu.org/gnu/automake/automake-$automakeVersion.tar.gz" \\
        -O /opt/automake.tar.gz && \\
    cd /opt && \\
    tar xf /opt/automake.tar.gz && \\
    cd /opt/automake-$automakeVersion && \\
    ./configure --prefix=$toolsdir && \\
    make -j && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/automake.tar.gz && \\
    rm -rf /opt/automake-$automakeVersion""",
                automakeVersion=automakeVersion, toolsdir=toolsdir)
    writer.emit("""RUN wget "ftp://ftp.gnu.org/gnu/libtool/libtool-$libtoolVersion.tar.gz" \\
        -O /opt/libtool.tar.gz && \\
    cd /opt && \\
    tar xf /opt/libtool.tar.gz && \\
    cd /opt/libtool-$libtoolVersion && \\
    ./configure --prefix=$toolsdir && \\
    make -j && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/libtool.tar.gz && \\
    rm -rf /opt/libtool-$libtoolVersion""",
                libtoolVersion=libtoolVersion, toolsdir=toolsdir)
    writer.emit("""RUN wget "https://github.com/westes/flex/releases/download/v$flexVersion/flex-$flexVersion.tar.gz" \\
        -O /opt/flex.tar.gz && \\
    cd /opt && \\
    tar xf flex.tar.gz && \\
    cd /opt/flex-$flexVersion && \\
    ./configure --prefix=$toolsdir && \\
    make -j && \\
    make install && \\
    cd /opt && \\
    rm -f /opt/flex.tar.gz && \\
    rm -rf /opt/flex-$flexVersion""", flexVersion=flexVersion, toolsdir=toolsdir)
    writer.emit("""ENV AUTOMAKE_JOBS=4
RUN git clone "https://github.com/open-mpi/ompi" /opt/ompi && \\
    cd /opt/ompi && \\
    ./autogen.pl && \\
    ./configure && \\
    make -j all && \\
    make install && \\
    cd /opt && \\
    rm -rf /opt/ompi""")
