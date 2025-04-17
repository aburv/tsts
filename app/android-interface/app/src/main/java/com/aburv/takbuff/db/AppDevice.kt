package com.aburv.takbuff.db

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import androidx.room.Room.databaseBuilder
import androidx.room.RoomDatabase
import com.aburv.takbuff.BuildConfig

@Entity(tableName = "device")
data class AppDevice(
    @PrimaryKey val isActive: Boolean,
    val appDeviceId: String
)

@Dao
interface DeviceDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDevice(userDevice: AppDevice)

    @Query("SELECT * FROM device WHERE isActive=true")
    suspend fun getDevices(): List<AppDevice>
}

@Database(entities = [AppDevice::class], version = 1)
abstract class AppDeviceData : RoomDatabase() {
    abstract fun deviceDao(): DeviceDao
}

class DeviceDB(context: Context) {

    private val connection = databaseBuilder(
        context,
        AppDeviceData::class.java,
        BuildConfig.BASE_NAME
    )
        .build()

    suspend fun getDevices(): List<AppDevice> = connection.deviceDao().getDevices()

    suspend fun insertDevice(device: AppDevice) = connection.deviceDao().insertDevice(device)
}