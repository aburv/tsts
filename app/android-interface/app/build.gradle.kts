plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt")
}

android {
    namespace = "com.aburv.takbuff"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.aburv.takbuff"
        minSdk = 34
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        debug {
            buildConfigField(
                "String", "API_DOMAIN",
                "\"${System.getenv("API_DOMAIN")}\""
            )

            buildConfigField(
                "String", "API_KEY",
                "\"${System.getenv("API_KEY")}\""
            )

            buildConfigField(
                "String", "BASE_NAME",
                "\"${System.getenv("DB")}\""
            )

            buildConfigField(
                "String", "G_CLIENT_ID",
                "\"${System.getenv("G_CLIENT_ID")}\""
            )

            buildConfigField(
                "String", "SEPARATOR",
                "\"${System.getenv("SEPARATOR")}\""
            )
        }
        release {
            buildConfigField(
                "String", "API_DOMAIN",
                "\"${System.getenv("API_DOMAIN")}\""
            )

            buildConfigField(
                "String", "API_KEY",
                "\"${System.getenv("API_KEY")}\""
            )

            buildConfigField(
                "String", "BASE_NAME",
                "\"${System.getenv("DB")}\""
            )

            buildConfigField(
                "String", "G_CLIENT_ID",
                "\"${System.getenv("G_CLIENT_ID")}\""
            )

            buildConfigField(
                "String", "SEPARATOR",
                "\"${System.getenv("SEPARATOR")}\""
            )

            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        viewBinding = true
        buildConfig = true
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.2.1")

    implementation("androidx.room:room-runtime:2.7.0")
    testImplementation("androidx.test:core:1.6.1")
    kapt("androidx.room:room-compiler:2.7.0")
    implementation("androidx.room:room-ktx:2.7.0")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    implementation("androidx.credentials:credentials:1.5.0")
    implementation("androidx.credentials:credentials-play-services-auth:1.5.0")
    implementation("com.google.android.libraries.identity.googleid:googleid:1.1.1")
    implementation("com.google.android.gms:play-services-identity:18.1.0")

    implementation("androidx.test.ext:junit-ktx:1.2.1")
    implementation("androidx.test.espresso:espresso-idling-resource:3.6.1")

    testImplementation("junit:junit:4.13.2")

    testImplementation("org.mockito:mockito-core:4.8.0")
    testImplementation("org.mockito.kotlin:mockito-kotlin:4.0.0")
    testImplementation("org.mockito:mockito-inline:4.8.0")

    testImplementation("org.robolectric:robolectric:4.9")
    testImplementation("androidx.test:core:1.6.1")

    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.6.1")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.6.1")
    androidTestImplementation("androidx.test.espresso:espresso-idling-resource:3.6.1")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
