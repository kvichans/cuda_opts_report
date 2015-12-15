''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on githab)
Version:
    '1.0.2 2015-12-15'
'''

from .cd_opts_report import Command as CommandRLS

RLS  = CommandRLS()
class Command:
    def run(self):  return RLS.run()
