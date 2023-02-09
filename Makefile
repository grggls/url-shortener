app_name = url_shortener

run:
	@docker build -t $(app_name) .
	@docker run --detach -p 8000:8000 $(app_name)
	@sleep 2
	@curl localhost:8000

kill:
	@echo 'Killing container...'
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker kill
