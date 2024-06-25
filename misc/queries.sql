-- Quais são as 5 fontes de recursos que mais arrecadaram?

select
nome_fonte_recursos,
round(total_arrecadado, 2) total_arrecadado
from sp_budget.app_sp_budget
order by total_arrecadado desc
limit 5

-- Quais são as 5 fontes de recursos que mais gastaram?

select
nome_fonte_recursos,
round(total_liquidado, 2) total_liquidado
from sp_budget.app_sp_budget
order by total_liquidado desc
limit 5

-- Quais são as 5 fontes de recursos que menir arrecadaram?

select
nome_fonte_recursos,
round(total_arrecadado, 2) total_arrecadado
from sp_budget.app_sp_budget
order by total_arrecadado asc
limit 5

-- Quais são as 5 fontes de recursos que menir gastaram?

select
nome_fonte_recursos,
round(total_liquidado, 2) total_liquidado
from sp_budget.app_sp_budget
order by total_liquidado asc
limit 5

-- Quais são as 5 fontes de recursos com a melhor margem bruta?

select
nome_fonte_recursos,
round(total_arrecadado - total_liquidado, 2) margem_bruta
from sp_budget.app_sp_budget
order by total_arrecadado - total_liquidado desc
limit 5

-- Quais são as 5 fontes de recursos com a pior margem bruta?

select
nome_fonte_recursos,
round(total_arrecadado - total_liquidado, 2) margem_bruta
from sp_budget.app_sp_budget
order by total_arrecadado - total_liquidado asc
limit 5

-- Qual a média de arrecadação por fonte de recurso?

select
fonte_de_recursos,
round(avg(arrecadado), 2) media_arrecadacao
FROM sp_budget.raw_gdvreceitasexcel
where fonte_de_recursos is not null
group by fonte_de_recursos

-- Qual a média de gastos por fonte de recurso?

select
fonte_de_recursos,
round(avg(liquidado), 2) media_gastos
FROM sp_budget.raw_gdvdespesasexcel
where fonte_de_recursos is not null
group by fonte_de_recursos