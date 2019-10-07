IMAGE:=naming

default: build run

build:
	docker build -t ${IMAGE}:latest .

run:
	docker run --rm  \
		--network playground \
		-v ${PWD}/data_files:/usr/src/app/data_files \
		${IMAGE} main.py


load_freq:
	docker run --rm  \
		--network playground \
		-v ${PWD}/data_files:/usr/src/app/data_files \
		${IMAGE} \
		process_chars_freq.py \
		data_files/caches/json/freq/0001-0500.json \
		data_files/caches/json/freq/0501-1000.json \
		data_files/caches/json/freq/1001-1500.json \
		data_files/caches/json/freq/1501-2000.json \
		 data_files/caches/json/freq/2001-2500.json \
		 data_files/caches/json/freq/2501-3000.json \
		 data_files/caches/json/freq/3001-3500.json \
		 data_files/caches/json/freq/3501-4000.json \
		data_files/caches/json/freq/4001-4500.json \
		data_files/caches/json/freq/4501-5000.json \
		data_files/caches/json/freq/5001-5500.json \
		data_files/caches/json/freq/5501-6000.json \
		data_files/caches/json/freq/6001-6500.json \
		data_files/caches/json/freq/6501-7000.json \
		data_files/caches/json/freq/7001-7072.json

load_sounds:
	docker run --rm  \
		--network playground \
		-v ${PWD}/data_files:/usr/src/app/data_files \
		${IMAGE} \
		parse_syllable_html.py data_files/caches/html/syllables/

load_strokes:
	docker run --rm  \
		--network playground \
		-v ${PWD}/data_files:/usr/src/app/data_files \
		${IMAGE} \
		set_chars_strokes.py