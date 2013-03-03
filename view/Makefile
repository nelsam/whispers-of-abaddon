BOOTSTRAP = ./docs/assets/static/css/bootstrap.css
BOOTSTRAP_LESS = ./static/less/bootstrap.less
BOOTSTRAP_RESPONSIVE = ./docs/assets/static/css/bootstrap-responsive.css
BOOTSTRAP_RESPONSIVE_LESS = ./static/less/responsive.less
DATE=$(shell date +%I:%M%p)
CHECK=\033[32m✔\033[39m
HR=\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#


#
# BUILD DOCS
#

build:
	@echo "\n${HR}"
	@echo "Building Bootstrap..."
	@echo "${HR}\n"
	@find static/js -iname '*.js' ! -name 'less.js' -exec jshint {} --config static/js/.jshintrc \;
	@jshint static/js/tests/unit/*.js --config static/js/.jshintrc
	@echo "Running JSHint on javascript...             ${CHECK} Done"
	@recess --compile ${BOOTSTRAP_LESS} > ${BOOTSTRAP}
	@recess --compile ${BOOTSTRAP_RESPONSIVE_LESS} > ${BOOTSTRAP_RESPONSIVE}
	@echo "Compiling LESS with Recess...               ${CHECK} Done"
	@node docs/build
	@cp -r templates/* docs/assets/templates/
	@find docs/assets/templates -iname '*.jinja2' -exec sed -i 's|<link.*href="/static/less/bootstrap.less".*>|<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.css"/>|g' {} \;
	@find docs/assets/templates -iname '*.jinja2' -exec sed -i 's|<script.*src="/static/js/less.js".*</script>||g' {} \;
	@cp -r static/img/* docs/assets/static/img/
	@cp -r static/fonts/* docs/assets/static/fonts/
	@find static/js -iname '*.js' ! -name 'less.js' -exec cp {} docs/assets/static/js/ \;
	@cp static/js/tests/vendor/jquery.js docs/assets/static/js/
	@echo "Compiling documentation...                  ${CHECK} Done"
	@cat static/js/bootstrap-transition.js static/js/bootstrap-alert.js static/js/bootstrap-button.js static/js/bootstrap-carousel.js static/js/bootstrap-collapse.js static/js/bootstrap-dropdown.js static/js/bootstrap-modal.js static/js/bootstrap-tooltip.js static/js/bootstrap-popover.js static/js/bootstrap-scrollspy.js static/js/bootstrap-tab.js static/js/bootstrap-typeahead.js static/js/bootstrap-affix.js > docs/assets/static/js/bootstrap.js
	@uglifyjs docs/assets/static/js/bootstrap.js -nc > docs/assets/static/js/bootstrap.min.tmp.js
	@echo "/**\n* Bootstrap.js v2.2.2 by @fat & @mdo\n* Copyright 2012 Twitter, Inc.\n* http://www.apache.org/licenses/LICENSE-2.0.txt\n*/" > docs/assets/static/js/copyright.js
	@cat docs/assets/static/js/copyright.js docs/assets/static/js/bootstrap.min.tmp.js > docs/assets/static/js/bootstrap.min.js
	@rm docs/assets/static/js/copyright.js docs/assets/static/js/bootstrap.min.tmp.js
	@echo "Compiling and minifying javascript...       ${CHECK} Done"
	@echo "\n${HR}"
	@echo "Bootstrap successfully built at ${DATE}."
	@echo "${HR}\n"
	@echo "Thanks for using Bootstrap,"
	@echo "<3 @mdo and @fat\n"

#
# RUN JSHINT & QUNIT TESTS IN PHANTOMJS
#

test:
	jshint static/js/*.js --config static/js/.jshintrc
	jshint static/js/tests/unit/*.js --config static/js/.jshintrc
	node static/js/tests/server.js &
	phantomjs static/js/tests/phantom.js "http://localhost:3000/static/js/tests"
	kill -9 `cat static/js/tests/pid.txt`
	rm static/js/tests/pid.txt

#
# CLEANS THE ROOT DIRECTORY OF PRIOR BUILDS
#

clean:
	rm -r bootstrap

#
# BUILD SIMPLE BOOTSTRAP DIRECTORY
# recess & uglifyjs are required
#

bootstrap:
	mkdir -p bootstrap/img
	mkdir -p bootstrap/css
	mkdir -p bootstrap/js
	cp img/* bootstrap/img/
	recess --compile ${BOOTSTRAP_LESS} > bootstrap/css/bootstrap.css
	recess --compress ${BOOTSTRAP_LESS} > bootstrap/css/bootstrap.min.css
	recess --compile ${BOOTSTRAP_RESPONSIVE_LESS} > bootstrap/css/bootstrap-responsive.css
	recess --compress ${BOOTSTRAP_RESPONSIVE_LESS} > bootstrap/css/bootstrap-responsive.min.css
	cat static/js/bootstrap-transition.js static/js/bootstrap-alert.js static/js/bootstrap-button.js static/js/bootstrap-carousel.js static/js/bootstrap-collapse.js static/js/bootstrap-dropdown.js static/js/bootstrap-modal.js static/js/bootstrap-tooltip.js static/js/bootstrap-popover.js static/js/bootstrap-scrollspy.js static/js/bootstrap-tab.js static/js/bootstrap-typeahead.js static/js/bootstrap-affix.js > bootstrap/static/js/bootstrap.js
	uglifyjs bootstrap/static/js/bootstrap.js -nc > bootstrap/static/js/bootstrap.min.tmp.js
	echo "/*!\n* Bootstrap.js by @fat & @mdo\n* Copyright 2012 Twitter, Inc.\n* http://www.apache.org/licenses/LICENSE-2.0.txt\n*/" > bootstrap/static/js/copyright.js
	cat bootstrap/static/js/copyright.js bootstrap/static/js/bootstrap.min.tmp.js > bootstrap/static/js/bootstrap.min.js
	rm bootstrap/static/js/copyright.js bootstrap/static/js/bootstrap.min.tmp.js

#
# MAKE FOR GH-PAGES 4 FAT & MDO ONLY (O_O  )
#

gh-pages: bootstrap docs
	rm -f docs/assets/bootstrap.zip
	zip -r docs/assets/bootstrap.zip bootstrap
	rm -r bootstrap
	rm -f ../bootstrap-gh-pages/assets/bootstrap.zip
	node docs/build production
	cp -r docs/* ../bootstrap-gh-pages

#
# WATCH LESS FILES
#

watch:
	echo "Watching less files..."; \
	watchr -e "watch('less/.*\.less') { system 'make' }"


.PHONY: docs watch gh-pages
