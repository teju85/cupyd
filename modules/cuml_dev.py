import cudf


def emit(writer):
    writer.packages(["doxygen", "graphviz", "libopenblas-dev", "zlib1g-dev"])
    writer.emit("""RUN conda install -c anaconda -c pytorch \\
        scikit-learn && \\
    conda clean -ya""")
