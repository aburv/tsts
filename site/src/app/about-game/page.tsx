import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: 'About | Sepak takraw game',
  description: 'History of the game',
};

export default function Home() {
  return (
    <>
      <div className="layout centerize">
        <div className={styles.content}>
          <div>
            <div className={styles.title}>
              About the game,
            </div>

            <div className={styles.text}>

              <div className="layout">
                <div className={styles.half}>
                  Sepak takraw is a team sport. The word sepak is Malay (Jawi: سيڨق) for kick while the word takraw is of Thai (Thai: ตะกร้อ) origin. It is played with a ball made of synthetic plastic between two teams of 2/3/4 players on a court with a net separting two creating a rally between them. It is similar to volleyball and footvolley, players using only their feet, knees, shoulders, chest and head to play with the ball.
                </div>
                <div className="spacer"></div>
                <Image src={'/logo_takbuff.png'} width="200" height="200" alt="image" />
              </div>
              <div>
                Sepak takraw resembles native sports known as <b>Sepak Raga</b> in Brunei, Indonesia, Malaysia, and Singapore Takraw and <b>Rago/Raga</b> in Indonesia, <b>Sipa</b> in Philippines, <b>Chinlone</b> in Myanmar; <b>Takraw</b> in Thailand; <b>Kataw</b> in Laos; and <b>Sek Dai</b> in Cambodia. It is also claimed to be related to <b>Cuju</b> in China, <b>Cau May</b> in Vietnam, <b>Jegichagi</b> in Korea and <b>Kemari</b> in Japan.
              </div>
              <br />
              <br />
              <div>
                The sport&rsquo;s modern version was introduced, developed and standardized in 1960 when officials from Malaysia, Singapore, Thailand and Myanmar met in Kuala Lumpur to agree on a name and standard rules for it. It was previously known as Sepak Raga Jaring, and was first exhibited in Penang in 1945. It was introduced in the 1965 Southeast Asian Games in Kuala Lumpur as a medal event. Sepak Takraw is considered Malaysia&rsquo;s national sport.
              </div>
              <br />
              <br />
              <div>
                International Sepaktakraw Federation (ISTAF), formed in 1988, governes internationally engaements like ISTAF SuperSeries (ISS) and ISTAF World Cup (IWC), Malaysia&rsquo;s Khir Johari Cup, and Thailand&rsquo;s King Cup.
              </div>
              <div>
                Tournaments please look at the tournament section of the app
              </div>
              <br />  <br />  <br />
              Other names buka ball, kick volleyball or foot volleyball <br />  <br />  <br />
              The ball once made of rattan  <br />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}