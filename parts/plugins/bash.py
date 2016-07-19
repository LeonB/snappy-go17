# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The bash plugin is useful for building script based parts.
Bash based projects use scripts which drive the build.
This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.
Additionally, this plugin uses the following plugin-specific keyword:
    - script:
      (string)
      Run the given script name.
    - stages:
      (list of strings)
      Run the script in the given stages. (default: ['build'])
    - pull-arguments:
      (list of strings)
      Pass the given arguments to the script during the pull stage.
    - build-arguments:
      (list of strings)
      Pass the given arguments to the script during the build stage.
"""

import snapcraft
import os
import shutil

class BashPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        schema['properties']['script'] = {
            'type': 'string',

        }
        schema['properties']['install'] = {
            'type': 'boolean',
            'default': True,
        }
        schema['properties']['destination'] = {
            'type': 'string',
            'default': '',
        }
        schema['properties']['stages'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': ['build'],
        }
        schema['properties']['pull-arguments'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }
        schema['properties']['build-arguments'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['required'].extend(['script'])
        schema['build-properties'].extend(['stages'])
        schema['build-properties'].extend(['pull-arguments'])
        schema['build-properties'].extend(['build-arguments'])

        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self.build_packages.append('bash')

    def pull(self):
        super().pull()

        if "pull" in self.options.stages:
            command = [self.sourcedir + '/' + self.options.script]
            command.extend(self.options.pull_arguments)

            self.run(command)

    def build(self):
        super().build()

        if "build" in self.options.stages:
            script = os.path.basename(self.options.script)
            command = [self.builddir + '/' + script]
            command.extend(self.options.build_arguments)

            if os.path.isfile(self.options.script):
                shutil.copy(
                    self.options.script,
                    self.builddir
                )

            self.run(command)

            if self.options.install:
                self.install()

    def install(self):
        installdir = self.installdir

        # Check override for installation directory
        if self.options.destination:
            installdir = os.path.join(self.installdir, self.options.destination)

        # Clean install dir if it already exists
        if os.path.exists(installdir):
            shutil.rmtree(installdir)

        shutil.copytree(self.builddir, installdir)
