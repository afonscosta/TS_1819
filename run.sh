#! /bin/bash

make

cp -r web-server-login $HOME/.web-server-login
cp -r web-server-pass $HOME/.web-server-pass
cp send_email.py $HOME/.send_email.py

./passthrough -omodules=subdir,subdir=$HOME -o auto_unmount -f mnt/

rm -r $HOME/.web-server-login
rm -r $HOME/.web-server-pass
rm $HOME/.send_email.py
rm $HOME/.database.txt
