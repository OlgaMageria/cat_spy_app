FROM python:3.12-slim

WORKDIR /app

# Install uv with pip
RUN pip install uv

# Make sure uv is in PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]