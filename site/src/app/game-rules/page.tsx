import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Rules | Sepak takraw game',
  description: 'Rules on the game',
};

export default function Home() {
  return (
    <>
      <div className="layout centerize">
      <div className={styles.content}>
        <div>
          <div className={styles.title}>
            Rules,
          </div>

          <div className={styles.text}>
             2/3/4 playing and 1/2 subsitutes<br /> <br /> <br />

             No Hand touching the ball at any point in time, apart from the time of serving <br /> <br /> <br />

             Upto 3 touch per team on each rally <br /> <br /> <br />

             Can use Legs (especially feet and thighs), chest, head to control the rally <br /> <br /> <br />

             Rolling on the chest on the first recieve on the service in not counted as touch but the same is counted as touch on other rallies <br />  <br />  <br />
          </div>
        </div>
      </div>
      </div>
    </>
  );
}