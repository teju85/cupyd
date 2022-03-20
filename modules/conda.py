
def emit(writer):
    writer.packages(["build-essential", "ca-certificates", "git", "wget"])
    writer.emit("""RUN wget "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" \\
        -O /opt/miniconda.sh && \\
    chmod +x /opt/miniconda.sh && \\
    /opt/miniconda.sh -b -p /opt/conda && \\
    /opt/conda/bin/conda update -n base conda && \\
    rm /opt/miniconda.sh

ENV PATH /opt/conda/bin:$${PATH}""")
    writer.condaPackages(["libarchive", "mamba", "python=3.9"], channels=["base", "conda-forge"])
