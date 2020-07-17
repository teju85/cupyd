import modules.conda
import modules.jupyter

def emit(writer, **kwargs):
    modules.conda.emit(writer)
    tmp_file = "/tmp/gnn_dev.yml"
    writer.emit("""RUN \\
    echo "name: gnn_dev" > $tmp_file && \\
    echo "channels:" >> $tmp_file && \\
    echo "  - rapidsai" >> $tmp_file && \\
    echo "  - nvidia" >> $tmp_file && \\
    echo "  - conda-forge" >> $tmp_file && \\
    echo "dependencies:" >> $tmp_file && \\
    echo "  - clang=8.0.1" >> $tmp_file && \\
    echo "  - clang-tools=8.0.1" >> $tmp_file && \\
    echo "  - cmake=3.14.5" >> $tmp_file && \\
    echo "  - cython>=0.29,<0.30" >> $tmp_file && \\
    echo "  - doxygen" >> $tmp_file && \\
    echo "  - flake8" >> $tmp_file && \\
    echo "  - pytest>=4.6" >> $tmp_file && \\
    echo "  - scikit-learn>=0.21" >> $tmp_file && \\
    conda env create -n gnn_dev -f $tmp_file && \\
    rm -f $tmp_file && \\
    conda clean --yes --all""", tmp_file=tmp_file)
    modules.jupyter.emit(writer, **kwargs)
