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
    repo = "rapidsai"
    branch = "branch-" + kwargs["rapidsVersion"]
    writer.emit("""RUN wget "https://raw.githubusercontent.com/$repo/cuml/$branch/conda/environments/cuml_dev_cuda$cudaVersionShort.yml" \\
        -O cuml_dev.yml && \\
    conda env create -n cuml_dev -f cuml_dev.yml && \\
    rm -f cuml_dev.yml && \\
    conda clean --yes --all""",
                repo=repo,
                branch=branch,
                cudaVersionShort=cudaVersionShort)
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/cuml-dev /cuml-dev")
    writer.emit("COPY contexts/raft-dev /raft-dev")
