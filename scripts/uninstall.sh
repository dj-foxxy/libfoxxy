#!/bin/bash
set -o errexit
set -o nounset

sudo rm -fr /usr/local/lib/python2.7/dist-packages/foxxy \
            /usr/local/lib/python2.7/dist-packages/libfoxxy-0.0.egg-info \
            /usr/local/lib/python2.7/dist-packages/libfoxxy-0.0-py2.7.egg

