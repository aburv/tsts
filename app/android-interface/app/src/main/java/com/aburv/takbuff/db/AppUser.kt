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

@Entity(tableName = "user")
data class AppUser(
    @PrimaryKey val isActive: Boolean,
    val id: String,
    val email: String,
    val dp: String,
    val name: String
)

@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: AppUser)

    @Query("SELECT * FROM user WHERE isActive=true")
    suspend fun getUsers(): List<AppUser>

    @Query("DELETE FROM user")
    suspend fun deleteAll()
}

@Database(entities = [AppUser::class], version = 1)
abstract class AppUserData : RoomDatabase() {
    abstract fun userDao(): UserDao
}

class UserDB(context: Context) {

    private val connection = databaseBuilder(
        context,
        AppUserData::class.java,
        BuildConfig.BASE_NAME + "_2"
    ).build()

    suspend fun getUsers(): List<AppUser> = connection.userDao().getUsers()

    suspend fun insertUser(user: AppUser) = connection.userDao().insertUser(user)

    suspend fun deleteAll() = connection.userDao().deleteAll()
}