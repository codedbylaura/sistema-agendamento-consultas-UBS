class Paciente:
    """
    Representa um paciente do sistema.
    """

    def __init__(
        self,
        id=None,
        nome=None,
        cpf=None,
        data_nascimento=None,
        sexo=None,
        telefone=None,
        email=None,
        cartao_sus=None,
        endereco_id=None,
        ativo=True,
        criado_em=None,
        atualizado_em=None
    ):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.telefone = telefone
        self.email = email
        self.cartao_sus = cartao_sus
        self.endereco_id = endereco_id
        self.ativo = ativo
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

        
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
            "sexo": self.sexo,
            "telefone": self.telefone,
            "email": self.email,
            "cartao_sus": self.cartao_sus,
            "endereco_id": self.endereco_id,
            "ativo": self.ativo,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em
        }