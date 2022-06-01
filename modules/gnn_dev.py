import modules.conda
import modules.cuda as cuda
import modules.jupyter


def gnn_env(writer):
    writer.emit("COPY contexts/envs/gnn_dev.yaml /tmp/gnn_dev.yaml")
    writer.condaEnv("/tmp/gnn_dev.yaml", "gnn_dev", deleteYaml=True)


def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersion"])
    gnn_env(writer)
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/envs/gnn-dev /gnn-dev")
