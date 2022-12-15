from flask import Flask, render_template, render_template_string, request
import random

app = Flask(__name__)


negative_msg = ["Well i don't think that's helpful..","Could be better i guess","I believe in you.. to provide better one liners next time! :')","Comon that's just basic.."]

positive_msg = ["Oh W0o0w thats actually sick !! Thank you", "Damn you must be a python guru,never knew about this THX!!","You have been googling a bunch for this didn't you? Thanks !","God damn..well that's just so efficiant..Thank you"]

# don't send me dangerous python one liners tho !!!

blacklist = [ 'class', 'mro', 'init', 'builtins', 'request', 'app','sleep', 'add', '+', 'config', 'subclasses', 'format', 'dict', 'getattr','attr', 'globals', 'time', 'read', 'import', 'sys', 'cookies', 'headers', 'doc', 'url', 'encode', 'decode', 'chr', 'ord', 'replace', 'echo', 'base', 'self', 'flag', 'template', 'exec', 'response', 'join', 'cat', 'list','last', 'session', 'update', '_', '&','{{','}}','[', ']' ,'~']

@app.route('/',methods=['GET'])
def __main__():
    return render_template('index.html',score='',message='')

@app.route('/send',methods=['POST'])
def send():
    code = request.form.get('input_code')
    score = 100*len(code)/500
    if score > 5:
        for x in blacklist: 
            if x in code:
                return  render_template('index.html',score='',message='Shame of you to try and hack me..',code='HACKERRR ATTEMPT!!')
        return render_template('index.html',score=score,message=random.choice(positive_msg),code='Your submittion : '+render_template_string(code))
    else:
        return render_template('index.html',score=score,message=random.choice(negative_msg),code='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)