import modules.cuda_dev
import modules.runas
import modules.ssh


def emit(writer, **kwargs):
    modules.runas.emit(writer)
    args = {}
    if "sshPort" in kwargs:
        args["sshPort"] = kwargs
    if "nsightPort" in kwargs:
        args["nsightPort"] = kwargs
    modules.ssh.emit(writer, **args)
    writer.packages(["libc6-dbg", "gdb", "valgrind"])
