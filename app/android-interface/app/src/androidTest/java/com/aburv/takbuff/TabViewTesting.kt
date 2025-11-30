package com.aburv.takbuff

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.widget.LinearLayout
import android.widget.TextView
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.viewpager.widget.ViewPager
import com.aburv.takbuff.customViews.TabBarView
import junit.framework.TestCase.assertEquals
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class TabBarViewTest {

    private lateinit var context: Context
    private lateinit var tabBarView: TabBarView
    private lateinit var viewPager: ViewPager

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
        tabBarView = TabBarView(context, null)

        viewPager = ViewPager(context)

        tabBarView.attachTo(viewPager)
    }

    @Test
    fun testTabsInitialization() {
        val titles = listOf("Tab 1", "Tab 2", "Tab 3")
        tabBarView.setTitles(titles)

        val tabs = tabBarView.findViewById<LinearLayout>(R.id.view_tabs_wrapper).childCount
        assertEquals(titles.size, tabs)

        val firstTab =
            tabBarView.findViewById<LinearLayout>(R.id.view_tabs_wrapper).getChildAt(0) as TextView
        assertEquals("Tab 1", firstTab.text)
        assertEquals(42f, firstTab.textSize) 
    }

    @Test
    fun testTabSelection() {
        val titles = listOf("Tab 1", "Tab 2", "Tab 3")
        tabBarView.setTitles(titles)

        val secondTab =
            tabBarView.findViewById<LinearLayout>(R.id.view_tabs_wrapper).getChildAt(1) as TextView
        secondTab.performClick()

        assertEquals(42f, secondTab.textSize)
        assertEquals(tabBarView.bright, secondTab.currentTextColor)

        val firstTab =
            tabBarView.findViewById<LinearLayout>(R.id.view_tabs_wrapper).getChildAt(0) as TextView
        assertEquals(36.75f, firstTab.textSize)
        assertEquals(tabBarView.dark, firstTab.currentTextColor)
    }

    @Test
    fun testTabBarWithViewPager() {
        val titles = listOf("Tab 1", "Tab 2", "Tab 3")
        tabBarView.setTitles(titles)

        val secondTab =
            tabBarView.findViewById<LinearLayout>(R.id.view_tabs_wrapper).getChildAt(1) as TextView
        secondTab.performClick()


        Handler(Looper.getMainLooper()).postDelayed({
            assertEquals(1, viewPager.currentItem)
        }, 1000)
    }
}
