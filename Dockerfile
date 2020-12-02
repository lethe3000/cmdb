FROM harbor.ops.yunlizhi.cn/runtime/python:3.8-django-3

ADD *.txt /
RUN pip install --no-cache-dir --trusted-host mirrors.cloud.aliyuncs.com -i http://mirrors.cloud.aliyuncs.com/pypi/simple -r /requirements.txt
ADD . /app
WORKDIR /app
CMD uwsgi -i uwsgi.ini
