launchpad-reporting
===================

Convenient web-based front-end for Launchpad. Displays bug tables and charts for a Launchpad project (currently hard-coded to project Openstack Swift).


Getting Started
===============

```
# git clone git@github.com:thiagodasilva/launchpad-reporting.git
# cd launchpad-reporting
# docker build --rm -t lp_report:dev .
# docker run -d -p 4444:4444 lp_report:dev
```

After that, open http://localhost:4444 in your browser.


How it works
============
- Flask is used as a web frontend
- d3 & nvd3 are used for the charts
- Interation with Launchpad is done through launchpadlib
- The code is optimized to retrieve data from launchpad using the minimum amount of queries. Still, it can take up to 5-10 seconds for a query to complete (for a milestone with hundreds of bugs)
- The results retrieved from Launchpad are cached for 5 minutes. See decorator @ttl_cache


Limitations
===========
- Does not show private bugs, as it requires more complex authentication flow with Launchpad


Screenshots
===========
![Image of Dashboard](https://github.com/thiagodasilva/launchpad-reporting/raw/master/screenshots/release_bug_trends.png)
