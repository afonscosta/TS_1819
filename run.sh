#! /bin/bash

make

cp -r web-server-login $HOME/.web-server-login
chmod -R u=rwx,g-rwx,o-rwx $HOME/.web-server-login

cp -r web-server-pass $HOME/.web-server-pass
chmod -R u=rwx,g-rwx,o-rwx $HOME/.web-server-pass

cp send_email.py $HOME/.send_email.py
chmod u=rwx,g=x,o-rwx $HOME/.send_email.py

cp .database.txt $HOME/.database.txt

./passthrough -omodules=subdir,subdir=$HOME -o default_permissions -o allow_other -o auto_unmount -f mnt/

rm -r $HOME/.web-server-login
rm -r $HOME/.web-server-pass
rm $HOME/.send_email.py
cp $HOME/.database.txt .
rm $HOME/.database.txt

