ARG baseImage=ml-dev:10.0
FROM $baseImage

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bison \
        cpanminus \
        curl \
        devmem2 \
        dos2unix \
        file \
        gcc-multilib \
        lib32z1 \
        libexpat1-dev \
        libpciaccess-dev \
        libssl-dev \
        make \
        openssl \
        perl \
        sudo \
        wget && \
    rm -rf /var/lib/apt/lists/*

RUN cpanm --force \
        Archive::Zip \
        Term::ReadKey \
        CGI \
        Clone \
        IO::String \
        Net::LDAP \
        Params::Validate \
        SOAP::Lite \
        Time::HiRes \
        XML::Parser

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libyaml-syck-perl && \
    rm -rf /var/lib/apt/lists/*

RUN cpanm --force \
    YAML::Syck
    
RUN cpanm --force \
    XML::SAX

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ypcat && \
    rm -rf /var/lib/apt/lists/*
