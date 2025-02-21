import Head from "next/head";
import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Takbuff | Report',
  description: 'App reports',
};

export default function Home() {
  return (
    <>
    <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Report
          </div>

          <div className={`layout centerize ${styles.remheight}`}>
            Updating soon
          </div>
        </div>
      </div>
    </>
  );
}