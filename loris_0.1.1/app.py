import loris


@loris.controller
def hello(req):
	if req.method == 'POST':
		return 'Hello %s!' % req.params['name']
	elif req.method == 'GET':
		return '''<form method="POST">
			You're name: <input type="text" name="name">
			<input type="submit">
			</form>'''

hello_world = loris.Router()
hello_world.add_route('/', controller=hello)

if __name__ == '__main__':
    loris.run(hello_world)