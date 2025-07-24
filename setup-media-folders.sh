#!/usr/bin/env bash
# create_media_tree.sh
# Creates the /data media/torrents/usenet folder hierarchy **and** sets
# ownership/permissions so that *any* service account you add to the
# "media" group can read & write the files.  Run it once and everything
# below /data will be ready for Plex, Sonarr, Radarr, etc.
#
# ▸ If you are not root the script transparently re‑executes itself with sudo.
# ▸ A system group called "media" is created if it doesn’t already exist.
# ▸ All directories are owned by root:media and are 775 (rwx rwx r‑x).
# ▸ The set‑gid bit (g+s) is applied so new files inherit the group.

set -euo pipefail

# ── Elevate to root if needed ────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
  echo "[create_media_tree] Need root privileges → re‑executing with sudo…"
  exec sudo "$0" "$@"
fi

BASE="/data"
MEDIA_GRP="media"   # Change this if you prefer a different group name
PERMS="775"          # Directory & file permissions (default: rwxrwxr‑x)

# ── Ensure the media group exists ────────────────────────────────────────────
if ! getent group "${MEDIA_GRP}" >/dev/null; then
  echo "[create_media_tree] Creating system group '${MEDIA_GRP}'…"
  groupadd --system "${MEDIA_GRP}"
fi

# ── All sub‑directories relative to $BASE ────────────────────────────────────
DIRS=(
  "media/books"
  "media/movies"
  "media/music"
  "media/tv"

  "torrents/books"
  "torrents/movies"
  "torrents/music"
  "torrents/tv"

  "usenet/complete/books"
  "usenet/complete/movies"
  "usenet/complete/music"
  "usenet/complete/tv"
  "usenet/incomplete"
)

# ── Create the directory tree ───────────────────────────────────────────────
for d in "${DIRS[@]}"; do
  mkdir -p "${BASE}/${d}"
done

echo "[create_media_tree] Directory tree created under ${BASE}"  

# ── Set ownership and permissions ───────────────────────────────────────────
chown -R root:"${MEDIA_GRP}" "${BASE}"
chmod -R "${PERMS}" "${BASE}"
# Ensure new sub‑files/dirs inherit the group
find "${BASE}" -type d -exec chmod g+s {} +

echo "[create_media_tree] Applied permissions ${PERMS} and setgid to all."  

echo -e "\n✔ Setup complete!  Add service accounts to the '${MEDIA_GRP}' group, e.g.:\n  sudo usermod -aG ${MEDIA_GRP} plex\n  sudo usermod -aG ${MEDIA_GRP} sonarr"
