from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import error
import upload
import mainPage
import edit
import stats
import charts

application = webapp.WSGIApplication(
                                     [('/', mainPage.MainPage),
                                      ('/stats', stats.Stats),
                                      ('/charts', charts.Charts),
                                      ('/add', upload.AddCSV),
                                      ('/edit', edit.Edit),
                                      ('/delete', edit.Delete),
                                      ('/err', error.Err)
                                     ],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
