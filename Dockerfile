FROM ocaml/opam:debian-ocaml-4.13 AS builder

WORKDIR /home/opam/marina
USER opam

COPY --chown=opam:opam . .

RUN opam install -y ocamlfind ounit2 \
    && eval $(opam env) \
    && make

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /home/opam/marina/marina /app/marina
COPY server.py /app/server.py

RUN chmod +x /app/marina

EXPOSE 8000
CMD ["python3", "/app/server.py"]
