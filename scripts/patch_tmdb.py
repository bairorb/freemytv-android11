#!/usr/bin/env python3
"""Patch the upstream Android 11 build to accept a private TMDB key from atvTools.

The key is sent directly to the TV via an explicit SettingsActivity intent and
stored in app-private SharedPreferences. No API key enters this public repo.
"""
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    hits = text.count(old)
    if hits != 1:
        raise SystemExit(f"Upstream changed; expected one match, got {hits}: {old[:90]!r}")
    return text.replace(old, new)


p = Path("free-my-tv/app/src/io/freemytv/Recs.java")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    """    static boolean hasKey(Context c) {
        return !Config.TMDB_KEY.trim().isEmpty();
    }""",
    """    /** Private API key set locally via atvTools, or the compiled-in fallback. */
    private static String tmdbKey(Context c) {
        String key = c.getSharedPreferences("tmdb_config", Context.MODE_PRIVATE)
                .getString("key", "");
        return key.trim().isEmpty() ? Config.TMDB_KEY.trim() : key.trim();
    }

    static boolean hasKey(Context c) {
        return !tmdbKey(c).isEmpty();
    }""",
)
s = replace_once(
    s,
    "long stamp = Config.TMDB_KEY.hashCode() * 31L + REGION.hashCode();",
    "long stamp = tmdbKey(context).hashCode() * 31L + REGION.hashCode();",
)
s = replace_once(
    s, "String key = Config.TMDB_KEY.trim();",
    "String key = tmdbKey(context);",
)
p.write_text(s, encoding="utf-8")

p = Path("free-my-tv/app/src/io/freemytv/SettingsActivity.java")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    """        Ui.init(this);
        view = new SettingsView(this);""",
    """        Ui.init(this);
        saveTmdbKeyFromIntent(getIntent());
        view = new SettingsView(this);""",
)
s = replace_once(
    s,
    """        setIntent(intent);
    }

    @Override protected void onPause()""",
    """        setIntent(intent);
        saveTmdbKeyFromIntent(intent);
    }

    @Override protected void onPause()""",
)
s = replace_once(
    s,
    "    @Override protected void onResume() {",
    """    /** Receive the user's TMDB key from atvTools; do not send it to GitHub.
     *  adb shell am start -n io.freemytv/.SettingsActivity --es tmdb_api_key KEY
     */
    private void saveTmdbKeyFromIntent(Intent intent) {
        if (intent == null || !intent.hasExtra("tmdb_api_key")) return;
        String key = intent.getStringExtra("tmdb_api_key");
        intent.removeExtra("tmdb_api_key");
        if (key == null || !key.trim().matches("[A-Za-z0-9._-]{20,1024}")) {
            AppLog.w("TMDB key was rejected: invalid format");
            return;
        }
        getSharedPreferences("tmdb_config", MODE_PRIVATE)
                .edit().putString("key", key.trim()).commit();
        AppLog.w("TMDB key saved locally");
        Recs.get(this).refreshIfStale();
    }

    @Override protected void onResume() {""",
)
p.write_text(s, encoding="utf-8")
print("Patched TMDB key support.")
