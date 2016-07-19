#!/bin/bash

unset GOROOT
export CGO_ENABLED=0
cd src
./make.bash
