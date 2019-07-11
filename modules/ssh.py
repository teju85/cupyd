
def emit(writer, sshPort="22"):
    writer.emit("""ENV DEBIAN_FRONTEND noninteractive
EXPOSE $sshPort""", sshPort=sshPort)
    writer.packages(["openssh-server"])
    writer.emit("""COPY "contexts/ssh" "/opt/ssh/"

# Hook up the start script as a pre-switch command
# That way '-runas user' launch option should also work
ENV RUNAS_PRE_SWITCH_CMD "/opt/ssh/start.sh"

# /etc/pam.d/sshd: SSH login fix. Otherwise user is kicked off after login
RUN mkdir -p /var/run/sshd && \\
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \\
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \\
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \\
    echo "root:root" | chpasswd""")
