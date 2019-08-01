import modules.build_essential


def emit(writer):
    modules.build_essential.emit(writer)
    writer.emit("""COPY contexts/runas /opt/runas
RUN cc -o /opt/runas/exec-as /opt/runas/exec-as.c
ENTRYPOINT ["/opt/runas/runas.sh"]""")
