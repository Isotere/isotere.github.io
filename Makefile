.DEFAULT_GOAL := help

PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON_BIN ?= python3.14
VENV_DIR := $(PROJECT_DIR)/.venv
VENV_PYTHON := $(VENV_DIR)/bin/python
ZENSICAL := $(VENV_DIR)/bin/zensical
DEV_ADDR ?= 127.0.0.1:8000
PREVIEW_PORT ?= 8001
GIT_NOREPLY_EMAIL ?=

export TZ := Europe/Moscow

.PHONY: help venv install serve build check preview clean require-deps git-privacy privacy-check test-privacy

help:
	@printf '%s\n' \
	  'make install  — создать .venv и установить зависимости' \
	  'make serve    — открыть сервер разработки на http://127.0.0.1:8000' \
	  'make build    — собрать сайт в site/ со строгой проверкой' \
	  'make check    — собрать сайт и проверить зависимости' \
	  'make preview  — показать результат сборки на http://127.0.0.1:8001' \
	  'make clean    — удалить site/ и .cache/, сохранив .venv' \
	  'make venv     — создать только локальное окружение' \
	  'make git-privacy — настроить публичную Git identity и hooks' \
	  'make privacy-check — проверить identity и метаданные текущей истории' \
	  'make test-privacy — проверить Git hooks на синтетических данных' \
	  '' \
	  'Другой Python: make install PYTHON_BIN=/path/to/python3' \
	  'Другой адрес: make serve DEV_ADDR=127.0.0.1:8080'

$(VENV_PYTHON):
	@command -v "$(PYTHON_BIN)" >/dev/null 2>&1 || { \
	  printf '%s\n' 'Не найден $(PYTHON_BIN). Укажи установленный Python через PYTHON_BIN.' >&2; \
	  exit 1; \
	}
	@"$(PYTHON_BIN)" -c 'import sys; sys.exit("Нужен Python 3.11 или новее.") if sys.version_info < (3, 11) else None'
	"$(PYTHON_BIN)" -m venv "$(VENV_DIR)"

venv: $(VENV_PYTHON)

install: venv
	"$(VENV_PYTHON)" -m pip install --disable-pip-version-check -r "$(PROJECT_DIR)/requirements.txt"
	"$(VENV_PYTHON)" -m pip check

require-deps:
	@if [ ! -x "$(VENV_PYTHON)" ] || [ ! -x "$(ZENSICAL)" ]; then \
	  printf '%s\n' 'Сначала выполни make install: зависимости должны находиться в .venv этого проекта.' >&2; \
	  exit 1; \
	fi

serve: require-deps
	cd "$(PROJECT_DIR)" && "$(ZENSICAL)" serve --dev-addr "$(DEV_ADDR)"

build: require-deps
	cd "$(PROJECT_DIR)" && "$(ZENSICAL)" build --clean --strict

check: build
	"$(VENV_PYTHON)" -m pip check

preview: build
	"$(VENV_PYTHON)" -m http.server "$(PREVIEW_PORT)" --bind 127.0.0.1 --directory "$(PROJECT_DIR)/site"

clean:
	$(RM) -r "$(PROJECT_DIR)/site" "$(PROJECT_DIR)/.cache"

git-privacy:
	cd "$(PROJECT_DIR)" && "$(PYTHON_BIN)" -B scripts/setup_git_privacy.py --email "$(GIT_NOREPLY_EMAIL)"

privacy-check:
	cd "$(PROJECT_DIR)" && "$(PYTHON_BIN)" -B scripts/git_privacy.py identity
	cd "$(PROJECT_DIR)" && "$(PYTHON_BIN)" -B scripts/git_privacy.py history

test-privacy:
	cd "$(PROJECT_DIR)" && "$(PYTHON_BIN)" -B -m unittest discover -s tests -p 'test_git_privacy.py' -v
