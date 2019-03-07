from bottle import route,response,request,template,auth_basic
import copy
import json
from pathlib import Path
from slugify import slugify
from cssmin import cssmin
from jsmin import jsmin
import functools

#CMS CONFIGURATION
pageList=[]

def addPageToCms(page):
	global pageList
	pageList.append(page)

def reGenerateAllPage():
	global pageList
	for page in pageList:
		page.generatePage()

editable={}
#CMS ROUTES

#authentication
def checkUser(u,p):
	authConfig=json.loads(Path('./app/editor/config.json').read_text())
	
	if u!=authConfig['user'] or p!=authConfig['password']:
		return False
	else:
		return True

#serve admin panel
@auth_basic(checkUser)
def cmsRoute():
	global editable
	
	#contents
	contentUnits=[]
	for description,fName in editable.items():
		contentUnits.append({
			'fName':fName,
			'name':slugify(fName),
			'description':description
		})
	
	Path('./app/editor/contentUnits.js').write_text('Admin.contentUnitData='+json.dumps(contentUnits)+';')
	
	#js for editor
	js=''
	scriptList=['contentUnits.js','textEditor.js','main.js']
	for scriptFname in scriptList:
		js+='<script>'+Path('./app/editor/'+scriptFname).read_text()+'</script>'
	
	#css for editor
	css=''
	cssList=['Panagram.css']
	for cssFname in cssList:
		css+='<style>'+Path('./app/editor/'+cssFname).read_text()+'</style>'
	
	return template(Path('./app/editor/editor.html').read_text(),{
		'js':js,
		'css':css
	})
"""
request data format:
fName:(path to content file, ROOT IS APP/CONTENT/)
newContent
"""
@auth_basic(checkUser)
def cmsUpdate():
	updateData = request.json
	contentFile=Path('app/content/'+updateData['fName'])
	newContent=updateData['newContent']
	if contentFile.is_file():
		contentFile.write_text(newContent)
		response.status=200
	else:
		response.status=404
#SWITCH FOR CMS
def enable():
	route('/admin',['get'],cmsRoute)
	route('/update',['post'],cmsUpdate)