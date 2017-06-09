from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json, requests
from .models import Post, Comment
from django.http import JsonResponse, HttpResponse



cepInfo = """
    CEP é a sigla de Código de Endereçamento Postal, criado e utilizado pelos Correios para facilitar o encaminhamento e a entrega das correspondências aos destinatários. O CEP é uma informação indispensável na correspondência, pois identifica todos os detalhes do endereço. No Brasil o número do CEP é formado por oito algarismos, que identificam o endereço do destinatário da correspondência, facilitando a sua entrega. O CEP pode estar relacionado a uma região, um bairro específico, ou até mesmo o prédio do destinatário da correspondência. Para facilitar a criação dos CEPs a Empresa Brasileira de Correios e Telégrafos dividiu o Brasil em 10 regiões postais. O Código de Endereçamento Postal ajuda na triagem, no encaminhamento e na distribuição de todas as correpondências ou encomendas. Cada número do código identifica todos os detalhes do endereço.
"""

cpfInfo = """
    CPF é o cadastro da Receita Federal brasileira no qual devem estar todos os contribuintes (pessoas físicas brasileiras ou estrangeiras com negócios no Brasil).
     O CPF armazena informações fornecidas pelo próprio contribuinte e por outros sistemas da Receita Federal.
"""

coordInfo = """
São linhas imaginárias pelas quais a Terra foi “cortada”, essas linhas são os paralelos e meridianos, através dos paralelos e meridianos é possível estabelecer localizações precisas em qualquer ponto do planeta.
"""
latInfo = """
• Latitude: É a distância medida em graus de um determinado ponto do planeta entre o arco do meridiano e a linha do equador.
"""

lonInfo = """
• Longitude: É a localização de um ponto da superfície medida em graus, nos paralelos e no meridiano de Greenwich.
"""
recent_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]

def cep(request):
    if request.method == "POST":
        cepNumber = request.POST['cepNumber']
        if validateCEP(cepNumber) == True:
            url = 'http://viacep.com.br/ws/' + cepNumber + '/json/'
            result = requests.get(url)
            cepJson = result.json()
            return render(request, 'application/cep.html', {
                'r': cepJson,
                'cepInfo': cepInfo,
                'page_title': 'CEP', 'recent_posts': recent_post})
        else:
            return render(request, 'application/cep.html', {
                'r': '*Insira um CEP válido!',
                'cepInfo': cepInfo + " 1",
                'page_title': 'CEP'})
    else:
        return render(request, 'application/cep.html', {
            'cepInfo': cepInfo,
             'page_title': 'CEP'})


def cpf(request):

    key = 'e6cc0c8ac7fddca7d4a7bb45bcb2a813'
    if request.method == "POST":
        cpfNumber = request.POST['cpfNumber']
        if validateCPF(cpfNumber) == True:
            url = "https://api.cpfcnpj.com.br/" + key + "/1/json/" + cpfNumber
            result = requests.get(url)
            cpfJson = result.json()
            return render(request, 'application/cpf.html', {
                'r': cpfJson,
                'cpfInfo': cpfInfo,
                'page_title': 'CPF'})
        else:
            return render(request, 'application/cpf.html', {
                'r': '*Insira um CPF válido!',
                'cpfInfo': cpfInfo,
                'page_title': 'CPF'})
    else:
        return render(request, 'application/cpf.html', {'cpfInfo': cpfInfo, 'page_title': 'CPF'})


# ------------ Validate --------------
def validateCEP(cepNumber):
    cepNumber_invalidos = [8*str(i) for i in range(7)]
    if cepNumber in cepNumber_invalidos:
        return False
    if len( cepNumber ) < 8:
        """ Verifica se o cpfNumber tem 11 digitos """
        return False

    if len( cepNumber ) > 8:
        """ cpfNumber tem que ter 11 digitos """
        return False
    return True


def validateCPF(cpfNumber):
        """
        Method to validate a brazilian cpfNumber number
        Based on Pedro Werneck source avaiable at
        www.PythonBrasil.com.br

        Tests:
        >>> print cpfNumber().validate('91289037736')
        True
        >>> print cpfNumber().validate('91289037731')
        False
        """
        cpfNumber_invalidos = [11*str(i) for i in range(10)]
        if cpfNumber in cpfNumber_invalidos:
            return False

        if not cpfNumber.isdigit():
            """ Verifica se o cpfNumber contem pontos e hifens """
            cpfNumber = cpfNumber.replace( ".", "" )
            cpfNumber = cpfNumber.replace( "-", "" )

        if len( cpfNumber ) < 11:
            """ Verifica se o cpfNumber tem 11 digitos """
            return False
        if len( cpfNumber ) > 11:
            """ cpfNumber tem que ter 11 digitos """
            return False
        selfcpfNumber = [int( x ) for x in cpfNumber]
        cpfNumber = selfcpfNumber[:9]
        while len( cpfNumber ) < 11:
            r =  sum( [( len( cpfNumber )+1-i )*v for i, v in [( x, cpfNumber[x] ) for x in range( len( cpfNumber ) )]] ) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            cpfNumber.append( f )


        return bool( cpfNumber == selfcpfNumber )


def coordinate(request):
    if request.method == "POST":
        lat = [request.POST['lat_deg'],request.POST['lat_min'], request.POST['lat_sec']]
        lon = [request.POST['lon_deg'],request.POST['lon_min'], request.POST['lon_sec']]
        #if validateCPF(cpfNumber) == True:
        try:
            coord = calc_coord(lat, lon)
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+ repr(coord[0]) +','+ repr(coord[1]) +'&key=AIzaSyA_3wK_DfiwW94-1dg352-I8Zs__FGYrDo'
            result = requests.get(url)
            geoJson = result.json()
            return render(request, 'application/coordinate.html', {
                'lat': coord[0],
                'lon': coord[1],
                'geoInfo': geoJson['results'][0]['formatted_address'],
                'page_title': 'Geo',
                'coordInfo': coordInfo,
                'latInfo': latInfo,
                'lonInfo': lonInfo})
        except:
            return render(request, 'application/coordinate.html', {
                'r': '* Insira coordenadas válidas! Utilize apenas números e pontos.',
                'page_title': 'Geo',
                'coordInfo': coordInfo,
                'latInfo': latInfo,
                'lonInfo': lonInfo})

    return render(request, 'application/coordinate.html', {
        'page_title': 'Geo',
        'coordInfo': coordInfo,
        'latInfo': latInfo,
        'lonInfo': lonInfo})


def calc_coord(lat, lon):
    opt = 'opt1'
    #lat = float(laDeg)
    #min = float(laMin)
    #sec = float(laSec)
    lat_d = (((float(lat[2])/60) + float(lat[1]))/60)
    lon_d = (((float(lon[2])/60) + float(lon[1]))/60)
    if opt == 'opt1':
        lat_dec = -(float(lat[0]) + lat_d)
        lon_dec = -(float(lon[0]) + lon_d)
    elif opt == 'opt2':
        lat_dec = (float(lat[0]) + lat_d)
        lon_dec = (float(lon[0]) + on_d)
    return lat_dec , lon_dec


def validaCoord(lat, lon):


    return True
