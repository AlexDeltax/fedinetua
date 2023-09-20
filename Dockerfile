FROM archlinux:base-devel-20230910.0.177821 as base

RUN pacman -Syy
RUN pacman -S --noconfirm pango cairo libwebp gdk-pixbuf2 \
    ttf-liberation ttf-linux-libertine libimagequant lcms2 openjpeg2 \
    nano git python python-pip python-pipenv openssh

WORKDIR /

# Setup env
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home fedi
WORKDIR /home/fedi

# Install application into container
COPY . .

RUN mkdir /home/fedi/static && mkdir /home/fedi/media

RUN find /home/fedi -type f -exec chmod 0664 {} + \
    && find /home/fedi -type d -exec chmod 0775 {} +

RUN chown -R fedi:fedi /.venv/* \
    && chown -R fedi:fedi /home/fedi/*

USER fedi

CMD ["python manage.py runserver 0.0.0.0:8000"]
