TARGETS := html/script.js html/callback.js
all: $(TARGETS)
clean:
	rm -f $(TARGETS)

%.js: %.ts
	tsc --removeComments --out $@ $<
