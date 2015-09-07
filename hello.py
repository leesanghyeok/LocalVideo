import tornado.ioloop
import tornado.web
import os
import ast

prefix = "flask"

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		dirlist=[]
		walklist=[]
		checkexts=['mp4', 'm4v', 'f4v', 'mov','flv', 'webm']
		rootdir="E:\\Download\\Movie\\"
		for (path, dirs, files) in os.walk(rootdir):
			if path.split(os.path.sep)[-1] == "jwplayer" :
				continue

			for file in files:
				ext = os.path.splitext(file)[-1]
				for checkext in checkexts:
					if ext == '.'+checkext:
						tmp={
							'dir':path[len(rootdir):],
							'filename':os.path.splitext(file)[0],
							'ext':ext
						}
						dirlist.append(tmp)
		self.render("index.html", dirlist=dirlist,prefix=prefix)

class playerHandler(tornado.web.RequestHandler):
	def get(self):
		playlist = ast.literal_eval(self.get_argument('playlist'))
		self.render('player.html',playlist=playlist,prefix=prefix)

handler=[
    (r"/"+prefix, MainHandler),
    (r"/"+prefix+"/player", playerHandler),
    (r"/"+prefix+"/(.*)", tornado.web.StaticFileHandler, {"path":""}),
]

settings={
	"debug":True,
	"template_path":os.path.dirname(__file__),
}


if __name__ == "__main__":
    application = tornado.web.Application(handler,**settings)
    application.listen(4040)
    tornado.ioloop.IOLoop.instance().start()