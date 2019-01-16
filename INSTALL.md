Para iniciar o projeto é necessário realizar os seguintes passos:

> pip install flask
> pip install python-dotenv

Mais ainda, é necessário descomentar a linha `user_allow_other` do ficheiro fuse.conf (normalmente no path `/etc/fuse.conf`).

O passo seguinte é compilar o sistema de ficheiros:

> make

Por fim, basta correr o script `run.sh`.
