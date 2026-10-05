FROM python@sha256:88310c082760d93ac7c74d579e95e53a4ab6ea52dd8901abc61a103daf488ac4
ARG SOURCE_COMMIT
ENV HAG_SOURCE_COMMIT=${SOURCE_COMMIT}
LABEL org.opencontainers.image.revision=${SOURCE_COMMIT}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY system-packages.lock.json /opt/system-packages.lock.json
COPY scripts/fetch_system_packages.py /tmp/fetch_system_packages.py
RUN python /tmp/fetch_system_packages.py /opt/system-packages.lock.json /tmp/system-packages && dpkg --install /tmp/system-packages/*.deb && rm -r /tmp/system-packages
COPY requirements.lock /tmp/requirements.lock
COPY requirements.lock /opt/requirements.lock
RUN python -m pip install --no-cache-dir --require-hashes -r /tmp/requirements.lock
COPY vendor/se_harness-0.22.1-py3-none-any.whl /opt/evaluator-wheel/se_harness-0.22.1-py3-none-any.whl
RUN python -m venv /opt/evaluator && /opt/evaluator/bin/python -I -m pip install --no-deps /opt/evaluator-wheel/se_harness-0.22.1-py3-none-any.whl
COPY pyproject.toml /tmp/service/pyproject.toml
COPY contracts /tmp/service/contracts
COPY hosted_artifact_graph /tmp/service/hosted_artifact_graph
RUN python -m pip wheel --no-deps --no-build-isolation --wheel-dir /opt/service-wheel /tmp/service && python -m pip install --no-deps /opt/service-wheel/*.whl
WORKDIR /tmp
EXPOSE 8080
ENTRYPOINT ["harness-hosted"]
CMD ["serve"]
