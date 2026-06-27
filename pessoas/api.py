from ninja import NinjaAPI
from .models import Pessoa
from .schemas import PessoaIn, PessoaOut, ErrorSchema
from typing import List

api = NinjaAPI(
    title="API RESTful Pessoas",
    description="API para gestão de pessoas com operações completas sobre os dados.",
    version="1.0.0",
    urls_namespace='pessoas'
)


###########################################################
# listar - corrigir !!!!
###########################################################
@api.get("pessoas/",
         response={200: List[PessoaOut]},
         description="Lista todas as pessoas",
         tags=["Pessoas"])
def listar_pessoas(request,
                   sort: str = None,
                   idade: int = None,
                   nome: str = None,
                   offset: int = 0,
                   limit: int = 3):
    pessoas = Pessoa.objects.all()

    if idade:
        pessoas = pessoas.filter(idade=idade)
    if nome:
        pessoas = pessoas.filter(nome=nome)
    if sort:
        pessoas = pessoas.order_by(sort)

    pessoas = pessoas[offset:offset + limit]
    return 200, pessoas



###########################################################
# ver um - corrigir !!!!
###########################################################
@api.get("pessoas/{pessoa_id}/", 
         response={200: PessoaOut, 404: ErrorSchema}, 
         description="Ver dados de uma pessoa",
         tags=["Pessoas"]
         )
def ver_uma_pessoa(request, pessoa_id:int):
    try:
        return 200, Pessoa.objects.get(id=pessoa_id)
    except Pessoa.DoesNotExist:
        return 404, {"detail": "Pessoa não encontrada"}


###########################################################
# criar - não mexer, estao corretos
###########################################################
@api.post("pessoas/", 
          response={201: PessoaOut}, 
          tags=["Pessoas"],
          description="Criar uma nova pessoa")
def criar_uma_pessoa(request, data: PessoaIn):
    return 201, Pessoa.objects.create(**data.dict())


###########################################################
# atualizar - não mexer, estao corretos
###########################################################
@api.put("pessoas/{pessoa_id}/", 
         response={200: PessoaOut, 404: ErrorSchema}, 
         tags=["Pessoas"],
         description="Substituir os dados duma pessoa")
def atualizar_uma_pessoa(request, pessoa_id: int, data: PessoaIn):
    try:
        pessoa = Pessoa.objects.get(id=pessoa_id)
        for attr, value in data.dict().items():
            setattr(pessoa, attr, value)
        pessoa.save()
        return 200, pessoa
    except Pessoa.DoesNotExist:
        return 404, {"detail": "Pessoa não encontrada"}


###########################################################
# apagar - implementar !!!!
###########################################################
@api.delete("pessoas/{pessoa_id}/", 
            response={204: None, 404: ErrorSchema}, 
            description="Apagar uma pessoa",
            tags=["Pessoas"])
def apagar_uma_pessoa(request, pessoa_id: int):
    try:
        pessoa = Pessoa.objects.get(id=pessoa_id)
        pessoa.delete()
        return 204, {"detail": "Pessoa apagada com sucesso"}
    except Pessoa.DoesNotExist:
        return 404, {"detail": "Pessoa não encontrada"}


