#!/bin/bash
#
# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

_checkBashReq() {
    log "Komutlar Kontrol Ediliyor ..."
    command -v jq &> /dev/null || quit "Gerekli komut: jq : bulunamadı!"
}

_checkPythonVersion() {
    log "Python Sürümü kontrol ediliyor ..."
    ( test -z $pVer || test $(sed 's/\.//g' <<< $pVer) -lt 380 ) \
        && quit "You MUST have a python version of at least 3.8.0 !"
    log "\tFound PYTHON - v$pVer ..."
}

_checkConfigFile() {
    log "Yapılandırma Dosyası Kontrol Ediliyor ..."
    configPath="config.env"
    if test -f $configPath; then
        log "\tYapılandırma dosyası bulundu : $configPath, Aktarılıyor ..."
        set -a
        . $configPath
        set +a
        test ${_____REMOVE_____THIS_____LINE_____:-fasle} = true \
            && quit "Please remove the line mentioned in the first hashtag from the config.sh file"
    fi
}

_checkRequiredVars() {
    log "Gerekli ENV Dosyası Kontrol Ediliyor ..."
    for var in API_ID API_HASH LOG_CHANNEL_ID DATABASE_URL; do
        test -z ${!var} && quit "Required $var var !"
    done
    [[ -z $HU_STRING_SESSION && -z $BOT_TOKEN ]] && quit "Required HU_STRING_SESSION or BOT_TOKEN var !"
    [[ -n $BOT_TOKEN && -z $OWNER_ID ]] && quit "Required OWNER_ID var !"
    test -z $BOT_TOKEN && log "\t[HINT] >>> BOT_TOKEN not found ! (Disabling Advanced Loggings)"
}

_checkDefaultVars() {
    replyLastMessage "Varsayılan ENV dosyası Kontrol Ediliyor ..."
    declare -rA def_vals=(
        [WORKERS]=0
        [PREFERRED_LANGUAGE]="en"
        [DOWN_PATH]="downloads"
        [UPSTREAM_REMOTE]="upstream"
        [UPSTREAM_REPO]="https://github.com/code-rgb/USERGE-X"
        [LOAD_UNOFFICIAL_PLUGINS]=true
        [G_DRIVE_IS_TD]=true
        [CMD_TRIGGER]="."
        [SUDO_TRIGGER]="!"
        [FINISHED_PROGRESS_STR]="█"
        [UNFINISHED_PROGRESS_STR]="░"
    )
    for key in ${!def_vals[@]}; do
        set -a
        test -z ${!key} && eval $key=${def_vals[$key]}
        set +a
    done
    DOWN_PATH=${DOWN_PATH%/}/
    [[ -n $HEROKU_API_KEY && -n $HEROKU_APP_NAME ]] \
        && declare -gx HEROKU_GIT_URL="https://api:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git"
    for var in G_DRIVE_IS_TD LOAD_UNOFFICIAL_PLUGINS; do
        eval $var=$(tr "[:upper:]" "[:lower:]" <<< ${!var})
    done
    local nameAndUName=$(grep -oP "(?<=\/\/)(.+)(?=\@)" <<< $DATABASE_URL)
    DATABASE_URL=$(sed 's/$nameAndUName/$(printf "%q\n" $nameAndUName)/' <<< $DATABASE_URL)
}

_checkDatabase() {
    editLastMessage "DATABASE_URL kontrol ediliyor ..."
    local err=$(runPythonCode '
import pymongo
try:
    pymongo.MongoClient("'$DATABASE_URL'").list_database_names()
except Exception as e:
    print(e)')
    [[ $err ]] && quit "pymongo response > $err" || log "\tpymongo response > {status : 200}"
}

_checkTriggers() {
    editLastMessage "KOMUTLAR kontrol ediliyor ..."
    test $CMD_TRIGGER = $SUDO_TRIGGER \
        && quit "Invalid SUDO_TRIGGER!, You can't use $CMD_TRIGGER as SUDO_TRIGGER"
}

_checkPaths() {
    editLastMessage ""Dizinler Kontrol Ediliyor ...""
    for path in $DOWN_PATH logs bin; do
        test ! -d $path && {
            log "\tCreating Path : ${path%/} ..."
            mkdir -p $path
        }
    done
}

_checkBins() {
    editLastMessage "BINS kontrol ediliyor ..."
    declare -rA bins=(
        [bin/megadown]="https://raw.githubusercontent.com/yshalsager/megadown/master/megadown"
        [bin/cmrudl]="https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py"
    )
    for bin in ${!bins[@]}; do
        test ! -f $bin && {
            log "\tİndiriliyor $bin ..."
            curl -so $bin ${bins[$bin]}
        }
    done
}

_checkGit() {
    editLastMessage "GIT kontrol ediliyor ..."
    if test ! -d .git; then
        if test ! -z $HEROKU_GIT_URL; then
            replyLastMessage "\tHeroku Git klonlanıyor "
            gitClone $HEROKU_GIT_URL tmp_git || quit "Invalid HEROKU_API_KEY or HEROKU_APP_NAME var !"
            mv tmp_git/.git .
            rm -rf tmp_git
        else
            replyLastMessage "\tBoş Git Başlatılıyor  ..."
            gitInit
        fi
        deleteLastMessage
    fi
}

_checkUpstreamRepo() {
    editLastMessage "UPSTREAM_REPO kontrol ediliyor ..."
    grep -q $UPSTREAM_REMOTE < <(git remote) || addUpstream
    replyLastMessage "\tFetching Data From UPSTREAM_REPO ..."
    fetchUpstream || updateUpstream && fetchUpstream || quit "Invalid UPSTREAM_REPO var !"
    deleteLastMessage
}

_checkUnoffPlugins() {
    editLastMessage "Userge-X [Ekstra] Eklentileri kontrol ediliyor ..."
    if test $LOAD_UNOFFICIAL_PLUGINS = true; then
        editLastMessage "\tUserge-X [Ekstra] Eklentileri Yükleniyor..."
        replyLastMessage "\t\tKlonlanıyor ..."
        gitClone --depth=1 https://github.com/code-rgb/Userge-Plugins.git
        editLastMessage "\t\tPIP sürümü yükseltiliyor..."
        upgradePip
        editLastMessage "\t\tGerkli bağımlılıklar yükleniyor ..."
        installReq Userge-Plugins
        editLastMessage "\t\tArda kalanlar temizleniyor ..."
        rm -rf userge/plugins/unofficial/
        mv Userge-Plugins/plugins/ userge/plugins/unofficial/
        cp -r Userge-Plugins/resources/* resources/
        rm -rf Userge-Plugins/
        deleteLastMessage
        editLastMessage "\tUserge-X [Ekstra] Eklentiler Başarıyla Yüklendi!"
    else
        editLastMessage "\tUserge-X [Ekstra] Eklentiler Devre Dışı!"
    fi
    sleep 1
    deleteLastMessage
}

assertPrerequisites() {
    _checkBashReq
    _checkPythonVersion
    _checkConfigFile
    _checkRequiredVars
}

assertEnvironment() {
    _checkDefaultVars
    _checkDatabase
    _checkTriggers
    _checkPaths
    _checkBins
    _checkGit
    _checkUpstreamRepo
    _checkUnoffPlugins
}