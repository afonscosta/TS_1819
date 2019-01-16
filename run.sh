#! /bin/bash

make

cp -r web-server-pass $HOME/.web-server-pass
chmod -R u=rwx,g-rwx,o-rwx $HOME/.web-server-pass

cp send_email.py $HOME/.send_email.py
chmod u=rwx,g=x,o-rwx $HOME/.send_email.py

if [ -f .database.txt ]; then
	cp .database.txt $HOME/.database.txt
fi

./passthrough -omodules=subdir,subdir=$HOME -o default_permissions -o allow_other -o auto_unmount -f mnt/

rm -r $HOME/.web-server-pass
rm $HOME/.send_email.py
if [ -f $HOME/.database.txt ]; then
	cp $HOME/.database.txt .
	rm $HOME/.database.txt
fi

