#!/bin/bash

docker:
	docker build -t stdprob -f ./Dockerfile .
	docker run -ti -d --name stdprob stdprob

travis:
	docker build -t stdprob -f ./Dockerfile .
	docker run -ti -d --name stdprob stdprob
	# Mount (-v volume) the current directory in /home/data in the container
	docker run -v `pwd`:/home/data stdprob bash -c "py.test --nbval --sanitize-with sanitize_nbval.cfg \
1d_problem.ipynb 2d_problem.ipynb 3d_problem_cylinder.ipynb"

test-ipynb:
	cd notebooks && py.test --nbval --sanitize-with sanitize_nbval.cfg \
		1d_problem.ipynb 2d_problem.ipynb 3d_problem_cylinder.ipynb

.PHONY: docker
