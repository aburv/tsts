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
data class AppUserDevice(
    @PrimaryKey val appDeviceId: String,
    val isActive: Boolean,
    val id: String?,
    val email: String?,
    val dp: String?,
    val name: String?,
)

@Dao
interface DeviceDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertDevice(userDevice: AppUserDevice)

    @Query("SELECT * FROM device WHERE isActive=true")
    suspend fun getDevices(): List<AppUserDevice>
}

@Database(entities = [AppUserDevice::class], version = 1)
abstract class AppDeviceData : RoomDatabase() {
    abstract fun deviceDao(): DeviceDao
}

class DeviceDB(context: Context) {

    private val connection = databaseBuilder(
        context,
        AppDeviceData::class.java,
        BuildConfig.BASE_NAME
    ).build()

    suspend fun getDevices(): List<AppUserDevice> = connection.deviceDao().getDevices()

    suspend fun insertDevice(device: AppUserDevice) = connection.deviceDao().insertDevice(device)
}
