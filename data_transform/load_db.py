
from ETL.extract import BasicExtract
from ETL import transform
from ETL import load


class DespesaFlowBuilder():
    transform = transform.DespesasTotais
    load      = load.DespesasTotaisLoad
    table     = 'fat_total_gastos_parlamentar'


class DistribuicaoFlowBuilder():
    transform = transform.DistribuicaoPartido
    load      = load.DistribuicaoLoad
    table     = 'fat_distribuicao_partido'


class RankingFlowBuilder():
    transform = transform.RankingPartido
    load      = load.RankingLoad
    table     = 'fat_ranking_partido'

class DespesaPartidoFlowBuilder():
    transform = transform.DespesasPartidos
    load      = load.DespesasPartidosLoad
    table     = 'fat_despesa_partido'


class TimeSeiresCandidatoFlowBuilder():
    transform = transform.TimeSeriesCandidato
    load      = load.TimeSeiresCandidatoLoad
    table     = 'fat_time_seires_candidato'


class ManagerFlow():
    @staticmethod
    def executor(objectBuilder, ano):
        df_extract = BasicExtract().executor(ano)

        transformer = objectBuilder.transform(df_extract)
        df_transformeted = transformer.executor()

        loader = objectBuilder.load(
            objectBuilder.table, df_transformeted)
        loader.executor()


if __name__ == "__main__":
    for ano in range(2008,2023):
            
        ManagerFlow.executor(DespesaFlowBuilder, ano)
        ManagerFlow.executor(DistribuicaoFlowBuilder, ano)
        ManagerFlow.executor(RankingFlowBuilder, ano)
        ManagerFlow.executor(TimeSeiresCandidatoFlowBuilder, ano)
        ManagerFlow.executor(DespesaPartidoFlowBuilder, ano)
