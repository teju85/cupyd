
def emit(writer):
    writer.emit("ENV TZ=Europe/Kiev")
    writer.emit("RUN ln -snf /usr/share/zoneinfo/$$TZ /etc/localtime && echo $$TZ > /etc/timezone")
    writer.packages(["build-essential", "cmake", "git", "make"])
    writer.emit("""
RUN git clone https://github.com/opencv/opencv.git && \\
    git clone https://github.com/opencv/opencv_contrib.git && \\
    cd opencv && \\
    mkdir build && \\
    cd build && \\
    cmake \\
        -D CMAKE_BUILD_TYPE=Release \\
        -D CMAKE_INSTALL_PREFIX=/usr/local \\
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \\
        -D OPENCV_GENERATE_PKGCONFIG=yes \\
        -D WITH_CUDA=ON \\
        -D ENABLE_FAST_MATH=ON \\
        -D CUDA_FAST_MATH=1 \\
        -D WITH_CUBLAS=1 \\
        -D BUILD_TIFF=ON \\
        .. && \\
    make -j && \\
    make install && \\
    cd ../.. && \\
    rm -rf opencv opencv_contrib""")
