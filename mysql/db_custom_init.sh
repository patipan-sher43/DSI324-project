mysql -u root -p$MYSQL_ROOT_PASSWORD -e 'create database curriculum_dataset'
mysql -u root -p$MYSQL_ROOT_PASSWORD curriculum_dataset < /home/Data.sql
