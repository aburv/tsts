plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt")
}

android {
    namespace = "com.aburv.takbuff"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.aburv.takbuff"
        minSdk = 34
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
    implementation("androidx.core:core-ktx:1.17.0")
    implementation("androidx.appcompat:appcompat:1.7.1")
    implementation("com.google.android.material:material:1.13.0")
    implementation("androidx.constraintlayout:constraintlayout:2.2.1")

    implementation("androidx.room:room-runtime:2.8.0")
    testImplementation("androidx.test:core:1.7.0")
    kapt("androidx.room:room-compiler:2.8.0")
    implementation("androidx.room:room-ktx:2.8.0")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")

    implementation("androidx.credentials:credentials:1.5.0")
    implementation("androidx.credentials:credentials-play-services-auth:1.5.0")
    implementation("com.google.android.libraries.identity.googleid:googleid:1.1.1")
    implementation("com.google.android.gms:play-services-identity:18.1.0")

    implementation("androidx.test.ext:junit-ktx:1.3.0")
    implementation("androidx.test.espresso:espresso-idling-resource:3.7.0")

    testImplementation("junit:junit:4.13.2")

    testImplementation("org.mockito:mockito-core:5.20.0")
    testImplementation("org.mockito.kotlin:mockito-kotlin:6.0.0")
    testImplementation("org.mockito:mockito-inline:5.2.0")

    testImplementation("org.robolectric:robolectric:4.16")
    testImplementation("androidx.test:core:1.7.0")

    androidTestImplementation("androidx.test.ext:junit:1.3.0")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.7.0")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:3.7.0")
    androidTestImplementation("androidx.test.espresso:espresso-intents:3.7.0")
    androidTestImplementation("androidx.test.espresso:espresso-idling-resource:3.7.0")
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
