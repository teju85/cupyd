
def emit(writer):
    writer.packages(["build-essential", "ca-certificates", "curl", "git"])
    writer.emit("""RUN curl -o /opt/miniconda.sh \\
        -O "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" && \\
    chmod +x /opt/miniconda.sh && \\
    /opt/miniconda.sh -b -p /opt/conda && \\
    /opt/conda/bin/conda update -n base conda && \\
    rm /opt/miniconda.sh

ENV PATH /opt/conda/bin:$${PATH}""")
