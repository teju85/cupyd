import modules.conda
import modules.cuda as cuda
import modules.jupyter

def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersion"])
    short = float(cudaVersionShort)
    # HACK!
    if short >= 11.0:
        cudaVersionShort = "10.2"
    writer.emit("""RUN wget "https://raw.githubusercontent.com/rapidsai/cuml/branch-$rapidsVersion/conda/environments/cuml_dev_cuda$cudaVersionShort.yml" \\
        -O cuml_dev.yml && \\
    echo "- notebook>=0.5.0" >> cuml_dev.yml && \\
    echo "- flake8" >> cuml_dev.yml && \\
    conda env create -n cuml_dev -f cuml_dev.yml && \\
    rm -f cuml_dev.yml && \\
    conda clean --yes --all""",
                rapidsVersion=kwargs["rapidsVersion"],
                cudaVersionShort=cudaVersionShort)
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/cuml-dev /cuml-dev")
    writer.emit("COPY contexts/raft-dev /raft-dev")
