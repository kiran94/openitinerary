#!/usr/bin/env bash

set -euo pipefail

VERSION=$(uv version --short)
PUBLISH=false

if [[ ! "${VERSION}" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$ ]]; then
  echo "::error::Project version '${VERSION}' is not a valid container tag."
  exit 1
fi

if [[ "${EVENT_NAME}" == "push" ]]; then
  # Check if the version has changed.
  PREVIOUS_VERSION=$(
    git show "${BEFORE_SHA}:pyproject.toml" |
      sed -n '/^\[project\]/,/^\[/s/^version = "\([^"]*\)"/\1/p'
  )

  if [[ "${VERSION}" != "${PREVIOUS_VERSION}" ]]; then
    PUBLISH=true
  fi
elif [[ "${EVENT_NAME}" == "workflow_dispatch" && "${REF}" == "refs/heads/main" ]]; then
  # A manual run on main can retry publishing the current project version.
  PUBLISH=true
fi

echo "version=${VERSION}" >> "${GITHUB_OUTPUT}"
echo "publish=${PUBLISH}" >> "${GITHUB_OUTPUT}"
