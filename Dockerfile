FROM jupyter/pyspark-notebook

USER root
RUN apt-get update && apt-get install -y daemon python-pip

## GABE add any dependencies you need here
ADD python /home/$NB_USER/
ENV PYTHONPATH /home/$NB_USER/python
RUN pip2 install msgpack-python

RUN python2 -m pip install ipython==5.4 ipykernel
RUN python2 -m ipykernel install --user
RUN chown -R $NB_USER /home/$NB_USER/.local/share/jupyter
RUN mkdir -p /home/$NB_USER/.ipynb_checkpoints
RUN chown -R $NB_USER /home/$NB_USER/.ipynb_checkpoints

COPY start.sh /usr/local/bin/
COPY ragent /bin/
RUN chmod 0755 /bin/ragent
COPY bw2 /bin/
COPY rise_entity.ent /etc/
COPY WAVE.ipynb /home/$NB_USER
RUN chown $NB_USER /home/$NB_USER/WAVE.ipynb
