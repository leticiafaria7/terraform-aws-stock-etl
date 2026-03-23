-- join
select F.ticker, D.empresa, D.setor, D.subsetor, D.segmento, F.data, F.abertura_dia, F.fechamento_dia, F.variacao_dia
from db_refined.ativos_ibov_fp F
left join db_refined.ativos_ibov_dim D on F.ticker = D.ticker
where D.setor = 'Financeiro'
and F.data = '2026-03-10';