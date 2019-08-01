import modules.conda


def emit(writer):
    modules.conda.emit(writer)
    writer.condaPackages(["h5py", "ipython", "jupyter", "matplotlib", "nose",
                          "numpy", "pandas", "Pillow", "scikit-learn", "scipy"])
