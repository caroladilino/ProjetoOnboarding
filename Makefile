.PHONY: ci api-ci even-ci odd-ci save-ci check-ci bbp-ci

ci: api-ci even-ci odd-ci save-ci check-ci bbp-ci

api-ci:
	make -C api ci

even-ci:
	make -C even ci

odd-ci:
	make -C odd ci

save-ci:
	make -C save ci

check-ci:
	make -C check ci
