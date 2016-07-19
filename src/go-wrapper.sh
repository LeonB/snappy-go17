#!/bin/sh

export GOROOT="$SNAP/$GOROOT"
$SNAP/bin/go $@
