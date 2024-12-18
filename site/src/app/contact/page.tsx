import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Contact us',
  description: 'Deliver a note to Takbuff team',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Contact us
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            Your feedback matter to us
          </div>
        </div>
      </div>
    </>
  );
}