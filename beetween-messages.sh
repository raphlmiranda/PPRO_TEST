#!/bin/bash

if [ $# -ne 3 ]; then
  echo "$0 <arquivo> <min> <max>"
  exit 1
fi

file_input="$1"

if [ ! -f "$file_input" ]; then
  echo "Arquivo $file_input não encontrado"
  exit 1
fi

min_input="$2"
max_input="$3"

awk -v min="$min_input" -v max="$max_input" '$3 >= min && $3 <= max' "$file_input"