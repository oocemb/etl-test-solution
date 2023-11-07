CREATE ROLE ro_user WITH LOGIN PASSWORD '12345';
GRANT CONNECT ON DATABASE postgres TO ro_user;
GRANT USAGE ON SCHEMA test TO ro_user;
GRANT SELECT ON ALL TABLES IN SCHEMA test TO ro_user;
GRANT pg_write_server_files TO ro_user;
create type type_nmb as (_type text, nmb int);

create or replace function select_all_subject_info()
RETURNS TABLE("Субъект РФ" text, "Вид обращения" text, "Количество записей" int, "%" text, "nmb" int) AS $$
declare
	strSQL text := '';
	nmb int;
	_type text;
	type_array type_nmb[] := array[('EПГУ', 1), ('РПГУ', 2), ('Регистратура', 3), ('Инфомат', 4), ('Call center', 5), ('АРМ медработника', 6), ('Прочие', 7), ('Всего записей', 9)];
begin
	foreach _type, nmb in array type_array
	loop
		strSQL := strSQL || format('
	    	SELECT DISTINCT
		    	f."Субъект РФ"::text,
				''%1$s'' as "Вид обращения",
				case
			        when %1$I = 0 then NULL
			    else 
			        %1$I
			    end as "Количество записей",
				case
			        when %1$I = 0 then NULL
			    else 
			        to_char(%1$I*100.0/"Всего записей", ''990.99'')
			    end as "%%",
				%2$s as nmb
	    	FROM test.fer as f
			union all ', _type, nmb);
	END LOOP;
	strSQL := strSQL || 'select distinct 
		"Субъект РФ",
		''Записей не через ЕПГУ'' as "Вид обращения",
		case
	        when "Всего записей"-"EПГУ" = 0 then NULL
	    else 
	        "Всего записей"-"EПГУ"
	    end as "Количество записей",
		case
	        when "Всего записей"-"EПГУ" = 0 then NULL
	    else 
	        to_char(("Всего записей"-"EПГУ")*100.0/"Всего записей", ''990.99'')
	    end as "%%",
		8 as nmb
		from test.fer as f
		order by "Субъект РФ", nmb';
	RETURN QUERY execute strSQL;
END;
$$ LANGUAGE plpgsql;

CREATE or replace FUNCTION select_sum_subject_info()
RETURNS TABLE("Субъект РФ" text, "Вид обращения" text, "Количество записей" bigint, "%" text, "nmb" int) AS $$
declare
	strSQL text := '';
	nmb int;
	_type text;
	type_array type_nmb[] := array[('EПГУ', 1), ('РПГУ', 2), ('Регистратура', 3), ('Инфомат', 4), ('Call center', 5), ('АРМ медработника', 6), ('Прочие', 7), ('Всего записей', 9)];
begin
	foreach _type, nmb in array type_array
	loop
		strSQL := strSQL || format('select 
				''Российская Федерация'' as "Субъект РФ", 
				''%1$s'' as "Вид обращения",
				sum(%1$I) as "Количество записей",
				to_char(sum(%1$I)*100.0/sum("Всего записей"), ''990.99'') as "%%",
				%2$s as nmb
				from (select distinct * from test.fer) as f
				union all ', _type, nmb);
	END LOOP;
	strSQL := strSQL || 'select 
			''Российская Федерация'' as "Субъект РФ", 
			''Записей не через ЕПГУ'' as "Вид обращения",
			sum("Всего записей"-"EПГУ") as "Количество записей",
			to_char(sum("Всего записей"-"EПГУ")*100.0/sum("Всего записей"), ''990.99'') as "%%",
			8 as nmb
			from (select distinct * from test.fer) as f
			order by nmb';
	RETURN QUERY execute strSQL;
END;
$$ LANGUAGE plpgsql;

set role ro_user;

COPY (select "Субъект РФ", "Вид обращения", "Количество записей", "%" from (
select * from select_sum_subject_info()
union all
select * from select_all_subject_info()
) _result) TO '/tmp/goal_test.csv' (FORMAT csv, HEADER);

