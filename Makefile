# Rebuild every generated asset from tools/*.py.
# Requirements: python3 (with tools/requirements.txt), rsvg-convert (librsvg),
# and the Ubuntu + Inter fonts installed (or FONTS_DIR pointing to them).

PYTHON ?= .venv/bin/python
RSVG   ?= rsvg-convert

LOGO      := logo/toulouse-devops-logo.svg
MARK      := logo/toulouse-devops-mark.svg
KAKEMONO  := kakemono/toulouse-devops-kakemono-85x200

.PHONY: all logo palette kakemono venv clean

all: logo palette kakemono

venv:
	python3 -m venv .venv
	.venv/bin/pip install -r tools/requirements.txt

logo:
	$(PYTHON) tools/build_logo.py
	$(RSVG) -f pdf $(LOGO) -o logo/toulouse-devops-logo.pdf
	for w in 256 512 1024 2048; do \
		$(RSVG) -w $$w $(LOGO) -o logo/png/toulouse-devops-logo-$${w}px.png; \
		$(RSVG) -w $$w -b '#ffffff' $(LOGO) -o logo/png/toulouse-devops-logo-$${w}px-white.png; \
	done
	for w in 256 512 1024; do \
		$(RSVG) -w $$w $(MARK) -o logo/png/toulouse-devops-mark-$${w}px.png; \
	done

palette:
	$(PYTHON) tools/build_palette.py

kakemono: logo
	$(PYTHON) tools/build_kakemono.py
	$(RSVG) -f pdf $(KAKEMONO).svg -o $(KAKEMONO).pdf
	$(RSVG) -h 2000 $(KAKEMONO).svg -o kakemono/toulouse-devops-kakemono-preview.png

clean:
	rm -f logo/*.pdf logo/png/*.png kakemono/*.pdf kakemono/*.png
