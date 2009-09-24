from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import views.error
import data.upload
import views.edit
import views.runs
import views.charts
import views.home

application = webapp.WSGIApplication(
                                     [('/', views.home.MainPage),
                                      ('/stats', views.runs.Stats),
                                      ('/charts', views.charts.Charts),
                                      ('/add', data.upload.AddCSV),
                                      ('/edit', views.edit.Edit),
                                      ('/delete', views.edit.Delete),
                                      ('/err', views.error.Err)
                                     ],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
