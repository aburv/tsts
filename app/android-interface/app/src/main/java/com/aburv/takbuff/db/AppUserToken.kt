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
import androidx.room.Update
import com.aburv.takbuff.BuildConfig

@Entity(tableName = "token")
data class AppUserToken(
    @PrimaryKey val isActive: Boolean,
    val accessToken: String,
    val idToken: String,
)

@Dao
interface UserTokenDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUserToken(token: AppUserToken)

    @Query("SELECT * FROM token WHERE isActive=true")
    suspend fun getUserToken(): List<AppUserToken>

    @Update
    suspend fun updateUserToken(token: AppUserToken): Int

    @Query("DELETE FROM token")
    suspend fun deleteAll()
}

@Database(entities = [AppUserToken::class], version = 1)
abstract class AppUserTokenData : RoomDatabase() {
    abstract fun userTokenDao(): UserTokenDao
}

class UserTokenDB(context: Context) {

    private val connection = databaseBuilder(
        context,
        AppUserTokenData::class.java,
        BuildConfig.BASE_NAME + "+_1"
    ).build()

    suspend fun getUserToken(): List<AppUserToken> = connection.userTokenDao().getUserToken()

    suspend fun insertUserToken(userToken: AppUserToken) =
        connection.userTokenDao().insertUserToken(userToken)

    suspend fun updateUserToken(userToken: AppUserToken) =
        connection.userTokenDao().updateUserToken(userToken)

    suspend fun deleteAll() = connection.userTokenDao().deleteAll()
}