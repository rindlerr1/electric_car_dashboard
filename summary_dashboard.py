#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:19:03 2020

@author: Home
"""

import os
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models.widgets import Div, Select, Slider
from bokeh.models import Circle
from bokeh.models.graphs import from_networkx

import networkx as nx
from gensim.summarization import summarize



"""Network Graph"""
files = os.listdir('/Users/Home/Desktop/Projects/Text_Projects/links')


dataframe = pd.DataFrame()

for file in files:
    table = pd.read_csv('/Users/Home/Desktop/Projects/Text_Projects/links/'+file)
    
    table['Core_Node'] = file.split('.')[0]
    
    dataframe = dataframe.append(table)
    

dataframe['Links'] = dataframe['Links'].apply(lambda x: x.split('/')[2])


dataframe = dataframe.drop_duplicates(subset=['Links', 'Core_Node'])

dataframe['edges'] = dataframe.apply(lambda col: (col['Links'], col['Core_Node']),1)
edges_list = [x for x in dataframe['edges']]

G=nx.Graph()

G.add_edges_from(edges_list)
  

plot = figure(title="Electric Car Network of Link Pages",
              x_range=(-2.5,2.5), y_range=(-2.5,2.5),
              plot_width=600, plot_height=600,
              tools="", toolbar_location=None)


plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None


plot.yaxis.visible = False
plot.xaxis.visible = False
plot.xgrid.visible = False




graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))


graph.node_renderer.glyph = Circle(fill_color='blue')



plot.renderers.append(graph)

"""Summary Section"""

def summarize_text(category, ratio):
    
    dir_path = "/users/home/desktop/projects/Text_Projects/corpus/"+category+'/'
    
    file_list = os.listdir(dir_path)

    
    text_files = []
    for files in file_list:
        text = open(dir_path+files, 'r')
        text_files.append(text.read())
    
    corpus = ''
    corpus = corpus.join(text_files)
    
    string_sum = summarize(corpus, ratio=ratio)
        
    return string_sum
     

cats = os.listdir("/users/home/desktop/projects/Text_Projects/corpus/")
selector = Select(title="Wikipedia Page:", value='Electric_car', options=cats)

slider = Slider(start=0.01, end=0.1, value=0.01, step=.01, title="Ratio Value")

string_sum = summarize_text(selector.value, slider.value)
text = Div(text = string_sum, width=600, height=100) 



def update_plot(attrname, old, new):
    string_sum = summarize_text(selector.value, slider.value)
    text.text = string_sum




    
slider.on_change('value', update_plot)
selector.on_change('value', update_plot)    

   
interactions = column(row(selector, slider), text)
layout =  row(plot, interactions) 
        
curdoc().add_root(layout)
curdoc().title = "Text Summary"




    