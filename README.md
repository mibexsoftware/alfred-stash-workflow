# Alfred Workflow for Atlassian Stash #

[![Build Status](http://img.shields.io/travis/mibexsoftware/alfred-stash-workflow.svg?style=flat-square)](https://travis-ci.org/mibexsoftware/alfred-stash-workflow)
[![Coverage Status](https://coveralls.io/repos/mibexsoftware/alfred-stash-workflow/badge.svg?branch=master&service=github)](https://coveralls.io/github/mibexsoftware/alfred-stash-workflow?branch=master)
[![Latest Version](http://img.shields.io/github/release/mibexsoftware/alfred-stash-workflow.svg?style=flat-square)](https://github.com/mibexsoftware/alfred-stash-workflow/releases)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](http://mibexsoftware.mit-license.org/2015)


Alfred workflow to search for projects, repositories and pull requests to review in [Atlassian Stash][stash].


![][screencast]


## Download ##

Get this Stash workflow for Alfred from [GitHub][gh-releases] or [Packal][packal-page]. See this [guide][alfred-workflow-installation] on how to install a workflow in Alfred (basically, you just have to open the file by double-clicking on it).


## Usage ##

- `stash repos [query]` — View/search for repositories in Stash
	+ `↩` — Open repository page on Stash in your browser
	+ `⌘+C` — Copy repository's clone URL to your clipboard
- `stash projects [query]` — View/search for projects in Stash
	+ `↩` Open project page on Stash in your browser
- `stash pullrequests [query]` — View/search for pull requests to review for the configured user in Stash
	+ `↩` Open pull request page on Stash in your browser


## Configuration ##

You have to configure the parameters for connecting to your Stash instance. Use the following commands:

- `stash config host [host_url]` — Configure the URL to your Stash host
- `stash config user [user_name]` — Configure the name of your Stash user
- `stash config password [password]` — Configure the password of your Stash user (will be stored encrypted in Keychain)
- `stash config verifycert [true|false]` — Enable/disable certificate verification for your connection to Stash (if you use a self-signed certificate, you might want to disable this)

If you want to verify if your connection parameters are valid, use the following command:

- `stash config check` — Verifies if a connection to Stash can be established by using the entered connection parameters

Further configuration commands:

- `stash config delcache` — Deletes the cached Stash infos


## Icons ##

After a repository name you might sometimes see the following icons:

| Icon |                    Description                    |
|------|---------------------------------------------------|
|  ⑂   | Repository is a fork                              |
|  🔓   | Public repository                                 |


## Credits ##

Thanks to [Dean Jackson][deanishe] for building the awesome Python library [Alfred Workflow][alfred-workflow].


## License ##

This workflow, excluding the Atlassian Stash logo, is released under the [MIT Licence][mit].


## Author

![https://www.mibexsoftware.com][mibexlogo]


[stash]: http://www.atlassian.com/stash
[mibexlogo]: https://www.mibexsoftware.com/wp-content/uploads/2015/06/mibex.png
[deanishe]: hhttps://github.com/deanishe
[mit]: http://opensource.org/licenses/MIT
[alfred-workflow]: hhttps://github.com/deanishe
[gh-releases]: https://github.com/mibexsoftware/alfred-stash-workflow/releases
[packal-page]: http://www.packal.org/workflow/atlassian-stash-workflow
[screencast]: https://raw.githubusercontent.com/mibexsoftware/alfred-stash-workflow/master/screencast.gif
[alfred-workflow-installation]: http://support.alfredapp.com/workflows:installing/
