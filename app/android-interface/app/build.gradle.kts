import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("com.android.application")
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.aburv.takbuff"
    compileSdk = 37

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
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }
    buildFeatures {
        viewBinding = true
        buildConfig = true
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_21)
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.constraintlayout)

    implementation(libs.androidx.room.runtime)
    testImplementation(libs.androidx.core)
    ksp(libs.androidx.room.compiler)
    implementation(libs.androidx.room.ktx)

    implementation(libs.kotlinx.coroutines.android)

    implementation(libs.androidx.credentials)
    implementation(libs.androidx.credentials.play.services.auth)
    implementation(libs.googleid)
    implementation(libs.play.services.identity)

    implementation(libs.androidx.junit.ktx)
    implementation(libs.androidx.espresso.idling.resource)

    testImplementation(libs.junit)

    testImplementation(libs.mockito.core)
    testImplementation(libs.mockito.kotlin)
    testImplementation(libs.mockito.inline)

    testImplementation(libs.robolectric)

    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.espresso.contrib)
    androidTestImplementation(libs.androidx.espresso.intents)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
