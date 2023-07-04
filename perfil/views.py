from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta
from .models import Categoria
from django .contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total
# from django.db.models import Sun

# Create your views here.

def home(request):
    contas = Conta.objects.all()
    
    total_contas = calcula_total(contas, 'valor')
    return render(request, 'home.html', {'contas' : contas, 'total_contas' : total_contas})

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    # Outra forma de fazer
    # total_contas = contas.aggregate(Sun('valor'))['valor__Sun']
    
    total_contas = calcula_total(contas, 'valor')
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias' : categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo =  request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        # Mensagem de erro
        messages.add_message(request, constants.WARNING, 'Você não preencheu todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone
    )
    
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta Cadastrada com Sucesso')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta Deletada com Sucesso')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    #TODO: Realizar validações
    isinstance(essencial, bool)
    if len(nome.strip()) == 0:
        # Mensagem de erro
        messages.add_message(request, constants.WARNING, 'Você não preencheu todos os campos')
        return redirect('/perfil/gerenciar/')
    
    
    categoria = Categoria(
        categoria = nome,
        essencial = essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('/perfil/gerenciar/')