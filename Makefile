build:
	docker-compose build

# --noinput: Suppresses all user prompts
# For migrate it is much trickier because of django signaling. The migrate
# management itself does not ask any questions, but other installed apps may
# hook into the pre_migrate_signal or post_migrate_signal and handle
# interactivity in their own way
migrate:
	docker-compose run app python manage.py migrate --noinput

# --noinput: Suppresses all user prompts
migrations:
	docker-compose run app python manage.py makemigrations --noinput

ps:
	docker-compose ps

# -d: detached mode - run containers in the background
run:
	docker-compose up -d

restart:
	docker-compose stop
	docker-compose up -d

shell:
	docker-compose run app sh

stop:
	docker-compose stop

test:
	docker-compose run app python manage.py test

test_flake8:
	docker-compose run app sh -c "python manage.py test && flake8 --exclude=*/migrations/, settings.py"


