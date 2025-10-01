.PHONY: up down logs test

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

test:
	cp -n .env.example .env || true
	curl -s http://localhost:8080/healthz | jq .
	@echo "Flood test (expect some 429s):"
	@for i in $$(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/; done | sort | uniq -c
