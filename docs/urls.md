API will contain the following URLs:

- User related actions
	- ![][not-required] `POST /api/users/create`
	- ![][not-required] `POST /api/users/login`
	- ![][required] `GET/api/users/<user-id>`
	- ![][required] `POST /api/users/logout`
	- ![][required] `POST /api/users/<user-id>/update`
- Project related actions
	- ![][required] `POST /api/projects/create`
	- ![][required] `GET /api/projects/<project-id>`
	- ![][required] `GET /api/projects/filter`
	- ![][required] `POST /api/projects/<project-id>/update`
	- ![][required] `POST /api/projects/<project-id>/delete`
- Event related actions
	- ![][required] `POST /api/events/create`
	- ![][required] `GET /api/events/<event-id>`
	- ![][required] `GET /api/events/filter`
	- ![][required] `GET /api/events/<event-id>/delete`
	- ![][required] `GET /api/events/filter/delete`

[required]: https://img.shields.io/badge/auth-required-green.svg?style=flat-square
[not-required]: https://img.shields.io/badge/auth-not_required-red.svg?style=flat-square
