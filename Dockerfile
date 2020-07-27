FROM python:3.8
ENV PYTHONBUFFERED 1
RUN mkdir /my_bug_tracker
WORKDIR /my_bug_tracker
ADD requirements.txt /my_bug_tracker/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /my_bug_tracker/