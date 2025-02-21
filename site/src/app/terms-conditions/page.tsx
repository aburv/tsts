import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Terms and Conditions',
  description: 'Terms and condition for the app users',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Terms and Conditions
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            Updating soon
          </div>
        </div>
      </div>
    </>
  );
}