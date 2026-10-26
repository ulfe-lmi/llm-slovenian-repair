#!/usr/bin/env bash
# Install the pinned Pandoc 3.7.0.2 (linux-amd64) into an owned prefix.
#
# Order 013-a: the runnable proxy requires the exact pinned Pandoc for
# structural original-span protection.  This script downloads the upstream
# release archive, verifies its byte size and SHA-256, and installs the
# static binary into an owned directory.  No sudo, no system packages, no
# writes outside the prefix.  The dependency record and its checksum notes
# live in pandoc-dependency.json.
set -eu

VERSION="3.7.0.2"
ARCH="amd64"
ARCHIVE="pandoc-${VERSION}-linux-${ARCH}.tar.gz"
URL="https://github.com/jgm/pandoc/releases/download/${VERSION}/${ARCHIVE}"
EXPECTED_BYTES=33678610
EXPECTED_SHA256="8f8f67fdd540b6519326b0ac49d5c55c5d5d15e43920e80a086e02c8aff83268"

PREFIX="${1:-${HOME}/.local/share/concept-verification/pandoc-${VERSION}}"
case "$PREFIX" in
    /*) ;;
    *) echo "prefix must be an absolute path: $PREFIX" >&2; exit 1 ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

echo "fetching ${URL}" >&2
curl -fSL --max-time 300 -o "${tmp}/${ARCHIVE}" "$URL"

actual_bytes="$(wc -c < "${tmp}/${ARCHIVE}")"
if [ "$actual_bytes" -ne "$EXPECTED_BYTES" ]; then
    echo "archive byte size mismatch: expected ${EXPECTED_BYTES}, got ${actual_bytes}" >&2
    exit 1
fi
actual_sha256="$(sha256sum "${tmp}/${ARCHIVE}" | cut -d' ' -f1)"
if [ "$actual_sha256" != "$EXPECTED_SHA256" ]; then
    echo "archive sha256 mismatch: expected ${EXPECTED_SHA256}, got ${actual_sha256}" >&2
    exit 1
fi

tar -xzf "${tmp}/${ARCHIVE}" -C "$tmp"
mkdir -p "${PREFIX}/bin"
install -m 0755 "${tmp}/pandoc-${VERSION}/bin/pandoc" "${PREFIX}/bin/pandoc"

actual_version="$("${PREFIX}/bin/pandoc" --version | head -n 1)"
expected_version="pandoc ${VERSION}"
if [ "$actual_version" != "$expected_version" ]; then
    echo "version mismatch: expected '${expected_version}', got '${actual_version}'" >&2
    exit 1
fi
echo "installed pandoc ${VERSION} at ${PREFIX}/bin/pandoc" >&2
