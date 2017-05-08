from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json, requests
from django.http import JsonResponse, HttpResponse



def cep(request):
    key = 'e6cc0c8ac7fddca7d4a7bb45bcb2a813'
    url = 'http://viacep.com.br/ws/87020230/json/'
    r = requests.get(url)
    cepJson = r.json()
    return render(request, 'application/cpfNumber.html', {'r': cepJson})



def cpf(request):

    key = 'e6cc0c8ac7fddca7d4a7bb45bcb2a813'
    if request.method == "POST":
        cpfNumber = request.POST['cpfNumber']
        if validateCPF(cpfNumber) == True:
            url = "https://api.cpfcnpj.com.br/" + key + "/1/json/" + cpfNumber
            r = requests.get(url)
            cpfJson = r.json()
            return render(request, 'application/cpf.html', {'r': cpfJson})
        else:
            return render(request, 'application/cpf.html', {'r': '*Insira um CPF válido!'})
    else:
        return render(request, 'application/cpf.html', {})


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
