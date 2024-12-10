drop schema if exists kmeans cascade;
create schema kmeans;
set search_path = 'kmeans';
create table models(id integer, cluster integer, x float,y float);
create table points(x float, y float, g integer);

CREATE OR REPLACE FUNCTION distance(x0 FLOAT, y0 FLOAT, x1 FLOAT, y1 FLOAT)
RETURNS FLOAT AS $$
    SELECT SQRT(POWER(x1 - x0, 2) + POWER(y1 - y0, 2));
$$ LANGUAGE SQL;

create function nearest_cluster(model integer, xcoord float, ycoord float) returns integer language sql as $$
	with center(cluster, x, y) as (select cluster, x, y from models where id=model)
		select cluster from center order by distance(x, y, xcoord, ycoord) asc limit 1;
$$;
create procedure generate_points(center_x float, center_y float, radius float, points integer, cluster integer) language sql as $$
	with polar(angle, distance) as (select random() * 2.0 * pi(), random() * radius from generate_series(1,points))
		insert into points (x, y, g) select center_x + cos(angle) * distance, center_y + sin(angle) * distance, cluster from polar;
$$;

create sequence model_id start 100;

create function create_model(clusters integer) returns integer language sql as $$
	with numbering (i) as (select nextval('model_id')) 
		insert into models (id, cluster) select i, x from numbering, generate_series(1, clusters) as x returning id;
$$;
create function init_model(model int, x_min float, x_max float, y_min float, y_max float) returns integer language sql as $$
	update models set x = x_min + random() * (x_max-x_min), y = y_min + random() * (y_max - y_min) where id = model returning 0;
$$;
create function classify_points(model int) returns integer language sql as $$
	update points set g = nearest_cluster(model, x, y) where g <> nearest_cluster(model, x, y) or g is null returning 0;
$$;

CREATE OR REPLACE FUNCTION run_kmeans(model_id INT, max_iterations INT, convergence_threshold INT DEFAULT 0)
RETURNS VOID AS $$
DECLARE
  changed_points INT;
  iteration_count INT := 0;
BEGIN
  LOOP
    iteration_count := iteration_count + 1;
    SELECT classify_points(model_id) INTO changed_points;
    IF changed_points <= convergence_threshold OR iteration_count >= max_iterations THEN
      RAISE NOTICE 'K-means converged after % iterations.', iteration_count;
      EXIT;
    END IF;
    PERFORM recalculate_centroids(model_id);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

call generate_points(1, 1, 1, 50, 1);
call generate_points(5, 5, 1, 50, 2);
call generate_points(9, 9, 1, 50, 3);

DO $$
DECLARE
  model_id INTEGER;
BEGIN
  SELECT create_model(3) INTO model_id;
  PERFORM init_model(model_id, 0, 10, 0, 10);
  PERFORM run_kmeans(model_id, 100, 1);
END;
$$;

SELECT * FROM points;
SELECT * FROM models;

SHOW server_encoding;