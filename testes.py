from src.infra.connect import ViaCep
from src.domain.validacoes import ValidarDocumento

teste = ViaCep('32341310')
teste = teste.executar_conexao()
print(teste)

teste = ValidarDocumento('090.051.826/.01000')
teste = teste.executar_validacao()
print(teste)