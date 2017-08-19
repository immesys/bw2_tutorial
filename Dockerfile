FROM jupyter/pyspark-notebook

USER root
RUN apt-get update && apt-get install daemon

## GABE add any dependencies you need here

COPY start.sh /usr/local/bin/
COPY ragent /bin/
RUN chmod 0755 /bin/ragent
COPY bw2 /bin/
COPY rise_entity.ent /etc/
COPY WAVE.ipynb /home/$NB_USER
RUN chown $NB_USER /home/$NB_USER/WAVE.ipynb
