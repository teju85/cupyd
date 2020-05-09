import modules.conda
import modules.cuda as cuda

def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    _, _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersionFull"])
    writer.emit("""RUN wget "https://raw.githubusercontent.com/rapidsai/cuml/branch-$rapidsVersion/conda/environments/cuml_dev_cuda$cudaVersionShort.yml" \\
        -O cuml_dev.yml && \\
    conda env create -n cuml_dev -f cuml_dev.yml && \\
    rm -f cuml_dev.yml && \\
    conda clean --yes --all""",
                rapidsVersion=kwargs["rapidsVersion"],
                cudaVersionShort=cudaVersionShort)
    writer.condaPackages(["flake8", "ipython", "jupyter"], channels=["anaconda"],
                         env="cuml_dev")
    writer.emit("COPY contexts/cuml-dev /cuml-dev")
    writer.emit("COPY contexts/raft-dev /raft-dev")
