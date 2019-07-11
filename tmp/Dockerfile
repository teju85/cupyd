ARG baseImage=ml-dev:10.0
FROM $baseImage

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       bison \
       cpanminus \
       curl \
       file \
       gcc-multilib \
       libexpat1-dev \
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
        IO::String \
        Params::Validate \
        SOAP::Lite \
        Time::HiRes \
        XML::Parser
