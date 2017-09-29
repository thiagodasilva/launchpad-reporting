from launchpadlib.launchpad import Launchpad
from bug import Bug
from project import Project
from ttl_cache import ttl_cache
from datetime import date
from dateutil.relativedelta import relativedelta


class LaunchpadData(object):

    BUG_STATUSES = {"New":        ["New"],
                    "Incomplete": ["Incomplete"],
                    "Open":       ["Triaged", "In Progress", "Confirmed"],
                    "Closed":     ["Fix Committed", "Fix Released", "Won't Fix", "Invalid", "Expired", "Opinion"]}

    BUG_STATUSES_ALL = BUG_STATUSES['New'] + BUG_STATUSES['Incomplete'] + \
        BUG_STATUSES['Open'] + BUG_STATUSES['Closed']

    def __init__(self):
        cachedir = "~/.launchpadlib/cache/"
        self.launchpad = Launchpad.login_anonymously('launchpad-reporting-www', 'production', cachedir)

    def _get_project(self, project_name):
        return self.launchpad.projects[project_name]

    def _get_milestone(self, project_name, milestone_name):
        project = self._get_project(project_name)
        return self.launchpad.load("%s/+milestone/%s" % (project.self_link, milestone_name))

    @ttl_cache(minutes=10)
    def get_project(self, project_name):
        return Project(self._get_project(project_name))

    @ttl_cache(minutes=10)
    def get_bugs(self, project_name, statuses, time_range=None, tags=None):
        project = self._get_project(project_name)
        today = date.today()

        # default target_date
        target_date = today + relativedelta(days=-90)
        try:
            target_date = today + relativedelta(days=-int(time_range))
        except (TypeError, ValueError):
            if (time_range == '1d'):
                target_date = today + relativedelta(days=-1)
            elif (time_range == '5d'):
                target_date = today + relativedelta(days=-5)
            elif (time_range == '1m'):
                target_date = today + relativedelta(months=-1)
            elif (time_range == '3m'):
                target_date = today + relativedelta(months=-3)
            elif (time_range == '6m'):
                target_date = today + relativedelta(months=-6)
            elif (time_range == '1y'):
                target_date = today + relativedelta(years=-1)
            else:
                return [Bug(r) for r in project.searchTasks(status=statuses)]

        return [Bug(r) for r in project.searchTasks(
                status=statuses, created_since=target_date.isoformat())]

    @staticmethod
    def dump_object(object):
        for name in dir(object):
            try:
                value = getattr(object, name)
            except AttributeError:
                value = "n/a"
            try:
                print name + " --- " + str(value)
            except ValueError:
                print name + " --- " + "n/a"
