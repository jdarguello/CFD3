import ipywidgets as widgets

def Read(raw):
    datos = {
        'Geometría':{},
        'Propiedades':{}
    }
    cont = 0
    for tipo in datos:
        suma = 0
        while True:
            try:
                if tipo != 'Malla':
                    datos[tipo][raw.children[cont].get_title(suma)] = raw.children[cont].children[suma].value
                else:
                    datos[tipo] = raw.children[cont].value
                    break
                suma += 1
            except:
                break
        cont += 1
    return datos

def Requerimientos():
    Req = widgets.Accordion(children=[widgets.FloatText(value=2, disabled=False),
                                      widgets.FloatText(value=1)])
    Req.set_title(0, 'W')
    Req.set_title(1, 'H')
    return Req

def Esp():
    Req = widgets.Accordion(children=[widgets.FloatText(value=0),
                                      widgets.FloatText(value=0),
                                      widgets.FloatText(value=55),
                                      widgets.FloatText(value=10),
                                      widgets.FloatText(value=0),
                                      widgets.FloatText(value=5)])
    Req.set_title(0, 'T_0')
    Req.set_title(1, 'T_{infty}')
    Req.set_title(2, 'K')
    Req.set_title(3, 'h')
    Req.set_title(4, 'Q_g')
    Req.set_title(5, 'Dt')
    return Req

def Datos():
    Req = Requerimientos()
    E = Esp()
    tab = widgets.Tab()
    tab.children = [Req, E]
    tab.set_title(0, 'Geometría')
    tab.set_title(1, 'Propiedades')
    return tab
