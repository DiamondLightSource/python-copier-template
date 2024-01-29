#!/bin/bash

CONSTRAINTS="$(dirname $0)/constraints.txt"
if [ "$#" -eq 0 ]; then
    # Run with no args then always generate
    pip freeze --exclude-editable > $CONSTRAINTS
elif [ "$1" == "--if-non-empty" ]; then
    # Under pre-commit only generate if non empty
    [ -s "$CONSTRAINTS" ] && pip freeze --exclude-editable > $CONSTRAINTS
else
    # Not recognised, provide help
    cat <<EOF
Usage: $(basename "$0") [options]

Regenerates the pip constraints that will be used to make sure the dev
environment and production environment are using the same superset of
dependencies.

Writes $CONSTRAINTS

Options:
    --if-non-empty  Only regenerate if the file is non-empty. Use this
                    under pre-commit to allow optional constraints.
EOF
    exit 0;
fi
