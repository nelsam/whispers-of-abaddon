#!/bin/bash

# Cache current directory
DIR=$( pwd )
FRONTEND_DIR='view'

python=$( which python2.7 )
found=$?

if [[ $found != 0 ]]
then
    python=$( which python2 )
    found=$?
fi

if [[ $found != 0 ]]
then
    python=$( which python )
    found=$?
fi

appcfg="${DIR}/../google_appengine/appcfg.py"
if [[ ! -e $appcfg ]]
then
    appcfg=$( which appcfg.py )
fi

yes_matches=( y yes Y YES Yes )
no_matches=( n no N NO No )
all_matches=( a all A ALL All )

function static_todev {
    echo "Setting dev environment"
    failonerror "rm -f static"
    failonerror "ln -s ${FRONTEND_DIR} static"
}

function static_toprod {
    build

    echo "Setting prod environment"
    failonerror "rm -f static"
    failonerror "ln -s ${FRONTEND_DIR}/publish static"

    upload="y"
    if [[ "$confirmation" != 'a' ]]
    then
        echo "Upload to App Engine?"
        upload=$(checkyesno)
    fi

    if [[ $(contains "${yes_matches[@]}" "$upload") == 'y' ]]
    then
        failonerror "$python $appcfg update \"$DIR\""
    fi
}

function dartc {
    failonerror "oldDir=\"$(pwd)\""

    echo "Running dart2js --checked against all dart files in $(pwd) "\
"and exporting to .dart.js files"

    failonerror "cd ${FRONTEND_DIR}/dart"
    failonerror "find -iname '*.dart' -exec dart2js --checked --out=\"{}.js\" \"{}\" \;"

    failonerror "cd \"$oldDir\""
}

function build {
    failonerror "find -name \"*.pyc\" -delete"
    failonerror "ant"

    echo "Converting references to .dart files to .dart.js"
    failonerror "cd ${FRONTEND_DIR}/publish/templates"
    failonerror "find -iname '*.html' -exec sed -i 's|application/dart|text/javascript|g' {} \;"
    failonerror "find -iname '*.html' -exec sed -i 's|\.dart|.dart.js|g' {} \;"
    failonerror "find -iname '*.html' -exec sed -i 's|^.*/js/dart\.js.*$||g' {} \;"

    failonerror "cd \"$DIR\""
}

function checkyesno {

    readvalue=""
    while [[ ! ($(contains "${yes_matches[@]}" "$readvalue") == 'y' ||
                $(contains "${no_matches[@]}" "$readvalue") == 'y') ]]
    do
        read -p "[Y]es, [N]o: " readvalue
    done

    echo $(contains "${yes_matches[@]}" "$readvalue")
    return 0
}

function checkyesnoall {

    readvalue=""
    while [[ ! ($(contains "${yes_matches[@]}" "$readvalue") == 'y' ||
                $(contains "${no_matches[@]}" "$readvalue") == 'y' ||
                $(contains "${all_matches[@]}" "$readvalue") == 'y') ]]
    do
        read -p "[Y]es, [N]o, Yes to [A]ll: " readvalue
    done

    if [[ $(contains "${yes_matches[@]}" "$readvalue") == 'y' ]]
    then
        echo 'y'
    elif [[ $(contains "${all_matches[@]}" "$readvalue") == 'y' ]]
    then
        echo 'a'
    else
        echo 'n'
    fi
    return 0
}

function failonerror {
    eval "$1"
    response="$?"
    if [[ "$response" -ne 0 ]]
    then
        echo "Command failed: $1"
        exit "$response"
    fi
}

function contains {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            echo "y"
            return 0
        fi
    }
    echo "n"
    return 1
}

echo "Do you want to compile .dart files to .dart.js?"
confirmation=$(checkyesnoall)
yes=""
if [[ "$confirmation" == 'a' ]]
then
    yes='y'
else
    yes="$confirmation"
fi

if [[ "$yes" == 'y' ]]
then
    dartc
fi

if [[ "$confirmation" != 'a' ]]
then
    echo "Do you want to set to production?"
    confirmation=$(checkyesnoall)

    yes=""
    if [[ "$confirmation" == 'a' ]]
    then
        yes='y'
    else
        yes="$confirmation"
    fi
fi

if [[ "$yes" == 'y' ]]
then
    static_toprod
    if [[ "$confirmation" != "a" ]]
    then
        echo "Do you want to set back to dev environment?"
        yes=$(checkyesno)
    fi

    if [[ "$yes" == "y" ]]
    then
        echo
        static_todev
    fi
else
    static_todev
fi
