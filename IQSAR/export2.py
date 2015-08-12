
# coding: utf-8

# Widget related imports
from IPython.html import widgets
from IPython.display import display, clear_output, Javascript
from traitlets import Unicode
import json
import os
import urllib2
import IPython
from IPython.lib import kernel

# nbconvert related imports
from IPython.nbconvert import get_export_names, export_by_name
from IPython.nbconvert.writers import FilesWriter
from IPython.nbformat import read, NO_CONVERT
from IPython.nbconvert.utils.exceptions import ConversionException


#exporter_names = widgets.Dropdown(options=get_export_names(), value='html')
#export_button = widgets.Button(description="Export")
#download_link = widgets.HTML(visible=False)
connection_file_path = kernel.get_connection_file()
connection_file = os.path.basename(connection_file_path)
kernel_id = connection_file.split('-', 1)[1].split('.')[0]

def get_name():
    sessions = json.load(urllib2.urlopen('http://127.0.0.1:8888/api/sessions'))
    for sess in sessions:
        if sess['kernel']['id'] == kernel_id:
            return sess['notebook']['path']
            break


class publish():


    filename =  os.getcwd()+"/"+get_name()#notebook_name.value
    #print filename
    global file_writer
    file_writer = FilesWriter()
    def __init__(self):#,name, nb):

        #filename = notebook_name.value
        self.filename =get_name()#  os.getcwd()+"/"+get_name()
        exporter_names = widgets.Dropdown(options=get_export_names(), value='html')
        export_button = widgets.Button(description="Export")
        download_link = widgets.HTML(visible=False)
    # Get a unique key for the notebook and set it in the resources object.
        def export8(self,name, nb):
            notebook_name = name[:name.rfind('.')]
            resources = {}
            resources['unique_key'] = notebook_name
            resources['output_files_dir'] = '%s_files' % notebook_name
            try:
                output, resources = export_by_name(exporter_names.value, nb)
            except ConversionException as e:
                download_link.value = "<br>Could not export notebook!"
            else:
                write_results = file_writer.write(output, resources, notebook_name=notebook_name)
    
                download_link.value = "<br>Results: <a href='files/{filename}'><i>\"{filename}\"</i></a>".format(filename=write_results)
                download_link.visible = True
        
            #display(exporter_names, export_button, download_link)
        def handle_export(widget):
            with open(get_name(), 'r') as f:
                export8(widget,get_name(), (read(f, NO_CONVERT)))
            
        export_button.on_click(handle_export)
        display(exporter_names, export_button, download_link)


# Display the controls.

