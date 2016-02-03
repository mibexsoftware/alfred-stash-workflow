# Alfred Workflow for Atlassian Bitbucket Server (Stash) #

[![Build Status](http://img.shields.io/travis/mibexsoftware/alfred-stash-workflow.svg?style=flat-square)](https://travis-ci.org/mibexsoftware/alfred-stash-workflow)
[![Latest Version](http://img.shields.io/github/release/mibexsoftware/alfred-stash-workflow.svg?style=flat-square)](https://github.com/mibexsoftware/alfred-stash-workflow/releases)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](http://mibexsoftware.mit-license.org/2015)


Alfred workflow to search for projects, repositories and pull requests in [Atlassian Bitbucket Server (Stash)][stash].


![][screencast]


## Download ##

Get this Stash workflow for Alfred from [GitHub][gh-releases] or [Packal][packal-page]. See 
this [guide][alfred-workflow-installation] on how to install a workflow in Alfred (basically, you 
just have to open the file by double-clicking on it).


## Configuration ##

You have to configure the parameters for connecting to your Stash instance. Use the following command:

- `stash:config` — Configure the Stash host URL, and if necessary, a username and password


## Usage ##

Start typing `stash` in Alfred and you will be guided by a menu.

Please note that you can `CMD+C` a repository entry to get its clone URL.


## Icons ##

After a repository name you might sometimes see the following icons:

| Icon |                    Description                    |
|------|---------------------------------------------------|
|  ⑂   | Repository is a fork                              |
|  🔓   | Public repository                                 |


## Credits ##

Thanks to [Dean Jackson][deanishe] for building the awesome Python library [Alfred Workflow][alfred-workflow].
Also thanks to Ian Paterson for the awesome [Wunderlist Alfred workflow][wunderlist] which is one of the nicest 
menu-based Alfred workflows we’ve seen so far and which has inspired our workflow deeply.
Also thanks to Google for their nice [material design icons][google-material-design].


## License ##

This workflow, excluding the Atlassian Stash logo, is released under the [MIT Licence][mit].


## Author

![https://www.mibexsoftware.com][mibexlogo]


[stash]: http://www.atlassian.com/stash
[wunderlist]: https://github.com/idpaterson/alfred-wunderlist-workflow
[mibexlogo]: https://www.mibexsoftware.com/wp-content/uploads/2015/06/mibex.png
[deanishe]: hhttps://github.com/deanishe
[mit]: http://opensource.org/licenses/MIT
[alfred-workflow]: hhttps://github.com/deanishe
[gh-releases]: https://github.com/mibexsoftware/alfred-stash-workflow/releases
[packal-page]: http://www.packal.org/workflow/atlassian-stash-workflow
[screencast]: https://raw.githubusercontent.com/mibexsoftware/alfred-stash-workflow/master/screencast.gif
[alfred-workflow-installation]: http://support.alfredapp.com/workflows:installing/
[google-material-design]: https://github.com/google/material-design-icons
