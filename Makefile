NAME	:= CMDB
MANAGER	:= ./manage.py


migrate:
	${MANAGER} makemigrations
	${MANAGER} migrate

