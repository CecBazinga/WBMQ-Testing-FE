FROM python:3.7.9-buster
LABEL maintainer="Alessandro Amici <a.amici@outlook.it>"
ADD WBMQ_Testing_FE.py /
RUN pip install Flask && \
	pip install requests
EXPOSE 5001
CMD ["python","./WBMQ_Testing_FE.py"]
