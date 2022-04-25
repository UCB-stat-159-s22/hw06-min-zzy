.PHONY: env
env: 
	conda env create -f environment.yml 
	conda activate ligo;python -m ipykernel install --user --name ligo --display-name "IPython - ligo"

.PHONY: html
html:
	jupyterbook build .

.PHONY: html-hub
html-hub:
	jupyter-book config sphinx .
	sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	cd _build/html
	python -m http.server
	
.PHONY: clean
clean:
	rm -f figurs/*.png
	rm -f audio/*.wav
	rm -rf _build/*