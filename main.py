import web
web.template.Template.globals['datestr'] = web.datestr
db = web.database(dbn='postgres', db='rtask', user='postgres', pw='x')
render = web.template.render('templates/', cache=False)
urls = (
  '/', 'main', 
  '/edit_name', 'edit_name'
)

class main:
	def GET(self):
		r = db.select('tasks')
		return render.index(r[0])

class edit_name:
	def POST(self):
		i = web.input('id', 'name')
		db.update('tasks', where="id=$id", name=i.name, vars=i)
		raise web.seeother('/')

app = web.application(urls, globals())
if __name__ == "__main__":
	app.run()
