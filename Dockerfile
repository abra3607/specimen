FROM debian:unstable

ENV DEBIAN_FRONTEND="noninteractive"

# Combine RUN instructions and clean up apt cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    graphviz \
    automake \
    libtool \
    sudo \
    sqlite3 \
    vim \
    git \
    ffmpeg \
    zsh \
    procps \
    npm \
    ruby-full \
    tmux \
    cargo \
    just

# install python dep manager
RUN zsh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'

RUN cargo install jj-cli

# install ai agents
RUN npm install -g @google/gemini-cli
RUN npm install -g @openai/codex
RUN npm install -g @anthropic-ai/claude-code

# install container process manager
RUN gem install overmind

WORKDIR /workspace

COPY . /workspace

RUN /root/.local/bin/uv sync