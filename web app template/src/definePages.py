from src.page import Page
import src.cms as cms

#editable contentfiles to cms
cms.editable={
	"Name of content":"body.txt"
}
cms.enable()
#clear page folder befor rerender

mypage=Page(opt={
	'url':'/asd',
	"template":"document.html",
	"contentFiles":{
		"body":'body.txt'
	},
	"cssList":['myStyle.css','myStyle2.css'],
	"jsList":['first.js','second.js']
})
