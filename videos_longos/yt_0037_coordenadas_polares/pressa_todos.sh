#!/bin/bash
# yt_0037: PRESSA=grava de todos os lotes (um por vez, dois fluxos em paralelo pelo chamador). uso: ./pressa_todos.sh LOTES...
cd "$(dirname "$0")"
for C in "$@"; do ./pressa.sh $C; done
