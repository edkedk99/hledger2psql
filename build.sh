#!/bin/bash

set -e

get_value() {
    sed -n "s/\($1 \?= \?\)\(.*\)/\2/p" setup.cfg
}

pkg_name="$(get_value name)"
version="$(get_value version)"
wheel="$pkg_name-$version-py3-none-any.whl"

./fix.sh
pip uninstall -y "$pkg_name"
python -m build
pip install "dist/$wheel"

