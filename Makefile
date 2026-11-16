# Rebuild every generated asset from tools/*.py.
# Requirements: python3 (with tools/requirements.txt), rsvg-convert (librsvg),
# and the Ubuntu + Inter fonts installed (or FONTS_DIR pointing to them).

PYTHON ?= .venv/bin/python
RSVG   ?= rsvg-convert

LOGO      := logo/toulouse-devops-logo.svg
MARK      := logo/toulouse-devops-mark.svg
KAKEMONO  := kakemono/toulouse-devops-kakemono-85x200

# Checkout of the toulouse-devops.org website (Astro). `make sync-site` copies
# the generated assets there; the site repo vendors them so its CI does not
# need this repository.
SITE       ?= ../toulousedevops.org
SITE_FILES := $(SITE)/public/static/brand
SITE_DATA  := $(SITE)/src/data/brand-palette.json

.PHONY: all logo palette kakemono venv clean sync-site

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

# Copy the published assets into the website. Run `make` first if sources changed.
sync-site:
	@test -d $(SITE)/src/pages || { echo "Website checkout not found at $(SITE) (set SITE=...)"; exit 1; }
	rm -rf $(SITE_FILES)
	mkdir -p $(SITE_FILES)/png $(SITE_FILES)/colors $(SITE_FILES)/kakemono
	cp logo/toulouse-devops-logo.svg logo/toulouse-devops-logo.pdf $(MARK) $(SITE_FILES)/
	cp logo/png/*.png $(SITE_FILES)/png/
	cp colors/palette.json colors/palette.css colors/palette.scss colors/toulouse-devops.gpl $(SITE_FILES)/colors/
	cp $(KAKEMONO).pdf kakemono/toulouse-devops-kakemono-preview.png $(SITE_FILES)/kakemono/
	cp colors/palette.json $(SITE_DATA)
	@echo "Synced brand assets into $(SITE). Review and commit there."
