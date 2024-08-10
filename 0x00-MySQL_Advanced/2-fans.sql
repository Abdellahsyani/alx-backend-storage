-- rank the country origin of bands

SELECT origin, SUM(fans) AS nb_fans
	FROM metal_bands
	GROUP BY origin
	GROUP BY nb_fans DESC; 
