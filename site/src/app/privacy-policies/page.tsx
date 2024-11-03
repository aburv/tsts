import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Privacy Policies',
  description: 'App user\'s privarcy policies on the app services and engagements',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Privacy Policies
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            Updating soon
          </div>
        </div>
      </div>
    </>
  );
}