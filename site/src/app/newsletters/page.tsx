import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Newsletters',
  description: 'Newsletters on the app updates and usages',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Newsletters
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            Nothing to show
          </div>
        </div>
      </div>
    </>
  );
}