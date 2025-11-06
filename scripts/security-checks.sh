#!/usr/bin/env bash
set -e

ALPINE_VERSION=3.18
ISSUES_REPORT_FILE=server_hawkeye_report.json

sudo apt-get update
sudo apt-get install -y jq curl

docker create -v /target --name target-code alpine:${ALPINE_VERSION} /bin/true
docker cp ./ target-code:/target

docker run --volumes-from target-code --name hawkeye hawkeyesec/scanner-cli:latest scan -f high /target --json ${ISSUES_REPORT_FILE}
hawkeye_return=$?

mkdir -p /tmp/artifacts/
docker cp $(docker ps -alq):/target/${ISSUES_REPORT_FILE} /tmp/artifacts/${ISSUES_REPORT_FILE}

echo "issues_report=${GITHUB_WORKSPACE}/tmp/artifacts/${ISSUES_REPORT_FILE}" >> $GITHUB_ENV

if [ ${hawkeye_return} -eq 0 ]; then
    echo "Security checks passed"
else
    echo "Security checks failed. Report is available on artifacts tab."
fi

exit ${hawkeye_return}
