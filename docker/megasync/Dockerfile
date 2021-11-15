FROM alpine:edge

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk add --no-cache libcurl c-ares crypto++ zlib openssl sqlite-libs readline libsodium \
    && apk add --no-cache --virtual .build-deps file git make automake autoconf libtool gcc libc-dev g++ curl-dev c-ares-dev crypto++-dev zlib-dev openssl-dev sqlite-dev readline-dev libsodium-dev \
    && git clone -b v3.6.3 --depth 1 https://github.com/meganz/sdk.git \
    && cd sdk \
    && ./autogen.sh \
    && CXXFLAGS="-O2 -Wno-deprecated-declarations --param ggc-min-expand=1" ./configure --without-freeimage \
    && make examples/megacli  \
    && make examples/megasimplesync \
    && make install \
    && cd ../ \
    && rm -rf sdk \
    && apk del .build-deps

