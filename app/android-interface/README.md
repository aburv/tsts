![Generic badge](https://img.shields.io/badge/Build-PASSED-green.svg)  ![Generic badge](https://img.shields.io/badge/Coverage-100%25-green.svg) ![Generic badge](https://img.shields.io/badge/Android-Kotlin-green.svg)

# Android Interface

   MinSDK : Android API V34

   Kotlin -V2.0.21

   Gradle -V8.11.1

## Development server

### Prerequisites:

* Env configs

Setup the values

```commandline
source envs/android.env
```

or 

In Android Studio on Edit configuration and set env variables and its values

* Place the google-services.json inside app level

* Run to generate keystore

```commandline
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

* Build application

```commandline
./gradlew build
```

or

In Android Studio, Build the App

* Install application

```commandline
adb
```
or

In Android Studio, Run the app


Maintain 0 errors and minimize the warnings as much as possible

## Testing

### Unit Testing

Unit tests are present under test

In Android Studio Run the Test with RunWithCoverage

View Code Coverage in html format

## Happy UI coding