ramdos

I accidentally committed a distribution file with a flag!
But it's okay! I completely removed it from the history with the following command, so the flag should never be detected when I distribute this file.

git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch flag.txt" --prune-empty -- --all
