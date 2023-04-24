FROM python:3.10.11
WORKDIR /ai
RUN apt-get update; apt-get -y install pulseaudio
ENV PULSE_SERVER=docker.for.mac.localhost
RUN apt-get -y install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
RUN pip install pyaudio
RUN pip install  EdgeGPT 
RUN pip install ffmpeg
RUN pip install openai
RUN pip install asyncio
RUN pip install whisper
RUN pip install boto3
RUN pip install pydub
RUN pip install SpeechRecognition
RUN apt-get update && apt-get install -y \
    vorbis-tools \
    sox \
    alsa-utils \
    libasound2 \
    libasound2-plugins \
    pulseaudio \
    pulseaudio-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
COPY mainV1.py /ai
CMD [ "python", "mainV1.py" ]

