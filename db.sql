drop schema if exists kmeans_sednevg325 cascade;
create schema kmeans_sednevg325;
create table points(x float, y float);
set search_path = 'kmeans_sednevg325';