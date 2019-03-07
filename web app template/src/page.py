from pathlib import Path
from bottle import route,SimpleTemplate,static_file
#minify
from cssmin import cssmin
from jsmin import jsmin
from htmlmin import minify as htmlmin

from src.cms import addPageToCms
"""
url:route path/url and also the filename('_' instead of '/')
template
contentFiles:path to content files(ROOT:app/content)
cssList(fileName list(only filename from app/css))
jsList(fileName list)
"""
class Page:
	def prepareCss(self):
		css=''
		for fName in self.cssList:
			css+=cssmin(Path('./app/css/'+fName).read_text())
		self.css='<style>'+css+'</style>'

	def prepareJs(self):
		js=''
		for fName in self.jsList:
			js+='<script>'+jsmin(Path('./app/js/'+fName).read_text())+'</script>'
		self.js=js
	
	def prepareContent(self):
		res={}
		for key, value in self.contentFiles.items():
			res[key]=Path('./app/content/'+value).read_text()
		self.contentFilesData=res
	
	def generatePage(self):
		#prepare js,css(result in self.js/css)
		self.prepareCss()
		self.prepareJs()
		#prepare content for page
		templateDict={
			'css':self.css,
			'js':self.js
		}
		#templateDict.update(self.content)
		self.prepareContent()
		templateDict.update(self.contentFilesData)
		#prepare template
		documentTmp=SimpleTemplate(Path('./app/template/'+self.template).read_text())
		self.document=documentTmp.render(templateDict)
		self.pageToFile()
	def pageToFile(self):
		#write document to file
		f=Path('./page/'+self.fileName).open(mode='w',buffering=-1, encoding='utf-8')
		f.write(self.document)
		f.close()
		
	def __init__(self,opt):
		#set up instance data
		#URL,FILE NAME
		if opt['url'] and isinstance(opt['url'],str):
			self.url=opt['url']
			self.fileName=opt['url'].replace('/','_')+'.html'
		else:
			ValueError('url is obligatory, type must be string!')
		#CSS
		if opt['cssList'] and isinstance(opt['cssList'],list):
			self.cssList=opt['cssList']
		else:
			self.cssList=[]
		#JS
		if opt['jsList'] and isinstance(opt['jsList'],list):
			self.jsList=opt['jsList']
		else:
			self.jsList=[]
		#CONTENTFILES
		if opt['contentFiles'] and isinstance(opt['contentFiles'],dict):
			self.contentFiles=opt['contentFiles']
		else:
			self.contentFiles={}
			self.contentFilesData={}
		#TEMPLATE
		if opt['template'] and isinstance(opt['template'],str):
			self.template=opt['template']
		else:
			raise ValueError('template is obligatory, type must be string!')
		#CMS
		addPageToCms(self)
		#generate file(to /page folder)
		self.generatePage()
		
		#set up route to page
		def routeHandler():
			return static_file(self.fileName, root='./page/')
			
		route(self.url,'GET',routeHandler)