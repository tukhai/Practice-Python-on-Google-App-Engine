import os
import re

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True) # if not give title a value, there would be exception
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True) # when the art is created, automatically set the time to the current time

class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC ") # store the cursor of this query to variable arts
        
        self.render("front.html", title=title, art=art, error=error, arts=arts)
    
    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)  # a is a new instance(object) of Art
                                               # where title variable of Art is the title value of post(self)
            a.put() # to store new Art object in the database
            self.redirect("/")  #  redirect to the front page
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)],debug=True)
