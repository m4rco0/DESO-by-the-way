from mangaba_agent import MangabaAgent
from src.database.sql_con import AnaDatabase
import os
class AgenteLampiao:
    def __init__(self):
        self.lampiao = MangabaAgent(
            api_key= os.getenv('GOOGLE_API_KEY'),
            agent_id='lampiao'
        )
        self.regras_durh = {
            100 : "normal sem erros",
            101 : "Condição normal de monitoramento, mas não houve uso da água no dia. Pode ser transmitido um único dado do dia, com o horário 23:45:00, informando vazão e duração igual a zero e volume conforme acumulado até a última leitura em que houve uso da água",
            102 : "Transmissão normal de leituras medidas (atual ou retroativa), com exceção da duração/horímetro (quebrado ou em manutenção)",
            103 : "Transmissão normal de leituras medidas (atual ou retroativa) apenas de duração/horímetro (medidor de vazão/volume quebrado ou em manutenção)",
            104 : "Transmissão de leituras estimadas. Equipamento de medição, de transmissão ou de registro inoperante, mas foi possível estimar o uso da água por métodos alternativos (ex.: horímetro, medidor reserva redundante, medição em outra etapa do processo etc.)",
            201 : "Falha no sistema/equipamentos de transmissão (transmissor etc.), de comunicação (sinal de internet, telefonia, rádio etc.) e/ou de alimentação (eletricidade/baterias/controladores). Potencialmente há dados armazenados para transmissão retroativa - envio 1x ao dia",
            202 : "Defeito ou manutenção preventiva de sistema/equipamento de monitoramento (medidor de vazão/volume ou outro componente) que impossibilite o registro local das medições para posterior transmissão retroativa); ou nos casos em que houve transmissão de dado errado de vazão/volume que não pode ser corrigido devido à natureza/defeito - envio 1x ao dia",
            203 : "Furto ou vandalismo de sistema/equipamento de monitoramento (medidor de vazão/volume ou outro componente que impossibilite o registro local das medições para posterior transmissão retroativa) - envio 1x ao dia",
            204 : "Falha no monitoramento ainda desconhecida. Código de envio imediato (ciência do problema) quando ainda não se conhece a causa da falha. Algum dos códigos mais específicos deve ser enviado para detalhar o problema. Evitar uso indiscriminado - envio 1x ao dia",
            205 : "Usuário não cumpriu obrigações ou rompeu contrato com operador de telemetria (envio único)",
            301 : "Uso sazonal da água - captação de água desativada temporariamente com equipamentos desinstalados/impossibilidade de rápida ativação (captação só é montada em período específico do ano). Em caso de captação operacional realize a transmissão normal (96 leituras) ou pelo código 101 - envio 1x por semana",
            303 : "Captação de água desativada permanentemente com equipamentos de captação desinstalados/impossibilidade de rápida ativação/abandono da captação/falência (envio único)"
        }

    def audicao_lote(self, intervencao_id, dados_brutos):
        print(f"\n🤖 [AGENTE] Iniciando análise para: {intervencao_id}...")

        relatorio = {
            "alvo": intervencao_id,
            "status": "APROVADO", # muda caso contrario
            "alertas": [],
            "predicoes": []
        }

        if not dados_brutos:
            relatorio["status"] = "ERROR"
            relatorio["alertas"].append("Nenhum dado encontrado no banco de dados!")
            return relatorio
        

        resultado = self.lampiao.chat(f"faça um relatorio dos dados, nesse relatorio deve ter calculos de estatisticas utilizado pela DESO para analisar seguindo as metricas do DURH: {dados_brutos}, retonando a resposta se está aprovado ou não, seguindo esses criterios {self.regras_durh}")
        print(f"\n 🤖 [AGENTE] Análise completa: {resultado}")
        return resultado
