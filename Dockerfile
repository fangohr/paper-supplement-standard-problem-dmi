FROM ubuntu:16.04

RUN apt -y update 
RUN apt install -y git python3 python3-pip gcc psutils cmake wget make
RUN apt install -y gfortran libblas-dev liblapack-dev python3-tk sudo fonts-lato
RUN pip3 install cython matplotlib pytest scipy psutil pyvtk ipywidgets
RUN pip3 install --no-cache-dir notebook

RUN ln -s /usr/bin/python3 /usr/bin/python

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
RUN python3 -c "import matplotlib"
# Headless Matplotlib:
ENV MPLBACKEND=Agg

# OOMMF BUILD
RUN apt install -y git tk-dev tcl-dev wget

# Compile oommf 2.0a and create OOMMFTCL environment variable
WORKDIR /usr/local
RUN git clone https://github.com/davidcortesortuno/oommf.git
RUN mv oommf oommf_TMP && mv oommf_TMP/oommf oommf && rm -rf oommf_TMP 
WORKDIR /usr/local/oommf
RUN ./oommf.tcl pimake
ENV OOMMFTCL /usr/local/oommf/oommf.tcl

# Create executable oommf script
WORKDIR /usr/local/bin
RUN echo "#! /bin/bash" > oommf
RUN echo "tclsh /usr/local/oommf/oommf.tcl \"\$@\"" >> oommf
RUN chmod a+x oommf

# Install JOOMMF
RUN pip3 install oommfc -U
RUN pip3 install oommfodt -U

# Headless Matplotlib:
ENV MPLBACKEND=Agg

# Set threads for OpenMP:
# ENV OMP_NUM_THREADS=2
# WORKDIR /io

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

# Set up user so that we do not run as root
# (not necessary if we run docker with --user)
# -s for shell, -m to create home directory, -G groups
#
# RUN useradd -m -s /bin/bash -G sudo fidimag && \
#     echo "fidimag:docker" | chpasswd && \
#     echo "fidimag ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# # -R recursive
# RUN chown -R fidimag:fidimag /usr/local/fidimag

