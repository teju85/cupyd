#!/usr/bin/env python
from string import Template
import inspect
import subprocess
import argparse
import shutil
import json
import os
import socket
import getpass
import tempfile
import sys
import glob
import importlib


def runcmd(cmd):
    print(cmd)
    subprocess.check_call(cmd, shell=True)


def dockercmd(*args):
    cmd = "docker " + " ".join(args)
    runcmd(cmd)


def dockercmdout(*args):
    cmd = "docker " + " ".join(args)
    return subprocess.check_output(cmd, shell=True)


def enrootcmd(datapath, *args):
    cmd = "ENROOT_DATA_PATH=" + datapath + " enroot " + " ".join(args)
    runcmd(cmd)

def copydir(src, dst):
    shutil.copytree(src, dst)


def findimage(args):
    image = args.img
    dir = args.path
    for file in glob.glob("%s/*.py" % dir):
        fullName = file.replace(dir + "/", "").replace(".py", "")
        module = importlib.import_module(fullName)
        imgs = module.images()
        for img in imgs.keys():
            if img == image:
                return module, imgs[img]
    if args.build:
        raise Exception("Failed to find image '%s'!" % image)
    else:
        return None, None


def listimages(dir="images"):
    imgs = []
    for file in glob.glob("%s/*.py" % dir):
        fullName = file.replace(dir + "/", "").replace(".py", "")
        module = importlib.import_module(fullName)
        imgs += module.images().keys()
    print("List of images supported:")
    for img in imgs:
        print(" . %s" % img)


def validateargs(args):
    if not args.list and args.img is None:
        raise Exception("'<img>' is mandatory if '-list' is not passed!")
    if args.build and args.pull:
        raise Exception("Cannot pass both '-build' and '-pull'!")
    if args.pull and args.push:
        raise Exception("Useless combination of options '-pull' and '-push'!")
    if args.build and not args.img:
        raise Exception("'<img>' is needed with '-build'!")
    if args.copy and not args.build:
        raise Exception("'-copy' is meaningful only with '-build'!")
    if args.create and not args.enrootdir:
        raise Exception("'-enrootdir' is mandatory with '-create'!")
    if args.enrootdir and not os.path.exists(args.enrootdir):
        raise Exception("'-enrootdir' does not exist!")
    if not args.list:
        args.module, args.imgArgs = findimage(args)


def parseargs():
    desc = "Wrapper to work with gpu containers"
    parser = argparse.ArgumentParser(description=desc)
    # options that are only valid with docker
    docker = parser.add_argument_group(
        "docker", "Options only valid when building/running via docker")
    docker.add_argument("-cap", default=[], action="append",
        help="Add capabilities to the container at runtime.")
    docker.add_argument("-copy", default=None, type=str,
        help="Copy the temporary build dir into this dir. Useful when one wants"
        " to share this with another person to build the images.")
    docker.add_argument("-dns", default=[], action="append", type=str,
        help="Pass DNS servers to be used inside container")
    docker.add_argument("-gdb", default=False, action="store_true",
        help="Enable ptrace capability needed for gdb sessions")
    docker.add_argument("-hostname", action="store_true", default=False,
        help="Pass '-h' option to docker run")
    docker.add_argument("-ipc", default=None, type=str,
        help="how to use shared memory between processes.")
    docker.add_argument("-noExposePorts", action="store_true", default=False,
        help="Do not expose ports to the host machine")
    docker.add_argument("-onlycopy", action="store_true", default=False,
        help="Only copy the Dockerfile folder")
    docker.add_argument("-path", default="images", type=str,
        help="Path where to find the definition of the images")
    docker.add_argument("-printComments", action="store_true", default=False,
        help="Print the origin of docker commands in the generated Dockerfile")
    docker.add_argument("-privileged", action="store_true", default=False,
        help="Pass a '--privileged' option to docker run command.")
    docker.add_argument("-repo", default="nvcr.io/nvidian/dt-compute/teju85-",
        type=str, help="Remote registry prefix to pull/push this image from/to")
    docker.add_argument("-security", type=str, default=None,
        help="Same as --security-opt option of docker")
    # options that work with both docker/enroot
    both = parser.add_argument_group(
        "both", "Options that work with both docker and enroot")
    both.add_argument("-env", default=[], action="append", type=str,
        help="Pass environmental variables to be used inside container")
    both.add_argument("-list", action="store_true", default=False,
        help="List all images supported")
    both.add_argument("-precmd", default=None, type=str,
        help="Run this command just *before* launching the container. This is "
        " valid only when the '-run' option is passed.")
    both.add_argument("-runas", choices=["user", "root", "uid"],
        default="user", type=str,
        help="Run as specified. Default is root. Options: "
        " user [run as current user by switching user inside the container]."
        " root [run as root, without any of these switching abilities]."
        " uid  ['-u' option to docker. To run on non-privileged containers].")
    both.add_argument("-v", default=[], action="append", type=str,
        help="Volumes to mount. Same syntax as docker run")
    # commands
    cmds = parser.add_argument_group(
        "commands", "Options that indicate a specific command")
    cmds.add_argument("-build", default=False, action="store_true",
        help="Build the docker image locally first. Cannot pass both '-build'"
        " and '-pull' options together!")
    cmds.add_argument("-create", default=False, action="store_true",
        help="Create enroot image from the docker image. If this option is passed"
        " then '-enrootdir' is mandatory!")
    cmds.add_argument("-pull", action="store_true", default=False,
        help="Pull the image first from a remote registry.")
    cmds.add_argument("-push", action="store_true", default=False,
        help="Push the local image to a remote registry.")
    cmds.add_argument("-run", default=False, action="store_true",
        help="Run the image to launch a container. If '-enrootdir' is passed"
        " then 'enroot start' will be used instead.")
    # enroot specific options
    enroot = parser.add_argument_group(
        "enroot", "Options that work only with enroot")
    enroot.add_argument("-enrootdir", default=None, type=str,
        help="Enroot data path variable (aka ENROOT_DATA_PATH env var)")
    # positional args
    parser.add_argument("img", type=str, nargs="?",
        help="Image to build/push/pull/run")
    parser.add_argument("cmd", nargs=argparse.REMAINDER,
        help="Command to run inside the container")
    args = parser.parse_args()
    args.path = args.path.rstrip("/")
    sys.path.append(args.path)
    args.enroot_img = args.img.replace(":", "+")
    validateargs(args)
    return args


class Puller:
    def __init__(self, args):
        self.args = args

    def run(self):
        here = self.args.img
        there = self.args.repo + here
        dockercmd("pull", there)
        dockercmd("tag", there, here)
        dockercmd("rmi", there)


class Pusher:
    def __init__(self, args):
        self.args = args

    def run(self):
        here = self.args.img
        there = self.args.repo + here
        dockercmd("tag", here, there)
        dockercmd("push", there)
        dockercmd("rmi", there)


class Creator:
    def __init__(self, args):
        self.args = args

    def __enter__(self):
        self.squash = self.args.enroot_img + ".sqsh"
        if os.path.exists(self.squash):
            os.unlink(self.squash)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if os.path.exists(self.squash):
            os.unlink(self.squash)

    def run(self):
        enrootcmd(self.args.enrootdir, "import", "--output", self.squash,
                  "dockerd://" + self.args.img)
        path = os.path.join(self.args.enrootdir, self.args.enroot_img)
        if os.path.exists(path):
            enrootcmd(self.args.enrootdir, "remove", "--force",
                      self.args.enroot_img)
        enrootcmd(self.args.enrootdir, "create", "--name", self.args.enroot_img,
                  self.squash)


class DockerRunner:
    def __init__(self, args):
        self.args = args

    def run(self):
        args = self.args
        finalcmd = ["-it", "--rm", "--runtime", "nvidia"]
        if not args.noExposePorts:
            finalcmd += self.__getPort(args.img)
        finalcmd += self.__getVols(args)
        finalcmd += self.__getUser(args)
        finalcmd += self.__getDns(args)
        finalcmd += self.__getHostname(args)
        finalcmd += self.__getHostIp(args)
        finalcmd += self.__getCapabilities(args)
        finalcmd += self.__getEnvVars(args)
        if args.privileged:
            finalcmd.append("--privileged")
        if args.ipc is not None:
            finalcmd += ["--ipc=%s" % args.ipc]
        if args.security is not None:
            finalcmd += ["--security-opt=\"%s\"" % args.security]
        if args.gdb:
            finalcmd += ["--cap-add=SYS_PTRACE", "--security-opt",
                         "seccomp=unconfined"]
        finalcmd.append(args.img)
        finalcmd += self.__getCmd(args)
        if args.precmd:
            print("Running pre-cmd before starting the container...")
            runcmd(args.precmd)
        dockercmd("run", *finalcmd)

    def __get(self, image, *args):
        output = dockercmdout("inspect", image)
        output = json.loads(output)[0]
        for a in args:
            if a not in output:
                return ""
            output = output[a]
        return output

    def __getCmd(self, args):
        if args.cmd is None:
            arr = self.__get(args.img, "Config", "Cmd")
            cmd = " ".join(arr) if len(arr) > 0 else "/bin/bash"
        elif len(args.cmd) > 0:
            cmd = " ".join(args.cmd)
        else:
            cmd = "/bin/bash"
        # single quotes around to directly pass this command to container!
        return ["'%s'" % cmd]

    def __getPort(self, image):
        arr = self.__get(image, "Config", "ExposedPorts")
        if len(arr) <= 0:
            return ""
        out = []
        for p in arr.keys():
            tmp = int(p.replace("/tcp", ""))
            # system ports?
            tmp1 = tmp + 8192 if tmp < 2048 else tmp
            out.append("-p %d:%d" % (tmp1, tmp))
        return out

    def __getIP(self, rhost):
        out = socket.getaddrinfo(rhost, 0)
        return out[0][4][0]

    def __getCurrentMount(self):
        cmd = []
        out = subprocess.check_output("df . | tail -n1 | awk '{print $1,$NF}'",
                                      shell=True)
        out = out.rstrip()
        out = out.decode("UTF-8")
        dirs = out.split(" ")
        tokens = dirs[0].split(":")
        # local mount
        if len(tokens) == 1:
            cwd = os.getcwd()
            cmd.append("-v %s:%s" % (cwd, cwd))
            cmd.append("-w %s" % cwd)
        # nfs mount
        elif len(tokens) == 2:
            (rhost, vol) = tokens
            ip = self.__getIP(rhost)
            basevol = os.path.basename(vol)
            volopts = [
                "o=addr=%s" % ip,
                "device=:%s" % vol,
                "type=nfs,source=%s,target=%s" % (basevol, dirs[1])
            ]
            mountopt = "type=volume"
            for vo in volopts:
                mountopt += ",volume-opt=%s" % vo
            cmd.append("--mount")
            cmd.append(mountopt)
            # TODO: doing this causes the following error!?
            # docker: Error response from daemon: chown /var/lib/docker/volumes/<volumeName>/_data: operation not permitted.
            #cmd.append("-w /work")
        else:
            raise Exception("Bad mount!?")
        return cmd

    def __getVols(self, args):
        vols = []
        for vol in args.v:
            vols.append("-v %s" % vol)
        vols += self.__getCurrentMount()
        return vols

    def __getDns(self, args):
        dns = []
        for d in args.dns:
            dns.append("--dns %s" % d)
        return dns

    def __getHostname(self, args):
        if not args.hostname:
            return []
        hn = "%s/%s" % (socket.gethostname(), args.img)
        return ["-h", hn]

    def __getHostIp(self, args):
        hostIp = socket.gethostbyname(socket.getfqdn())
        print("Host IP Address: %s" % hostIp)
        return ["-e", "HOST_IP=%s" % hostIp]

    def __getUser(self, args):
        out = []
        bindir = os.path.abspath(os.path.dirname(__file__))
        if args.runas == "user":
            out.append("-e RUNAS_UID=%d" % os.getuid())
            out.append("-e RUNAS_USER=%s" % getpass.getuser())
        elif args.runas == "uid":
            uid = os.getuid()
            gid = os.getgid()
            out.append("-u %d:%d" % (uid, gid))
            out.append("-e RUNAS_USER=%s" % getpass.getuser())
        return out

    def __getCapabilities(self, args):
        out = []
        for c in args.cap:
            out.append("--cap-add %s" % c)
        return out

    def __getEnvVars(self, args):
        out = []
        for e in args.env:
            out.append("-e %s" % e)
        return out


class EnrootRunner:
    def __init__(self, args):
        self.args = args

    def run(self):
        cmd = ["start"]
        cmd += self.__getVols()
        cmd += self.__getEnvVars()
        if self.args.runas == "root":
            cmd.append("--root")
        cmd.append(self.args.enroot_img)
        cmd += self.__getCmd()
        if self.args.precmd:
            print("Running pre-cmd before starting the enroot container...")
            runcmd(self.args.precmd)
        enrootcmd(self.args.enrootdir, *cmd)

    def __getVols(self):
        vols = []
        for vol in self.args.v:
            vols.append("-m %s" % vol)
        return vols

    def __getEnvVars(self):
        out = []
        for e in self.args.env:
            out.append("-e %s" % e)
        return out

    def __getCmd(self):
        if len(self.args.cmd) > 0:
            cmd = " ".join(self.args.cmd)
        else:
            cmd = "/bin/bash"
        # single quotes around to directly pass this command to container!
        return ["'%s'" % cmd]


class Writer:
    def __init__(self, verbose=False, file="Dockerfile"):
        self.verbose = verbose
        self.file = file
        self.fp = open(self.file, "w")
        self.past = set()
        self.fp.write("# Generated file. Do NOT modify!\n")
        self.fp.flush()

    def __del__(self):
        self.fp.close()

    def emit(self, str, caller=1, **kwargs):
        str = str.rstrip() + "\n"
        stack = inspect.stack()
        frameinfo = inspect.getframeinfo(stack[caller][0])
        frame = "%s:%d" % (frameinfo.filename, frameinfo.lineno)
        if frame in self.past:
            if self.verbose:
                self.fp.write("### %s already called\n" % frame)
                self.fp.flush()
            return
        self.past.add(frame)
        if self.verbose:
            start = "### Start: from %s ###\n" % frame
            end = "### End: from %s ###\n" % frame
            str = start + str + end
        s = Template(str)
        self.fp.write(s.substitute(kwargs))
        self.fp.flush()

    def packages(self, pkgs, caller=2, **kwargs):
        if len(pkgs) <= 0:
            return
        if "installOpts" not in kwargs:
            kwargs["installOpts"] = ""
        str = """RUN apt-get update && \\
    apt-get install -y --no-install-recommends $installOpts """
        for p in pkgs:
            str += "\\\n        %s " % p
        str += """&& \\
    rm -rf /var/lib/apt/lists/*"""
        self.emit(str, caller=caller, **kwargs)

    def condaPackages(self, pkgs, channels=[], env=None, caller=2, cmd="conda",
                      **kwargs):
        if len(pkgs) <= 0:
            return
        if "installOpts" not in kwargs:
            kwargs["installOpts"] = ""
        ch = "-c " + " -c ".join(channels) + " " if len(channels) > 0 else ""
        str = "RUN " + cmd + " install $installOpts " + ch
        if env is not None:
            str += " -n %s" % env
        for p in pkgs:
            str += "\\\n        %s " % p
        str += """&& \\
    %s clean -ya""" % cmd
        self.emit(str, caller=caller, **kwargs)

    def condaEnv(self, yamlFile, envName, cmd="conda", deleteYaml=False, caller=2):
        if deleteYaml:
            self.emit("""RUN \\
    $cmd env create -n $envName -f $yamlFile && \\
    rm -f $yamlFile && \\
    $cmd clean --yes --all""", cmd=cmd, caller=caller, envName=envName, yamlFile=yamlFile)
        else:
            self.emit("""RUN \\
    $cmd env create -n $envName -f $yamlFile && \\
    $cmd clean --yes --all""", cmd=cmd, caller=caller, envName=envName, yamlFile=yamlFile)


class Builder:
    def __init__(self, args):
        self.args = args
        self.builddir = tempfile.mkdtemp()
        self.pwd = os.getcwd()
        os.chdir(self.builddir)
        print("Working out of %s..." % self.builddir)

    def __enter__(self):
        self.writer = Writer(verbose=self.args.printComments)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self.writer
        os.chdir(self.pwd)
        if self.args.copy:
            print("Copying %s to %s..." % (self.builddir, self.args.copy))
            shutil.copytree(self.builddir, self.args.copy)
        print("Cleaning up %s..." % self.builddir)
        shutil.rmtree(self.builddir)

    def run(self):
        imgArgs = self.args.imgArgs
        print("Generating Dockerfile...")
        self.writer.emit("FROM %s\n" % imgArgs["base"])
        self.args.module.emit(writer=self.writer, **imgArgs)
        if "needsContext" in imgArgs and imgArgs["needsContext"]:
            print("Copying contexts...")
            copydir(os.path.join(self.pwd, "shared-contexts"),
                    os.path.join(self.builddir, "contexts"))
        if self.args.onlycopy:
            return
        print("Building image '%s'..." % self.args.img)
        dockercmd("build", "-t", self.args.img, ".")


if __name__ == "__main__":
    args = parseargs()
    if args.list:
        listimages(args.path)
        sys.exit(0)
    if args.build:
        with Builder(args) as b:
            b.run()
    elif args.pull:
        Puller(args).run()
    # push should only be done after a build!
    if args.push:
        Pusher(args).run()
    # enroot image creator should only be called after build/pull
    if args.create:
        with Creator(args) as c:
            c.run()
    # run happens only at the last!
    if args.run:
        if args.enrootdir:
            EnrootRunner(args).run()
        else:
            DockerRunner(args).run()
