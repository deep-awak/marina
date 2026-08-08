# ---------- Build stage ----------
FROM ocaml/opam:debian-ocaml-4.13 AS builder

WORKDIR /home/opam/marina
USER opam

# Copy sources
COPY --chown=opam:opam . .

# Install build dependencies and compile
RUN opam install -y ocamlfind ounit2 \
    && eval $(opam env) \
    && make

# ---------- Runtime stage ----------
FROM debian:bookworm-slim

WORKDIR /app

# The Makefile builds with `-custom`, producing a self-contained
# executable (bytecode + embedded runtime), so no OCaml install is
# needed at runtime — only glibc, already present in this base image.
COPY --from=builder /home/opam/marina/marina /app/marina

COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh /app/marina

ENTRYPOINT ["/app/docker-entrypoint.sh"]
