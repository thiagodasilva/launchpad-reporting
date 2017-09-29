#import httplib2
import flask
from launchpad.release_chart import ReleaseChart
from launchpad.lpdata import LaunchpadData

#httplib2.debuglevel = 1

app = flask.Flask(__name__)
lpdata = LaunchpadData()

@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>')
def bug_table_for_status(project_name, bug_type, milestone_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("bug_table.html", project=project)

@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>/bug_list')
def bug_list(project_name, bug_type, milestone_name):
    project = lpdata.get_project(project_name)
    tags = None
    if 'tags' in flask.request.args:
        tags = flask.request.args['tags'].split(',')
    bugs = lpdata.get_bugs(project_name, LaunchpadData.BUG_STATUSES[bug_type], milestone_name, tags)
    return flask.render_template("bug_list.html", project=project, bugs=bugs, bug_type=bug_type, milestone_name=milestone_name, selected_bug_table=True)

@app.route('/project/<project_name>')
def project_overview(project_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("project.html", project=project, selected_overview=True)

@app.route('/project/<project_name>/bug_trends/<milestone_name>')
def bug_trends(project_name, milestone_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("bug_trends.html", project=project, milestone_name=milestone_name, selected_bug_trends=True)

@app.route('/project/<project_name>/api/release_chart_trends/<time_range>/get_data')
def bug_report_trends_data(project_name, time_range):
    data = ReleaseChart(lpdata, project_name, time_range).get_trends_data()
    return flask.json.dumps(data)

@app.route('/project/<project_name>/api/release_chart_incoming_outgoing/<time_range>/get_data')
def bug_report_get_incoming_outgoing_data(project_name, time_range):
    data = ReleaseChart(lpdata, project_name, time_range).get_incoming_outgoing_data()
    return flask.json.dumps(data)

@app.route('/')
def main_page():
    return flask.redirect(flask.url_for("project_overview", project_name="Swift"))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 4444, threaded = True, debug = True)
