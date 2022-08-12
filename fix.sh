#!/bin/bash
# shellcheck disable=SC3000-SC4000

proj_dir="$(dirname "$0")"


echo -e "\nVerify errors and auto-fixing"
echo -e    "-----------------------------\n"

echo -e "\nPyright - static type ckecker"
pyright "$proj_dir"
echo -e "\nPycln - Remove unused imports"
pycln "$proj_dir"
echo -e "\nIsort - organize imports"
isort --profile black "$proj_dir"
echo -e "\nBlack formatter"
black "$proj_dir"




