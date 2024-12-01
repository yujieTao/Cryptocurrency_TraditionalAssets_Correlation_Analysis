
all: data model visualize
data:
	python src/data/scripts/process_data.py

model:
	python src/models/scripts/correlation_analysis.py

visualize:
	python src/visualization/scripts/generate_heatmaps.py

clean:
	rm -rf src/visualization/plots/*
	rm -rf logs/*.log
