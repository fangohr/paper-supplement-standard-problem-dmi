FROM ubuntu:18.04

# -----------------------------------------------------------------------------
# LIBRARIES

# ENTRYPOINT ["/bin/bash"]  
# SHELL ["/bin/bash", "-c"] 

# Avoid user interaction dialog
ENV DEBIAN_FRONTEND=noninteractive

# We need cython3 from the ubuntu repos, since cython-ising Sundials fail
# with pip cython
RUN apt update -y
RUN apt install -y build-essential cmake python3-dev python3-pip cython3 \
    python3-pytest-cov liblapack-dev libopenblas-dev \
    wget make gfortran libblas-dev liblapack-dev python3-tk sudo fonts-lato

RUN ln -s /usr/bin/python3 /usr/bin/python

# Next line for codecov target
RUN apt install -y curl git

RUN pip3 install ipywidgets nbval numpy scipy matplotlib==2.2.2 notebook psutil pytest pytest-cov -U
# RUN pip3 install --upgrade setuptools==20.4

# Headless Matplotlib:
ENV MPLBACKEND=Agg

# FIDIMAG ---------------------------------------------------------------------

WORKDIR /usr/local
RUN git clone https://github.com/computationalmodelling/fidimag.git
WORKDIR /usr/local/fidimag
# Work with stable release
RUN git checkout tags/v2.9

# Install CVODE and FFTW libraries
WORKDIR /usr/local/fidimag/bin
RUN bash install-fftw.sh
RUN bash install-sundials.sh

ENV PYTHONPATH="/usr/local/fidimag:$PYTHONPATH"
ENV LD_LIBRARY_PATH="/usr/local/fidimag/local/lib:$LD_LIBRARY_PATH"

WORKDIR /usr/local/fidimag
RUN python3 setup.py build_ext --inplace

# OOMMF BUILD -----------------------------------------------------------------
RUN apt install -y git tk-dev tcl-dev wget

# Compile oommf 2.0a and create OOMMFTCL environment variable
WORKDIR /usr/local
RUN git clone https://github.com/fangohr/oommf
WORKDIR /usr/local/oommf
# Use specific 2.0a version
RUN git checkout tags/2.0a0_20170929a0
RUN make build-with-dmi-extension-all
WORKDIR /usr/local
RUN mv oommf oommf_TMP && mv oommf_TMP/oommf oommf && rm -rf oommf_TMP 
ENV OOMMFTCL /usr/local/oommf/oommf.tcl

# Create executable oommf script
WORKDIR /usr/local/bin
RUN echo "#! /bin/bash" > oommf
RUN echo "tclsh /usr/local/oommf/oommf.tcl \"\$@\"" >> oommf
RUN chmod a+x oommf

# -----------------------------------------------------------------------------

# Install JOOMMF

RUN python3 -m pip install --upgrade \
    git+git://github.com/joommf/joommfutil.git \
    git+git://github.com/joommf/discretisedfield.git \
    git+git://github.com/joommf/micromagneticmodel.git \
    git+git://github.com/joommf/oommfodt.git \
    git+git://github.com/joommf/oommfc.git

# -----------------------------------------------------------------------------

# Set threads for OpenMP:
ENV OMP_NUM_THREADS=2
# WORKDIR /io

# -----------------------------------------------------------------------------
# User to make Binder happy
ENV NB_USER micromag
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

# Set the working directory
WORKDIR /home/${USER}/micromag/notebooks

# -----------------------------------------------------------------------------
