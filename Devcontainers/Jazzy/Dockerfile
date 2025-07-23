# Wybór obrazu
FROM ros:jazzy

# USERNAME brane z devcontainer.json
ARG USERNAME=USERNAME
ARG UID=1000
ARG GID=$UID

# Dodawanie nowego użytkownika
RUN if id -u $UID; then userdel `id -un $UID`; fi
RUN groupadd --gid $GID $USERNAME
RUN useradd --uid $UID --gid $GID -m $USERNAME

# Paskudne obejście problemów z podpisami w repozytoriach
RUN rm /etc/apt/sources.list.d/ros2-latest.list && \
    apt update && apt install curl && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null



# Uaktualnienie systemu
RUN apt-get update
RUN apt-get upgrade -y

# Wsparcie dla sudo
RUN apt-get install -y sudo
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
RUN chmod 0440 /etc/sudoers.d/$USERNAME

# Instalacja dodatkowych pakietów
RUN apt-get install -y python3-pip  ros-jazzy-desktop

# Konfiguracja środowiska
ENV SHELL /bin/bash
USER $USERNAME
