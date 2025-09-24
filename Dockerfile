FROM kaspanet/rusty-kaspad:latest
LABEL org.opencontainers.image.title="research-pad" \
      org.opencontainers.image.description="Neutral build of the upstream index research node - data only" \
      org.opencontainers.image.source="local"
CMD ["entrypoint.sh", "kaspad"]
