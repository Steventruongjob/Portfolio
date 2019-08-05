from flask import Flask, render_template, request, redirect
from app import app
import splat
import splat.utilities as splut
import splat.model
from splat.initialize import *
from splat.utilities import *
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.tools import BoxZoomTool, HoverTool, PanTool, ResizeTool, SaveTool, ResetTool, WheelZoomTool
from bokeh.models.widgets import Panel, Tabs, DataTable, DateFormatter, TableColumn
from bokeh.resources import INLINE
from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.layouts import layout
import numpy as np

#Plotting Function
def Plot(n):
	p = figure(plot_width=1200,plot_height=500,toolbar_location='above',tools="pan,wheel_zoom,box_zoom,reset,hover,save")
	p.line(np.array(n.wave),np.array(n.flux),line_width=2,color='blue',legend='Flux')
	p.line(np.array(n.wave),np.array(n.noise),line_width=1,color='black',legend='Uncertainty')
	if request.form.get('compare'):
		standard_flux = splat.core.getStandard(splat.classifyByStandard(n)[0]).flux * n.fluxMax().value
		p.line(np.array(n.wave),np.array(standard_flux),line_width=1,color='red',legend='Spectral Standard')
	p.xaxis.axis_label = 'Wavelength (Microns)'
	p.yaxis.axis_label = 'Flux (erg/cm^2 micron s)'
	ymax = n.fluxMax().value
	p.y_range = Range1d(0,ymax)
	return p

#Table Function

def Table(n):
	data = dict(
		name=[n.name],
		source_key=[n.source_key],
		designation=[n.designation],
		RA=[n.ra],
		dec=[n.dec],
		discovery_reference=[n.discovery_reference],
		opt_type=[n.opt_type],
		opt_type_ref=[n.opt_type_ref],
		nir_type=[n.nir_type],
		nir_type_ref=[n.nir_type_ref],
		reduction_spextool_version=[n.reduction_spextool_version],
		reduction_person=[n.reduction_person],
		reduction_date=[n.reduction_date],
		quality_flag=[n.quality_flag],
		median_snr=[n.median_snr],
		spex_type=[n.spex_type],
		spex_gravity_classification=[n.spex_gravity_classification],
		published=[n.published],
		data_reference=[n.data_reference],
		note_sp=[n.note_sp],

		

)
	

	source = ColumnDataSource(data)
	columns = [TableColumn(field='name',title='NAME'),
		TableColumn(field='source_key',title='SOURCE_KEY'),
		TableColumn(field='designation',title='DESIGNATION'),
		TableColumn(field='RA',title='RA'),
		TableColumn(field='dec',title='DEC'),
		TableColumn(field='discovery_reference',title='Discovery_reference'),
		TableColumn(field='opt_type',title='Opt_type'),
		TableColumn(field='opt_type_ref',title='opt_type_ref'),
		TableColumn(field='nir_type',title='nir_type'),
		TableColumn(field='nir_type_ref',title='nir_type_ref'),
		TableColumn(field='reduction_spextool_version',title='Reduction_spextool_version'),
		TableColumn(field='reduction_person',title='Reduction_person'),
		TableColumn(field='reduction_date',title='Reduction_date'),
		TableColumn(field='quality_flag',title='Quality_flag'),
		TableColumn(field='median_snr',title='Median_snr'),
		TableColumn(field='spex_type',title='Spex_type'),
		TableColumn(field='spex_gravity_classification',title='Spex_gravity_classification'),
		TableColumn(field='published',title='Published'),
		TableColumn(field='data_reference',title='Data_reference'),
		TableColumn(field='note_sp',title='Note_sp'),

		]
	Table = DataTable(source=source,columns=columns,width=1200,height=50)
	return Table

def Standard(n):
	a = splat.classifyByStandard(n)
	data = dict()
	columns = list()
	if request.form.get('standard'):
		data.update(spt=[a])
		source = ColumnDataSource(data)
		column_standard = [
			TableColumn(field='spt',title='Spectral Type'),]
		Analysis1 = DataTable(source=source,columns=column_standard,width=1200,height=50)
		return Analysis1

def Index(n):
	b = splat.measureIndexSet(n)
	data = dict()
	if request.form.get('index'):
		data.update(		
		ch4h=[b['CH4-H']],
		ch4j=[b['CH4-J']],
		ch4k=[b['CH4-K']],
		h2oh=[b['H2O-H']],
		h2oj=[b['H2O-J']],
		h2ok=[b['H2O-K']],
		kj=[b['K-J'][0]],)
		source = ColumnDataSource(data)
		column_index = 	[
			TableColumn(field='ch4h',title='CH4-H'),
			TableColumn(field='ch4j',title='CH4-J'),
			TableColumn(field='ch4k',title='CH4-K'),
			TableColumn(field='h2oh',title='H2O-H'),
			TableColumn(field='h2oj',title='H2O-J'),
			TableColumn(field='h2ok',title='H2O-K'),
			TableColumn(field='kj',title='KJ'),]
		Analysis2 = DataTable(source=source,columns=column_index,width=1200,height=50)
		return Analysis2

def Model(n):
	c = splat.model.modelFitGrid(n)
	data = dict()
	if request.form.get('model'):
		data.update(
		cld=[c[0]['cld']],
		fsed=[c[0]['fsed']],
		kzz=[c[0]['kzz']],
		logg=[c[0]['logg']],
		radius=[c[0]['radius']],
		scale=[c[0]['scale']],
		set=[c[0]['set']],
		stat=[c[0]['stat']],
		teff=[c[0]['teff']],
		z=[c[0]['z']],)
		source = ColumnDataSource(data)
		column_model = [
			TableColumn(field='cld',title='CLD'),
			TableColumn(field='fsed',title='FSED'),
			TableColumn(field='kzz',title='KZZ'),
			TableColumn(field='logg',title='LogG'),
			TableColumn(field='radius',title='Radius'),
			TableColumn(field='scale',title='Scale'),
			TableColumn(field='set',title='SET'),
			TableColumn(field='stat',title='STAT'),
			TableColumn(field='teff',title='Temperature'),
			TableColumn(field='z',title='Z'),]
		Analysis3 = DataTable(source=source,columns=column_model,width=1200,height=50)
	source = ColumnDataSource(data)
	return Analysis3

def Simple(n):
	P = Plot(n)
	T = Table(n)
	if request.form.get('standard'):
		if request.form.get('standard') and request.form.get('index'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
			else: 
				A,B = Standard(n),Index(n)
				return layout([[P],[T],[A],[B]])
		elif request.form.get('standard') and request.form.get('model'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
			else:
				A,C = Standard(n),Model(n)
				return layout([[P],[T],[A],[C]])
		else:
			A = Standard(n)
			return layout([[P],[T],[A]])
	elif request.form.get('index'):
		if request.form.get('standard') and request.form.get('index'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
			else:
				A,B = Standard(n),Index(n)
				return layout([[P],[T],[A],[B]])
		elif request.form.get('index') and request.form.get('model'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
			else:
				B,C = Index(n),Model(n)
				return layout([[P],[T],[B],[C]])
		else: 
			B = Index(n)
			return layout([[P],[T],[A]])
	elif request.form.get('model'):
		if request.form.get('standard') and request.form.get('model'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
		elif request.form.get('index') and request.form.get('model'):
			if request.form.get('standard') and request.form.get('index') and request.form.get('model'):
				A,B,C = Standard(n),Index(n),Model(n)
				return layout([[P],[T],[A],[B],[C]])
			else:
				B,C = Index(n),Model(n)
				return layout([[P],[T],[B],[C]])
		else:
			C = Model(n)
			return layout([[P],[T],[A]])

	else: return layout([[P],[T]])


#Routes
@app.route('/')
@app.route('/SpectrumQuery.html')
@app.route('/SpectrumResults.html')
def app_home():
    return redirect('/query')

#Query Page
@app.route('/query', methods=['GET', 'POST'])
def app_query():
    return render_template('SpectrumQuery.html')

#Receiving data
@app.route('/results', methods=['GET', 'POST'])
def app_results():
	mkwargs = {}
	for key in list(request.form.keys()):
		if request.form['shortname'] != '':
			mkwargs['shortname'] = request.form['shortname']
		if request.form['name'] != '':
			mkwargs['name'] = request.form['name']
		if request.form['coordinate'] != '':
			mkwargs['coordinate'] = splut.properCoordinates(request.form['coordinate'])
		if request.form['spt'] != '':
			mkwargs['spt'] = request.form['spt']
		if request.form.get('young'):
			mkwargs['young'] = True
		if request.form.get('subdwarf'):
			mkwargs['subdwarf'] = True
		if request.form.get('wd'):
			mkwargs['wd'] = True
		if request.form.get('giant'):
			mkwargs['giant'] = True
		if request.form.get('binary'):
			mkwargs['binary'] = True
		if request.form.get('sbinary'):
			mkwargs['sbinary'] = True
		if request.form.get('lucky'):
			mkwargs['lucky'] = True

#Plotting data
		splist = splat.getSpectrum(**mkwargs)
		n = len(splist)
		number = {'count':n}
		splist = splat.getSpectrum(**mkwargs)[0:20]

#Error Template
		if n == 0:
			return render_template('zeroerror.html')

#Tabs doesn't support for loops for some reason, so I got desperate
		tabs = []
		for i in range(n):
		 	sp = splist[i]			
		 	l = Simple(sp)
		 	tabs.append(Panel(child=l,title=sp.name))
		tabs = Tabs(tabs=tabs)
		div = file_html(tabs,INLINE)

		return render_template('SpectrumResults.html',div=div,number=number)