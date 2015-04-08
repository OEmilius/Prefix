# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    import os
    import csv

    def min_order(num): return 1 if num%10 else 10*min_order(num//10)
    
    def prefixes(low, high):
        def forward(num, order):
            nxt = num + order
            if nxt == high + 1: return [num//order]
            if nxt > high + 1: return backward(num, order//10)
            if not num%(order*10): return forward(num, order*10)
            return [num//order] + forward(nxt, order)
    
        def backward(num, order):
            nxt = num + order
            if nxt == high + 1: return [num//order]
            if nxt > high + 1: return backward(num, order//10)
            return [num//order] + backward(nxt, order)
            
        return forward(low, min_order(low))
    
    def to_cp1251(s):
        return s.decode('utf-8').encode('cp1251')
    
    def find_prefix(codes):
        pfx = []
        for cnacld in codes:
            my_list = prefixes(int(cnacld[0]), int(cnacld[1]))
            pfx.extend(map(str,my_list))
        return pfx
    
    def CLDGRP(prefix_list,GRP,name):
        add_cldgrp = []
        for p in prefix_list:
            add_cldgrp.append("ADD CLDGRP: CLD=K'8" + str(p) + ', GRPT=OG, GRP=' + GRP + ', NAME="' + name+'";')
        return add_cldgrp
    
    def CNACLD(prefix_list, route_sel_code, desc):
        add_cnacld = []
        for p in prefix_list:
            add_cnacld.append("ADD CNACLD: PFX=K'8"+str(p)+', CSTP=BASE, CSA=NTT, RSC=' +route_sel_code+' , MINL=11, MAXL=11, CHSC=0, SDESCRIPTION="' +desc+'", EA=NO;')
        return add_cnacld
    
    def combine(ranges):
    #attension tis def modified incoming paramiters
        i = 0
        new = []
        found = True
        while found == True:
            if i < len(ranges)-1:
                if (int(ranges[i][1]) + 1) == int(ranges[i+1][0]):
                    r = [ranges[i][0],ranges[i+1][1]]
                    ranges[i] = r
                    a = ranges.pop(i+1)
                else:
                    i += 1
            else:
                found = False
        return ranges  
    
    
    
    r = 'Моск'
    html = 'Данные из файла app../static/Kody_DEF-9kh.csv. Префиксы учетом объединения диапазонов<br>'
    region = r.decode('utf-8').encode('cp1251')
    
    oper = ['Мобильные ТелеСистемы', 'МегаФон', 'Московская сотовая связь','Вымпел-Коммуникации']
    operators = map(to_cp1251, oper)
    region = r.decode('utf-8').encode('cp1251')
    mts = []
    megafon = []
    mss  =[]
    beeline = []
    filename = os.path.join(request.folder, 'static', 'Kody_DEF-9kh.csv')
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        for row in reader:
            if row[5].find(region) >= 0:
                if row[4].find(operators[0]) >=0:
                    mts.append([row[0] + row[1].rjust(7,'0'),row[0] + row[2].rjust(7,'0')])
                elif row[4].find(operators[1]) >= 0:
                    megafon.append([row[0] + row[1].rjust(7,'0'),row[0] + row[2].rjust(7,'0')])
                elif row[4].find(operators[2]) >= 0:
                    mss.append([row[0] + row[1].rjust(7,'0'),row[0] + row[2].rjust(7,'0')])
                elif row[4].find(operators[3]) >= 0:
                    beeline.append([row[0] + row[1].rjust(7,'0'),row[0] + row[2].rjust(7,'0')])
    
    combine(mts)
    combine(megafon)
    combine(mss)
    combine(beeline)
    
    mts_pfx = find_prefix(mts)
    megafon_pfx = find_prefix(megafon)
    mss_pfx = find_prefix(mss)
    beeline_pfx = find_prefix(beeline)
    

    #return dict(message="hello from prefix.py")
    html += '<h3>MTS</h3>' 
    html += str(mts_pfx)
    html += '<br>pfx count' + str(len(mts_pfx))
    html += '<h3>Megafon</h3>' 
    html += 'len Megafon after combine' + str(len(megafon)) + '<br>'
    html += str(megafon_pfx)
    html += '<br>pfx count' + str(len(megafon_pfx))
    html += '<h3>MSS</h3>' 
    html += str(mss_pfx)
    html += '<h3>Beeline</h3>' 
    html += str(beeline_pfx)
    
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CNACLD(mts_pfx, '252', 'MTC_msk'))
    html += '</textarea>'
    
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CLDGRP(mts_pfx, '26', 'MTC_msk'))
    html += '</textarea>'
################################   megafon 
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CNACLD(megafon_pfx, '251', 'Mega_msk'))
    html += '</textarea>'
    
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CLDGRP(megafon_pfx, '25', 'Mega_msk'))
    html += '</textarea>'
################################  MCC
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CNACLD(mss_pfx, '253', 'MSS_msk'))
    html += '</textarea>'
    
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CLDGRP(mss_pfx, '27', 'MSS_msk'))
    html += '</textarea>'
############################### beeline
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CNACLD(beeline_pfx, '250', 'Bi_msk'))
    html += '</textarea>'
    
    html += '<hr>'
    html += '<textarea cols=120 rows=10>'
    html += '\r\n'.join(CLDGRP(beeline_pfx, '24', 'Bi_msk'))
    html += '</textarea>'
    return html


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
