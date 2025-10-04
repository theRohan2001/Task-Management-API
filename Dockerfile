FROM python:3.13-slim

# Install deps for uv
RUN apt-get update && apt-get install --no-install-recommends -y \
        curl build-essential bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv (Astral’s package manager)
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

# Set up uv environment path
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

# Install dependencies with uv
RUN uv sync

# Ensure uv venv binaries are on PATH
ENV PATH="/.venv/bin:${PATH}"

# Run FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
