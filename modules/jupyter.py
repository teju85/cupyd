# This assumes that jupyter has already been installed!
# This also assumes needsContext flag is set to true for the image.
def emit(writer, **kwargs):
    nbPort = kwargs["nbPort"] if "nbPort" in kwargs else "8888"
    writer.emit("COPY contexts/jupyter /jupyter")
    writer.emit("EXPOSE $nbPort", nbPort=nbPort)
