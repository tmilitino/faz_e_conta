
from ETL.extract import BasicExtract
from ETL.transform import DistribuicaoPartido, DespesasTotais, RankingPartido
from ETL.load import DespesasTotaisLoad, DistribuicaoLoad, RankingLoad


class DespesaFlowBuilder():
    transform = DespesasTotais
    load      = DespesasTotaisLoad
    table     = 'fat_total_gastos_parlamentar'


class DistribuicaoFlowBuilder():
    transform = DistribuicaoPartido
    load      = DistribuicaoLoad
    table     = 'fat_distribuicao_partido'


class RankingFlowBuilder():
    transform = RankingPartido
    load      = RankingLoad
    table     = 'fat_ranking_partido'


class ManagerFlow():
    @staticmethod
    def executor(objectBuilder):
        df_extract = BasicExtract().executor()

        transformer = objectBuilder.transform(df_extract)
        df_transformeted = transformer.executor()

        loader = objectBuilder.load(
            objectBuilder.table, df_transformeted)
        loader.executor()


if __name__ == "__main__":
    ManagerFlow.executor(DespesaFlowBuilder)
    ManagerFlow.executor(DistribuicaoFlowBuilder)
    ManagerFlow.executor(RankingFlowBuilder)
