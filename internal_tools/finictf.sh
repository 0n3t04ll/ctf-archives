#!/bin/bash

current_dir=`pwd`
ctf_dir=${current_dir#`git rev-parse --show-toplevel`/ctfs/}
ctf_name="${ctf_dir%%/*}"

cd $(git rev-parse --show-toplevel)

git add --all
git clean -f -d
git commit -am "$ctf_name challs"
git push
