FROM python:3.7.9-buster
LABEL maintainer="Alessandro Amici <alessandro.amici@alumni.uniroma2.eu>, Cecilia Calavaro <cecilia.calavaro@alumni.uniroma2.eu>, Roberto Pavia <roberto.pavia@alumni.uniroma2.eu>"
ADD WBMQ_Testing_FE.py /
RUN pip install Flask && \
	pip install requests
EXPOSE 5001
CMD ["python","./WBMQ_Testing_FE.py"]
