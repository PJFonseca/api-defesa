from ninja import Schema

class PessoaIn(Schema):
    nome: str 

class PessoaOut(PessoaIn):
    id: int
    
class ErrorSchema(Schema):
    detail: str
