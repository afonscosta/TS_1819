Para iniciar o projeto é necessário realizar os seguintes passos:

> pip install flask

> pip install python-dotenv

> chmod +x send_email.py

Mais ainda, é necessário descomentar a linha `user_allow_other` do ficheiro fuse.conf (normalmente no path `/etc/fuse.conf`).

O passo seguinte é compilar o sistema de ficheiros:

> make

De seguida, basta correr o script `run.sh`.

Por fim, caso seja a primeira vez que o FS é montado, então o administrador deve introduzir os seus dados no `database.txt` de forma a que possa gerir o acesso ao FS posteriormente.

> echo "<uid_do_admin>::<email_do_admin>" >> $HOME/.database.txt
