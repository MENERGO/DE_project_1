CREATE OR REPLACE VIEW showcase AS
with news as
(
	select c.id ids, c.title categories, s.title sources, a.title titles, a.pubdate pubdate
	from content.category c
	left join content.category_article ca on c.id = ca.category_id
	left join content.article a on ca.article_id = a.id
	left join content.source s on source_id = s.id
),
news_all as (
	select ids, categories, count(titles) news_all_c
from news al
group by ids, categories
),
news_all_l as
(
	select ids, count(titles) news_all_l_c
	from news
	group by ids, categories, sources
	having sources = 'Lenta.ru : Новости'
),
news_all_v as
(
	select ids, count(titles) news_all_v_c
	from news
	group by ids, categories, sources
	having sources LIKE '%Ежедневная деловая газета'
),
news_all_t as
(
	select ids, count(titles) as news_all_t_c
	from news
	group by ids, categories, sources
	having sources = 'ТАСС'
),
news_all_day as
(
	select ids, count(titles) news_all_day_c
	from news
	where pubdate > (SELECT NOW() - INTERVAL '1 DAY')
	group by ids
),
news_all_day_l as
(
	select ids, count(titles) news_all_day_l_c
	from news
	where pubdate > (SELECT NOW() - INTERVAL '1 DAY')
	group by ids, categories, sources
	having sources = 'Lenta.ru : Новости'
),
news_all_day_v as
(
	select ids, count(titles) news_all_day_v_c
	from news
	where pubdate > (SELECT NOW() - INTERVAL '1 DAY')
	group by ids, categories, sources
	having sources LIKE '%Ежедневная деловая газета'
),
news_all_day_t as
(
	select ids, count(titles) as news_all_day_t_c
	from news
	where pubdate > (SELECT NOW() - INTERVAL '1 DAY')
	group by ids, categories, sources
	having sources = 'ТАСС'
),
news_avg as
(
	select ids, DATE(pubdate), count(titles) cou
	from news
	group by ids, DATE(pubdate)
),
news_all_avg as
(
select ids, avg(cou) news_all_avg_a
from news_avg
group by ids
),
news_date as (
	select ids, categories, DATE(pubdate) ddate, count(titles) couu
	from news
	group by ids, categories, pubdate
	order by categories
),
news_max_day as
(
	select ids, (select ddate
	from news_date b
	where a.ids = b.ids and b.couu= max(a.couu)
	limit 1) as news_max_day_all
	from news_date a
	group by ids
),
news_mon as
(
	select ids, count(titles) news_mon_c
	from news
	where to_char(pubdate, 'dy') = 'mon'
	group by ids
),
news_tue as
(
	select ids, count(titles) news_tue_c
	from news
	where to_char(pubdate, 'dy') = 'tue'
	group by ids
),
news_wed as
(
	select ids, count(titles) news_wed_c
	from news
	where to_char(pubdate, 'dy') = 'wed'
	group by ids
),
news_thu as
(
	select ids, count(titles) news_thu_c
	from news
	where to_char(pubdate, 'dy') = 'thu'
	group by ids
),
news_fri as
(
	select ids, count(titles) news_fri_c
	from news
	where to_char(pubdate, 'dy') = 'fri'
	group by ids
),
news_sat as
(
	select ids, count(titles) news_sat_c
	from news
	where to_char(pubdate, 'dy') = 'sat'
	group by ids
),
news_sun as
(
	select ids, count(titles) news_sun_c
	from news
	where to_char(pubdate, 'dy') = 'sun'
	group by ids
)
select al.ids "Суррогатный ключ",
	al.categories "Категория",
	news_all_c "Всего",
	news_all_l_c "Lenta",
	news_all_v_c "Ведомости",
	news_all_t_c "ТАСС",
	news_all_day_c "Всего/день",
	news_all_day_l_c "Lenta/день",
	news_all_day_v_c "Ведомости/день",
	news_all_day_t_c "ТАСС/день",
	news_all_avg_a "avg, всего",
	news_max_day_all "дата/max count news",
	news_mon_c mon,
	news_tue_c tue,
	news_wed_c wed,
	news_thu_c thu,
	news_fri_c fri,
	news_sat_c sat,
	news_sun_c sun
from news_all al
left join news_all_l on al.ids = news_all_l.ids
left join news_all_v on al.ids = news_all_v.ids
left join news_all_t on al.ids = news_all_t.ids
left join news_all_day on al.ids = news_all_day.ids
left join news_all_day_l on al.ids = news_all_day_l.ids
left join news_all_day_v on al.ids = news_all_day_v.ids
left join news_all_day_t on al.ids = news_all_day_t.ids
left join news_all_avg on al.ids = news_all_avg.ids
left join news_max_day on al.ids = news_max_day.ids
left join news_mon on al.ids = news_mon.ids
left join news_tue on al.ids = news_tue.ids
left join news_wed on al.ids = news_wed.ids
left join news_thu on al.ids = news_thu.ids
left join news_fri on al.ids = news_fri.ids
left join news_sat on al.ids = news_sat.ids
left join news_sun on al.ids = news_sun.ids
order by categories
