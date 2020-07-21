# PostgreSQL Backup Python tool
### Usage
```shell script
start.py -path -dbhost -dbport -dblogin -dbpassword -db -token -sid [-btime]
```

##### Arguments:
**-path**: path to pg_dump file. Version of pg_dump cannot be difference with PostgreSQL server version

**-dbhost**: database hostname

**-dbport**: database port

**-dblogin**: login of PostgreSQL user

**-dbpassword**: password of PostgreSQL user

**-db**: database name

**-token**: Telegram bot api token

**-sid**: Id of user or channel where Telegram bot will post backup files

**-btime**: Optional. Time between backups in minutes. Default is 1440 (24 hours)