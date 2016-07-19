#!/bin/bash

unset GOROOT
export GOROOT=`realpath ../install`
export GOROOT_BOOTSTRAP=`realpath ../../go14/build/`
export GOROOT_FINAL="/"
export CGO_ENABLED=0
cd src
./make.bash
