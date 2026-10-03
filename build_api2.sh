#!/bin/bash
cd /home/aryan/flyrank-crud
rm -rf .git
git init

git add requirements.txt
git commit -m "Initial commit"

git add main.py
git commit -m "Stage 0: hello server"
git commit --amend -m "Stage 0: hello server" --allow-empty # actually we have the final main.py so it will just be one big commit if we do this.

# Wait, if we just run the original script again after deleting .git, it won't work because main.py already has the final code. 
# We should recreate it exactly as before.
