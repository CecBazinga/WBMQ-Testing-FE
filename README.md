# WBMQ-Testing-FE

Multithreaded testing controller written in python for [WBMQSystemProject](https://github.com/CecBazinga/WBMQSystemProject). Spawning variable numbers of publisher (sensors) and fixed number of subscribers (bots) as main use case

## Installation

Controller works on internal IP address of the machine, listening on port "5001". It is necessary to port forwarding. 

```bash
  	# Dependencies
  	pip install Flask
	pip install requests
  
  	# Actual running
	python WBMQ_Testing_FE.py
```

Testing app can be also deployed on AWS service using. Dockerfile is present in main folder.
Follow the information given here [WBMQSystemProject](https://github.com/CecBazinga/WBMQSystemProject)
