CHROME ?= chrome

# for some reason the fonts don't render correctly for ć without the `--virtual-time-budget=10000` option
# we use intermediate file (.resume.html) instead of direct base64 because on some OSs we get Argument list too long error
resume.pdf: resume.md style.css
	@pandoc \
		--data-dir . \
		--template default \
		--css style.css \
		--embed-resources \
		--standalone resume.md \
		-o .resume.html
	@$(CHROME) \
		--headless=new \
		--virtual-time-budget=10000 \
		--run-all-compositor-stages-before-draw \
		--no-pre-read-main-dll \
		--no-first-run \
		--no-sandbox \
		--no-default-browser-check \
		--no-pdf-header-footer \
		--print-to-pdf="resume.pdf" \
		.resume.html

.PHONY: write
write:
	@./live_compile.py --verbose

.PHONY: spellcheck
spellcheck:
	@pre-commit run vale --all-files

.PHONY: pre-commit
pre-commit:
	@pre-commit run --all-files
