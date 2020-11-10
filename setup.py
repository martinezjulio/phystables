#!/usr/bin/env python
import distutils
import distutils.command.install_data
from distutils.core import setup
import os

icons = [os.path.join('.','phystables','creator','icons',i) for i in os.listdir(os.path.join('.','phystables','creator','icons')) if i[-4:] == '.png']

# Found at https://wiki.python.org/moin/Distutils/Tutorial for keeping image files with the package
class wx_smart_install_data(distutils.command.install_data.install_data):
    """need to change self.install_dir to the actual library dir"""
    def run(self):
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return distutils.command.install_data.install_data.run(self)


setup(name = 'phystables',
      version = '0.7',
      description = '2-D physics tables for intuitive physics psychology experiments',
      author = 'Kevin A Smith',
      author_email = 'k2smith@mit.edu',
      url = 'https://github.com/kasmith/phystables',
      packages = ['phystables','phystables.objects','phystables.utils','phystables.constants','phystables.creator',
                  'phystables.visualize','phystables.models', 'phystables.tables'],
      requires=['pymunk (>=5.0)', 'numpy', 'scipy', 'OptimTools'],
      data_files=[('phystables/creator/icons', icons)],
      cmdclass={'install_data': wx_smart_install_data}
      )
