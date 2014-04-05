#import httplib2
import requests, json, flask
from launchpad.release_chart import ReleaseChart
from launchpad.lpdata import LaunchpadData

#httplib2.debuglevel = 1

app = flask.Flask(__name__)
lpdata = LaunchpadData()

@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>')
def bug_table_for_status(project_name, bug_type, milestone_name):
    project = lpdata.get_project(project_name)
    bugs = lpdata.get_bugs(project_name, LaunchpadData.BUG_STATUSES[bug_type], milestone_name)
    return flask.render_template("bug_table.html", project=project, bugs=bugs, bug_type=bug_type, milestone_name=milestone_name, selected_bug_table=True)

@app.route('/project/<project_name>/bug_table_for_tag/<bug_tag>/<milestone_name>')
def bug_table_for_tag(project_name, bug_tag, milestone_name):
    project = lpdata.get_project(project_name)
    bugs = lpdata.get_bugs(project_name, LaunchpadData.BUG_STATUSES_ALL, milestone_name, [bug_tag])
    return flask.render_template("bug_table.html", project=project, bugs=bugs, bug_tag=bug_tag, milestone_name=milestone_name, selected_bug_table=True, breakdown_by_status=True)

# The following method is a bit hacky.
@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>/<bug_tag>')
def bug_ids_for_tag(project_name, bug_type, milestone_name, bug_tag):
    project = lpdata.get_project(project_name)
    bugs = lpdata.get_bugs(project_name, LaunchpadData.BUG_STATUSES[bug_type], milestone_name, [bug_tag])
    data = [{'id': b.id} for b in bugs]
    js = json.dumps(data)
    resp = flask.Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/project/<project_name>')
def project_overview(project_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("project.html", project=project, selected_overview=True)

@app.route('/project/<project_name>/bug_trends/<milestone_name>')
def bug_trends(project_name, milestone_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("bug_trends.html", project=project, milestone_name=milestone_name, selected_bug_trends=True)

@app.route('/project/<project_name>/api/release_chart_trends/<milestone_name>/get_data')
def bug_report_trends_data(project_name, milestone_name):
    data = ReleaseChart(lpdata, project_name, milestone_name).get_trends_data()
    return flask.json.dumps(data)

@app.route('/project/<project_name>/api/release_chart_incoming_outgoing/<milestone_name>/get_data')
def bug_report_get_incoming_outgoing_data(project_name, milestone_name):
    data = ReleaseChart(lpdata, project_name, milestone_name).get_incoming_outgoing_data()
    return flask.json.dumps(data)

@app.route('/')
def main_page():
    return flask.redirect(flask.url_for("project_overview", project_name="fuel"))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 4444, threaded = True, debug = True)
