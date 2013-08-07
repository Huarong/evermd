# encoding: utf-8
# author: Huarong Huo



def text_to_ENML(text):
    content = '<?xml version="1.0" encoding="UTF-8"?>\
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    content += '<en-note>%s</en-note>' % text
    return content