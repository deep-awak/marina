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
FROM python:3.12-slim

WORKDIR /app

# The Makefile builds with `-custom`, producing a self-contained
# executable (bytecode + embedded runtime), so no OCaml install is
# needed at runtime -- only glibc, already present in this base image.
COPY --from=builder /home/opam/marina/marina /app/marina
COPY server.py /app/server.py

RUN chmod +x /app/marina

# Render sets $PORT at runtime; server.py reads it.
EXPOSE 8000
CMD ["python3", "/app/server.py"]
