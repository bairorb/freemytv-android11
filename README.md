# Free My TV — TCL G07 (Android 11)

Experimental Android 11 port of [Free My TV](https://github.com/simbasjungles/free-my-tv).

**Intended device:** TCL G07, Realtek RTD2851A, Android 11 (API 30), `armeabi-v7a`.

The workflow downloads Free My TV's upstream sources at build time and changes the minimum Android API from 31 to 30. This alone **does not guarantee runtime compatibility**. Review the build logs and do not disable the stock launcher until the APK has been tested.

## Build / download
Open **Actions → Free My TV Android 11 — TCL G07**. The workflow automatically starts after the workflow file is committed; you can also select **Run workflow**.

On successful build download the artifact **FreeMyTV-Android11-TCL-G07-EXPERIMENTAL** (ZIP) and extract the APK.

Use **atvTools → Apps → Install APK** to install it. Open Free My TV's settings and test it before enabling the replacement home screen.

## Rollback
If you have not yet enabled Free My TV's mode, uninstalling the app restores the prior state. If you have enabled its home-screen mode, follow the upstream project's restoration instructions first; ADB on your TV can restore the stock HOME app `com.google.android.apps.tv.launcherx`.

**Warnings:** This build uses a debug-style self-generated signing key. Do not assume it is suitable for secure software distribution. A different workflow run may create a different key; future updates may require uninstalling the previous APK, losing its app settings.

Upstream license: MIT. This repository does not distribute or endorse Free My TV.
