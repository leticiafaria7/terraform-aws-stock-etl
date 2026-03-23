-- total de linhas da tabela
select count(*) from db_refined.ativos_ibov_fp;

-- datas mínima e máxima
select min(data) as min_data, max(data) as max_data from db_refined.ativos_ibov_fp;

-- selecionar uma data específica
select * from db_refined.ativos_ibov_fp where data = '2026-03-08' order by ticker;

-- ver tabela
select * from db_refined.ativos_ibov_fp limit 5;