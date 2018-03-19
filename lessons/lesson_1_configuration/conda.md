
<img src="https://github.com/Alexjmsherman/ml_guild/blob/master/raw_data/images/conda_logo.png" alt="conda_logo" width="60px" height="30" />


"Conda is an open source package management system and environment management system that runs on Windows, macOS and Linux. Conda quickly installs, runs and updates packages and their dependencies. Conda easily creates, saves, loads and switches between environments on your local computer. It was created for Python programs, but it can package and distribute software for any language.

Conda as a package manager helps you find and install packages. If you need a package that requires a different version of Python, you do not need to switch to a different environment manager, because conda is also an environment manager. With just a few commands, you can set up a totally separate environment to run that different version of Python, while continuing to run your usual version of Python in your normal environment."

	Source: https://conda.io/docs/

	Cheat Sheet: https://conda.io/docs/_downloads/conda-cheatsheet.pdf


### CONDA INSTALLATION
**create a basic conda environment**

	conda create --name guild

**create an environment with Python 3.6 and all anaconda packages**

	conda create --name guild python=3.6 anaconda -y

#### RESOLVE ERRORS
If you run into errors, such as an error downloading a .dll file or CondaError: PermissionError(13, 'Permission denied')

	conda clean --all --yes

### ENVIRONMENTS
**list conda environments**

	conda env list

<img src="https://github.com/Alexjmsherman/ml_guild/blob/master/raw_data/images/conda_envs.png" alt="conda_logo" width="200" height="200" />

### INSTALL PACKAGES SETUP
**add conda-forge to provide ease of access to install python packages**

	conda config --add channels conda-forge

### JUPYTER NOTEBOOK SETUP
**add new kernel to jupyer notebook to access kernel**

	http://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments
	
	https://stackoverflow.com/questions/37433363/link-conda-environment-with-jupyter-notebook


Type the following commands:

	source activate guild
		
	conda install nb_conda
		
	python -m ipykernel install --user --name myenv --display-name "guild environment"

#### RESOLVE ERRORS
**identify which python version is running in Jupyter notebook**

	import sys
	sys.executable

##### if it is the correct python version, try the following
	conda install ipykernel --name Python3


<img src="https://github.com/Alexjmsherman/ml_guild/blob/master/raw_data/images/conda_stack.png" alt="conda_logo" width="300" height="250" />


### RESOURCES:
conda vs pip vs virtualenv

	https://conda.io/docs/_downloads/conda-cheatsheet.pdf

Video: Managing python environments with conda

	https://www.youtube.com/watch?v=EGaw6VXV3GI

Effectively using open source with conda: 

	https://www.slideshare.net/teoliphant/effectively-using-open-source-with-conda

Create a virtual env with conda

	http://uoa-eresearch.github.io/eresearch cookbook/recipe/2014/11/20/conda/