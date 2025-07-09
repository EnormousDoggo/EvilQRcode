# Utilise l'image officielle Kali Rolling comme base
FROM kalilinux/kali-rolling

# Set non-interactive mode globally for the entire build
ENV DEBIAN_FRONTEND=noninteractive

# Met à jour le système et installe les outils nécessaires
RUN apt-get update && apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    #dig \
    whois \
    openssl \
    jq \
    whatweb \
    wafw00f \
    iputils-ping \
    net-tools \
    dnsutils \
    python3-pip \
    iproute2 \
    procps \
    wget \
    chromium \
    #python3-wafw00f \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# wafw00f nécessite parfois une mise à jour ou installation via pip
#RUN pip3 install --upgrade pip && \
#    pip3 install wafw00f

# Remove ENV in final image
RUN echo "unset DEBIAN_FRONTEND" >> ~/.bashrc

# Définir le point d’entrée par défaut
CMD [ "bash" ]