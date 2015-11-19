''' Plugin for CudaText editor
Authors:
    Andrey Kvichansky    (kvichans on githab)
Version:
    '0.1.1 2015-11-12'
'''
#! /usr/bin/env python3

import  re, json, os, webbrowser, tempfile, collections, html
import  cudatext        as app
from    cudatext    import ed
import  cudax_lib       as apx

pass;                           LOG = (-2==-2)  # Do or dont logging.

RPT_HEAD = '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>CudaText currect options</title>
    <style type="text/css">
td, th, body {
    color:          #000;
    font-family:    Verdana, Arial, Helvetica, sans-serif;
    font-size:      12px;
}
table {
    border-width:   1px;
    border-spacing: 2px;
    border-color:   gray;
    border-collapse:collapse;
}
table td, table th{
    border-width:   1px;
    padding:        1px;
    border-style:   solid;
    border-color:   gray;
}
pre {
    margin:         0;
    padding:        0;
}
td.nxt {
    color:          grey;
}
td.win {
    font-weight:    bold;
}
    </style>
</head>
<body>
'''
RPT_FOOT = '''
</body>
</html>
'''

def do_report(fn):
    lex         = ed.get_prop(app.PROP_LEXER_CARET)
    def_json    = os.path.join(apx.get_def_setting_dir()         , 'default.json')
    usr_json    = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'user.json')
    lex_json    = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'lexer {}.json'.format(lex))
    def_opts    = apx.get_app_default_opts()
#   def_opts    = apx.get_app_default_opts(         object_pairs_hook=collections.OrderedDict)
    usr_opts    = apx._get_file_opts(usr_json, {},  object_pairs_hook=collections.OrderedDict)
#   pass;                      apx.log('usr_opts=\n{}', usr_opts)
    lex_opts    = apx._get_file_opts(lex_json, {},  object_pairs_hook=collections.OrderedDict)
    fil_opts    = get_ovrd_ed_opts(ed)
    cmt_opts    = {}
    # Find Commentary for def opts in def file
    # Rely: _commentary_ is some (0+) lines between opt-line and prev opt-line
    def_body    = open(def_json).read()
    def_body    = def_body.replace('\r\n', '\n').replace('\r', '\n')
    def_body    = def_body[def_body.find('{')+1:]   # Cut head with start '{'
    def_body    = def_body.lstrip()
    pass;                      #LOG and apx.log('pr for def_body={}',def_body[:50])
    for opt in def_opts.keys():
        pos_opt = def_body.find('"{}"'.format(opt))
        pass;                  #LOG and apx.log('opt, pos_opt={}',(opt, pos_opt))
        cmt     = def_body[:pos_opt].strip()
        cmt     = re.sub('^\s*//', '', cmt, flags=re.M)
        cmt     = cmt.strip()
        pass;                  #LOG and apx.log('cmt={}',cmt)
        cmt_opts[opt]    = html.escape(cmt)
        def_body= def_body[def_body.find('\n', pos_opt)+1:]   # Cut the opt
        pass;                  #LOG and apx.log('pr for def_body={}',def_body[:50])
       #pass;                   return False

    with open(fn, 'w', encoding='utf8') as f:
        f.write(RPT_HEAD)
        f.write('<table>\n')
        f.write(	'<tr>\n')
        f.write(	'<th>Option name</th>\n')
        f.write(	'<th>Value in<br>default</th>\n')
        f.write(	'<th>Value in<br>user</th>\n')
        f.write(	'<th>Value in<br>lexer<br>{}</th>\n'.format(lex))
        f.write(	'<th title="{}">Value in<br>file<br>{}</th>\n'.format(ed.get_filename()
                                              , os.path.basename(ed.get_filename())))
        f.write(	'<th>Comment</th>\n')
        f.write(	'</tr>\n')
        for opt in fil_opts.keys():
            winner  = 'def'
            winner  = 'usr' if opt in usr_opts else winner
            winner  = 'lex' if opt in lex_opts else winner
            winner  = 'fil' if opt in fil_opts else winner
            f.write(	'<tr>\n')
            f.write(	'<td>{}</td>\n'.format(opt))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='def' else 'nxt', def_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='usr' else 'nxt', usr_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='lex' else 'nxt', lex_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='fil' else 'nxt', fil_opts.get(opt, '')))
            f.write(	'<td><pre>{}</pre></td>\n'.format(cmt_opts.get(opt, '')))
            f.write(	'</tr>\n')
            def_opts.pop(opt, None)
            usr_opts.pop(opt, None)
            lex_opts.pop(opt, None)
        f.write('</table><br/>\n')
        f.write('<table>\n')
        f.write(	'<tr>\n')
        f.write(	'<th>Option name</th>\n')
        f.write(	'<th>Value in<br>default</th>\n')
        f.write(	'<th>Value in<br>user</th>\n')
        f.write(	'<th>Value in<br>lexer<br>{}</th>\n'.format(lex))
        f.write(	'<th>Comment</th>\n')
        f.write(	'</tr>\n')
        for opt in def_opts.keys():
            winner  = 'def'
            winner  = 'usr' if opt in usr_opts else winner
            winner  = 'lex' if opt in lex_opts else winner
            winner  = 'fil' if opt in fil_opts else winner
            f.write(	'<tr>\n')
            f.write(	'<td>{}</td>\n'.format(opt))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='def' else 'nxt', def_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='usr' else 'nxt', usr_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='lex' else 'nxt', lex_opts.get(opt, '')))
            f.write(	'<td><pre>{}</pre></td>\n'.format(cmt_opts.get(opt, '')))
            f.write(	'</tr>\n')
            usr_opts.pop(opt, None)
            lex_opts.pop(opt, None)
        f.write('</table><br/>\n')
        f.write('<table>\n')
        f.write(	'<tr>\n')
        f.write(	'<th>Option name</th>\n')
        f.write(	'<th>Value in<br>user</th>\n')
        f.write(	'<th>Value in<br>lexer<br>{}</th>\n'.format(lex))
        f.write(	'<th>Comment</th>\n')
        f.write(	'</tr>\n')
        for opt in usr_opts.keys():
            winner  = 'usr'
            winner  = 'lex' if opt in lex_opts else winner
            f.write(	'<tr>\n')
            f.write(	'<td>{}</td>\n'.format(opt))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='usr' else 'nxt', usr_opts.get(opt, '')))
            f.write(	'<td class="{}">{}</td>\n'.format('win' if winner=='lex' else 'nxt', lex_opts.get(opt, '')))
            f.write(	'<td><pre>{}</pre></td>\n'.format(cmt_opts.get(opt, '')))
            f.write(	'</tr>\n')
            lex_opts.pop(opt, None)
        for opt in lex_opts.keys():
            winner  = 'lex'
            f.write(	'<tr>\n')
            f.write(	'<td>{}</td>\n'.format(opt))
            f.write(	'<td class="{}"></td>  \n'.format('non'))
            f.write(	'<td class="{}">{}</td>\n'.format('win', lex_opts.get(opt, '')))
            f.write(	'<td><pre>{}</pre></td>\n'.format(cmt_opts.get(opt, '')))
            f.write(	'</tr>\n')
            lex_opts.pop(opt, None)
        f.write('</table><br/>\n')
        f.write(RPT_FOOT)
        return True
   #def do_report(fn):

def get_ovrd_ed_opts(ed):
    ans     = collections.OrderedDict()
    ans['tab_size']             = ed.get_prop(app.PROP_TAB_SIZE)
    ans['tab_spaces']           = ed.get_prop(app.PROP_TAB_SPACES)
    ans['wrap_mode']            = ed.get_prop(app.PROP_WRAP)
    ans['unprinted_show']       = ed.get_prop(app.PROP_UNPRINTED_SHOW)
    ans['unprinted_spaces']     = ed.get_prop(app.PROP_UNPRINTED_SPACES)
    ans['unprinted_ends']       = ed.get_prop(app.PROP_UNPRINTED_ENDS)
    ans['unprinted_end_details']= ed.get_prop(app.PROP_UNPRINTED_END_DETAILS)
    return ans
   #def get_ovrd_ed_opts(ed):

class Command:
    def run(self):
       #pass;                   apx.log('??')
       #pass;                   apx.log('apx.get_def_setting_dir()={}',apx.get_def_setting_dir())
        htm_file = os.path.join(tempfile.gettempdir(), 'CudaText_overided_options.html')
        if do_report(htm_file):
            webbrowser.open_new_tab('file://'+htm_file)
            app.msg_status('Opened browser with file '+htm_file)
       #pass;                   apx.log('ok')

