import conda


def emit(writer):
    conda.emit(writer)
    writer.condaPackages(["h5py", "ipython", "jupyter", "matplotlib", "nose",
                          "numpy", "pandas", "Pillow", "scikit-learn", "scipy"])
