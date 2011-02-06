import web

web.template.Template.globals['datestr'] = web.datestr
web.template.Template.globals['len'] = len

db = web.database(dbn='postgres', db='rtask', user='postgres', pw='x')
render = web.template.render('templates/', cache=False)
now = web.SQLLiteral('now()')

urls = (
  '/', 'main', 
  '/add', 'add',
  '/edit', 'edit',
  '/reset', 'reset'
)

class main:
	def GET(self):
		q = "and completed is null and (postponed_until is null or postponed_until < now()) and someday is null"
		focus = db.select('tasks', where="stalled='f' " + q)
		stalled = db.select('tasks', where="stalled='t' " + q)
		return render.index(focus, stalled)

class add:
	def POST(self):
		i = web.input('name')
		db.insert('tasks', name=i.name)
		raise web.seeother('/')

class edit:
	def POST(self):
		i = web.input('id')
		out = web.storage()
		if i.get('name'):
			out.name = i.name
		elif i.get('stall'):
			out.stalled=True
		elif i.get('finished'):
			out.completed = now 
			out.gave_up = (i.finished=='gaveup')
		elif i.get('postpone'):
			if i.postpone == 'someday':
				out.someday = True
			else:
				out.postponed_until = web.SQLLiteral('now() + ' + web.sqlquote(i.postpone)) 
		db.update('tasks', where="id=$id", vars=i, **out)
		raise web.seeother('/')

class reset:
	def POST(self):
		db.update('tasks', where="stalled='t'", stalled=False)
		raise web.seeother('/')

app = web.application(urls, globals())
if __name__ == "__main__":
	app.run()
