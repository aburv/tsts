'use client'
import "./globals.css";
import styles from "./page.module.css";
import Image from "next/image";

export function Footer() {
  const list1 = [
    {
      url: "/about-game",
      title: "About the Game"
    },
    {
      url: "/game-rules",
      title: "Game Rules"
    },
    {
      url: "/game-events",
      title: "Events"
    },
  ]

  const list2 = [
    {
      url: "/blogs",
      title: "Blogs"
    },
    {
      url: "/newsletters",
      title: "Newsletters"
    },
    {
      url: "/faq",
      title: "FAQ"
    },
    {
      url: "/report",
      title: "Report"
    },
  ]
  const list3 = [
    {
      url: "/terms-conditions",
      title: "Terms & Conditions"
    },
    {
      url: "/privacy-policies",
      title: "Privacy Policies"
    },
    {
      url: "/contact",
      title: "Contact us"
    }
  ]

  const thisYear: number = new Date().getFullYear();

  const isBrowser = () => typeof window !== 'undefined';

  function scrollToTop() {
    if (!isBrowser()) return;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <footer className={styles.footer}>
      <div className={styles.fContainer}>
        <div className={styles.footerInner}>
          <div className={styles.cFooter}>
            <div className="layout" style={{ position: 'relative' }}>
              <Image alt="" style={{ position: 'absolute', bottom: '0px' }} src={`/logo_company.svg`} width="150" height="150" />
              <div className="spacer"></div>
              <div style={{ width: '200px' }}>
                <ul className={styles.ul}>
                  {
                    list1.map((item, index) => (
                      <a key={index} href={item['url']} className={styles.a}> {item['title']}</a>
                    ))
                  }
                </ul>
              </div>
              <div style={{ width: '200px' }}>
                <ul className={styles.ul}>
                  {
                    list2.map((item, index) => (
                      <a key={index} href={item['url']} className={styles.a}> {item['title']}</a>
                    ))
                  }
                </ul>
              </div>
              <div>
                <ul className={styles.ul}>
                  {
                    list3.map((item, index) => (
                      <a key={index} href={item['url']} className={styles.a}> {item['title']}</a>
                    ))
                  }
                </ul>
              </div>
            </div>
            <div className={styles.bottomLine}>
              <div>
                <div className={styles.footerTag}>
                  <p>Powered by Aburv | © {thisYear} Takbuff </p>
                </div>
              </div>
              <div className="spacer"></div>
              <div onClick={() => (scrollToTop())}>
                <svg className={styles.svg} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style={{ position: 'absolute', right: '0px' }}>
                  <path d="M12 2c5.52 0 10 4.48 10 10s-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2zm1 10h3l-4-4-4 4h3v4h2v-4z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export function Header() {
  return (
    <div className={`layout centerize ${styles.header}`}>
      <a href="/"><Image className={styles.appLogo} src={`/logo_takbuff.png`} width="64" height="64" alt="logo" /></a>
    </div>
  )
}

export default function Home() {
  return (
    <>
      <div className={styles.content}>
        <div className={styles.subtitle} style={{ textAlign: "center" }}>
          An Open Source Application <br />
          for <br />
          the <b>Sepak Takraw</b> community
        </div>
      </div>
    </>
  );
}
