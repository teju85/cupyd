import modules.conda
import modules.cuda as cuda
import modules.jupyter

def ml_env(writer, cudaVersionShort, rapidsVersion):
    short = float(cudaVersionShort)
    repo = "rapidsai"
    branch = "branch-" + rapidsVersion
    writer.emit("""RUN wget "https://raw.githubusercontent.com/$repo/cuml/$branch/conda/environments/cuml_dev_cuda$cudaVersionShort.yml" \\
        -O cuml_dev.yml && \\
    mamba env create -n cuml_dev -f cuml_dev.yml && \\
    rm -f cuml_dev.yml && \\
    mamba clean -ya""",
                repo=repo,
                branch=branch,
                cudaVersionShort=cudaVersionShort)
    writer.condaPackages(["ccache", "clang=11.0.0", "clang-tools=11.0.0"],
                         channels=["conda-forge"], cmd="mamba")


def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersion"])
    ml_env(writer, cudaVersionShort, kwargs["rapidsVersion"])
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/envs/cuml-dev /cuml-dev")
    writer.emit("COPY contexts/envs/raft-dev /raft-dev")
