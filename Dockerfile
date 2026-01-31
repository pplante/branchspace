FROM ubuntu:latest
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=dev
ARG USER_UID=1001
ARG USER_GID=$USER_UID

RUN <<EOF
apt-get update
apt-get install -y \
    build-essential \
    ca-certificates \
    locales \
    fonts-powerline \
    zsh \
    git \
    curl \
    wget \
    zip \
    unzip \
    sed \
    sudo
rm -rf /var/lib/apt/lists/*
EOF

RUN <<EOF
echo "en_US.UTF-8 UTF-8" >> /etc/locale.ge
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8
EOF

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

RUN <<EOF
groupadd --gid $USER_GID $USERNAME
useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
usermod --shell /bin/zsh $USERNAME
echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
chmod 0440 /etc/sudoers.d/$USERNAME
EOF

COPY <<EOF /usr/local/bin/zai
#!/usr/bin/env zsh
set -euo pipefail
set -a; source .env; set +a

# Check required environment variables
if [[ -z "\${ZAI_BASE_URL:-}" ]]; then
  echo "Error: ZAI_BASE_URL environment variable is not set" >&2
  exit 1
fi

if [[ -z "\${ZAI_AUTH_TOKEN:-}" ]]; then
  echo "Error: ZAI_AUTH_TOKEN environment variable is not set" >&2
  exit 1
fi

export ANTHROPIC_BASE_URL=\$ZAI_BASE_URL
export ANTHROPIC_AUTH_TOKEN=\$ZAI_AUTH_TOKEN
export ANTHROPIC_MODEL=\$ZAI_MODEL
export ANTHROPIC_SMALL_FAST_MODEL=\$ZAI_SMALL_FAST_MODEL
mise x -- claude "\$@"
EOF
RUN chmod +x /usr/local/bin/zai

USER $USERNAME

RUN <<EOF
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
git clone https://github.com/zsh-users/zsh-autosuggestions $HOME/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sed -i 's|^plugins=.*|plugins=(git mise zsh-autosuggestions zsh-syntax-highlighting)|g' ~/.zshrc
EOF

SHELL ["/bin/zsh", "-o", "pipefail", "--login", "-c"]

WORKDIR /claude
WORKDIR /workspace

STOPSIGNAL SIGTERM
ENTRYPOINT []
