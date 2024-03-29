#! /bin/bash

make

cp -r web-server-pass $HOME/.web-server-pass
chmod -R u=rwx,g-rwx,o-rwx $HOME/.web-server-pass

cp send_email.py $HOME/.send_email.py
chmod u=rwx,g=x,o-rwx $HOME/.send_email.py

if [ -f .database.txt ]; then
	cp .database.txt $HOME/.database.txt
else
	if [ "$#" -ne 2 ]; then
		echo "Usage: ./run.sh <uid> <email>" >&2
		exit 1
	else
		touch $HOME/.database.txt
		chmod u=rw,g=r,o=r $HOME/.database.txt
		echo "$1::$2" >> $HOME/.database.txt
	fi
fi

./passthrough -omodules=subdir,subdir=$HOME -o default_permissions -o allow_other -o auto_unmount -f mnt/

rm -r $HOME/.web-server-pass
rm $HOME/.send_email.py
if [ -f $HOME/.database.txt ]; then
	cp $HOME/.database.txt .
	rm $HOME/.database.txt
fi

