#===============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import threading
import wx
import urllib2
import json
import config
import service
import dateutil.parser
import calendar

class CheckUpdateThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.settings = service.settings.UpdateSettings.getInstance()
        self.network = service.Network.getInstance()

    def run(self):
        network = service.Network.getInstance()

        try:
            response = network.request('https://api.github.com/repos/pyfa-org/Pyfa/releases', network.UPDATE)
            jsonResponse = json.loads(response.read())
            jsonResponse.sort(key=lambda x: calendar.timegm(dateutil.parser.parse(x['published_at']).utctimetuple()), reverse=True)

            for release in jsonResponse:
                # Suppress pre releases
                if (release['prerelease'] and self.settings.get('prerelease')):
                    continue

                # Handle use-case of updating to suppressed version
                if self.settings.get('version') == 'v'+config.version:
                    self.settings.set('version', None)

                # Suppress version
                if (release['tag_name'] == self.settings.get('version')):
                    break

                # Set the release version that we will be comparing with.
                if release['prerelease']:
                    rVersion = release['tag_name'].replace('singularity-', '', 1)
                else:
                    rVersion = release['tag_name'].replace('v', '', 1)

                if config.tag is 'git' and not release['prerelease'] and self.versiontuple(rVersion) >= self.versiontuple(config.version):
                    wx.CallAfter(self.callback, release) # git (dev/Singularity) -> Stable
                elif config.expansionName is not "Singularity":
                    if release['prerelease']:
                        wx.CallAfter(self.callback, release) # Stable -> Singularity
                    elif self.versiontuple(rVersion) > self.versiontuple(config.version):
                        wx.CallAfter(self.callback, release) # Stable -> Stable
                else:
                    if release['prerelease'] and rVersion > config.expansionVersion:
                        wx.CallAfter(self.callback, release) # Singularity -> Singularity
                break
        except:
            pass

    def versiontuple(self, v):
        return tuple(map(int, (v.split("."))))

class Update():
    instance = None
    def __init__(self):
       pass

    def CheckUpdate(self, callback):
        thread = CheckUpdateThread(callback)
        thread.start()

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Update()
        return cls.instance


