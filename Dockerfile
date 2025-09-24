FROM kaspanet/rusty-kaspad:latest
LABEL org.opencontainers.image.title="research-pad" \
      org.opencontainers.image.description="Neutral build of the upstream index research node - data only" \
      org.opencontainers.image.source="https://github.com/KaspaDev/Rusty-Kaspa-Docker" \
      org.opencontainers.image.url="https://github.com/KaspaDev/Rusty-Kaspa-Docker" \
      org.opencontainers.image.vendor="KaspaDev (KRCBOT)" \
      org.opencontainers.image.authors="KaspaDev Community"
CMD ["entrypoint.sh", "kaspad"]
