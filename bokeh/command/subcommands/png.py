'''
To generate a standalone PNG file for a Bokeh application from a single
Python script, pass the script name to ``bokeh png`` on the command
line:

.. code-block:: sh

    bokeh png app_script.py

The generated PNG will be saved in the current working directory with
the name ``app_script.png``.

It is also possible to run the same commmand with jupyter notebooks:

.. code-block:: sh

    bokeh png app_notebook.ipynb

This will generate an PNG file named ``app_notebook.png`` just like
with a python script.

Applications can also be created from directories. The directory should
contain a ``main.py`` (and any other helper modules that are required) as
well as any additional assets (e.g., theme files). Pass the directory name
to ``bokeh png`` to generate the PNG:

.. code-block:: sh

    bokeh png app_dir

It is possible to generate PNG files for multiple applications at once:

.. code-block:: sh

    bokeh png app_script.py app_dir

For all cases, it's required to explicitly add a Bokeh layout to
``bokeh.io.curdoc`` for it to appear in the output.

'''
from __future__ import absolute_import

import io
import sys
import warnings

from ...io.export import get_screenshot_as_png, create_webdriver, terminate_webdriver
from ...models.plots import Plot
from .file_output import FileOutputSubcommand

class PNG(FileOutputSubcommand):
    ''' Subcommand to output applications as standalone PNG files.

    '''

    #: name for this subcommand
    name = "png"

    #: file extension for output generated by this :class:`~bokeh.command.subcommands.file_output.FileOutputSubcommand`
    extension = "png"

    help = "Create standalone PNG files for one or more applications"

    args = (

        FileOutputSubcommand.files_arg("PNG"),

        ('--height', dict(
            metavar='HEIGHT',
            type=int,
            help="The desired height of the exported layout obj only if it's a Plot instance",
            default=None,
        )),

        ('--width', dict(
            metavar='WIDTH',
            type=int,
            help="The desired width of the exported layout obj only if it's a Plot instance",
            default=None,
        )),

    ) + FileOutputSubcommand.other_args()

    def invoke(self, args):
        '''

        '''
        self.driver = create_webdriver()
        try:
            super(PNG, self).invoke(args)
        finally:
            terminate_webdriver(self.driver)

    def write_file(self, args, filename, doc):
        '''

        '''
        contents = self.file_contents(args, doc)
        if filename == '-':
            sys.stdout.buffer.write(contents)
        else:
            with io.open(filename, "w+b") as f:
                f.write(contents)
        self.after_write_file(args, filename, doc)

    def file_contents(self, args, doc):
        '''

        '''
        if args.width is not None or args.height is not None:
            layout = doc.roots
            if len(layout) != 1 or not isinstance(layout[0], Plot):
                warnings.warn("Export called with height or width kwargs on a non-single Plot layout. The size values will be ignored.")
            else:
                plot = layout[0]
                plot.plot_height = args.height or plot.plot_height
                plot.plot_width  = args.width or plot.plot_width

        image = get_screenshot_as_png(doc, driver=self.driver)
        buf = io.BytesIO()
        image.save(buf, "png")
        buf.seek(0)
        return buf.read()
