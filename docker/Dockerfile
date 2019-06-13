FROM glueviz/py36-pyqt512:1.1
LABEL authors="Thomas Robitaille <thomas.robitaille@gmail.com>"

RUN apt install sudo
RUN cp /usr/bin/pip3 /usr/bin/pip
RUN pip install git+https://github.com/astrofrog/pyinstaller.git@develop
RUN apt install -y upx
RUN apt install -y libxkbcommon-x11-0
