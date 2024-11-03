import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Blogs',
  description: 'Blogs about the app',
};

export default function Home() {
  return (
    <>
      <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Blogs
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            No blogs to show
          </div>
        </div>
      </div>
    </>
  );
}