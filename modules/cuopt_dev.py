import modules.conda
import modules.cuda as cuda
import modules.jupyter

def cuopt_env(writer, cudaVersionShort, cuoptVersion):
    short = float(cudaVersionShort)
    repo = "NVIDIA"
    branch = "branch-" + cuoptVersion
    cu_short = cudaVersionShort.replace(".", "")
    writer.emit("""RUN wget "https://raw.githubusercontent.com/$repo/cuopt/refs/heads/$branch/conda/environments/all_cuda-${cu_short}_arch-x86_64.yaml" \\
        -O cuopt_dev.yaml && \\
    mamba env create -n cuopt_dev -f cuopt_dev.yaml && \\
    rm -f cuopt_dev.yaml && \\
    mamba clean -ya""",
                repo=repo,
                branch=branch,
                cu_short=cu_short)
    writer.condaPackages(["ccache", "pre-commit"],
                         channels=["conda-forge"], cmd="mamba")


def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "cuoptVersion" not in kwargs:
        raise Exception("'cuoptVersion' is mandatory!")
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersion"])
    cuopt_env(writer, cudaVersionShort, kwargs["cuoptVersion"])
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/envs/cuopt-dev /cuopt-dev")
