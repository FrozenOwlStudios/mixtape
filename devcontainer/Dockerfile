#============================== BASIC IMAGE ===================================  
FROM mcr.microsoft.com/devcontainers/miniconda:3

#============================== ADDING USER ====================================  
ARG USERNAME=USERNAME
ARG UID=1000
ARG GID=$UID

RUN if id -u $UID; then userdel `id -un $UID`; fi
RUN groupadd --gid $GID $USERNAME
RUN useradd --uid $UID --gid $GID -m $USERNAME



#========================== SYSTEM DEPENDENCIES ================================  
# Install system dependencie
RUN apt-get update && apt-get install -y --no-install-recommends 
COPY packages.txt /tmp/packages.txt
RUN cat /tmp/packages.txt | sed '/^#/d' | xargs apt-get install -y --no-install-recommends

# Enable sudo for remote user
RUN apt-get install -y sudo
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
RUN chmod 0440 /etc/sudoers.d/$USERNAME


#============================ GO ENVIRONMENT ===================================  
ENV GOPATH=/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin



#========================== PYTHON ENVIRONMENT ================================= 
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

#============================ POSTGRES SETUP =================================== 
RUN mkdir -p /var/lib/postgresql/data /run/postgresql 
RUN chown -R postgres:postgres /var/lib/postgresql /run/postgresql
RUN su - postgres -c "/usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/data"
RUN echo \"listen_addresses='*'\" >> /var/lib/postgresql/data/postgresql.conf 
RUN echo \"host all all 0.0.0.0/0 md5\" >> /var/lib/postgresql/data/pg_hba.conf

#============================= OTHER STUFF =====================================  
# Set up default command
CMD [ "bash" ]

# Keep everything alive via supervisor
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]


# Konfiguracja środowiska
ENV SHELL /bin/bash
USER $USERNAME

#============================ IMPLEMENT THIS =================================== 
# Download popular spaCy and NLTK resources
# RUN python -m spacy download en_core_web_sm && \
#     python -m nltk.downloader punkt averaged_perceptron_tagger wordnet

# Install go pakages that will deffinietly be used
# RUN go install github.com/jdkato/prose/v2@latest && \
#     go install github.com/gin-gonic/gin@latest && \
#     go install github.com/sashabaranov/go-openai@latest

# Create app user/db (user: app / pass: app / db: app)
# RUN su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data -o '-c listen_addresses=localhost' -w start" \
#  && su - postgres -c "psql -v ON_ERROR_STOP=1 -c \"CREATE USER app WITH PASSWORD 'app';\" -c \"CREATE DATABASE app OWNER app;\"" \
#  && su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data -m fast -w stop"

# # ---------- Redis (foreground mode) ----------
# RUN sed -i 's/^#\?bind .*/bind 0.0.0.0/' /etc/redis/redis.conf \
#  && sed -i 's/^#\?protected-mode .*/protected-mode no/' /etc/redis/redis.conf \
#  && sed -i 's/^#\?daemonize .*/daemonize no/' /etc/redis/redis.conf

# # ---------- RabbitMQ ----------
# RUN rabbitmq-plugins enable --offline rabbitmq_management