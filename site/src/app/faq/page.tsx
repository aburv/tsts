import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | FAQ',
  description: 'FAQs on the app usages',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Frequently Asked Questions
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            No FAQs to show
          </div>
        </div>
      </div>
    </>
  );
}