import styles from "./page.module.css";
import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Events | Sepak takraw game',
  description: 'Events in the game',
};

export default function Home() {
  return (
    <>
      <div className="layout centerize">
        <div className={styles.content}>
          <div>
            <div className={styles.title}>
              Events,
            </div>

            <div className={styles.text}>

              <div className={styles.event}>
                <div className="layout">
                  <div>
                    <b>Regu</b>
                  </div>
                  <div className="spacer"></div>
                  <div>
                    <b>3</b> Playing and <b>2</b> Substitutes
                  </div>
                </div>

                <b>Serving</b><br />
                A serving circle is drawn in the middle of each side of court, two quater circles are drawn for each side connecting the middle line and side lines of the court.<br />
                <b>Serving position</b><br />
                The serving player needs to keep his non kicking leg firmly in contact with ground to serve. the non serving/remaining two players will keep both themselves inside the quarter circles. players can relax from circles once the ball crosses the net.
                Serving method, one of the player from quater circle with feed the ball to serving player by throwing enabling the serving player to kick with his serving leg.
                the team can choose a player to serve amoung themselves
                the teams get the serving chance in alternative fashion. <br />
                <b>Substituting rules</b><br />
                A team can have two individual substitutes or can substitute a player and make a re-entry on the same player on each set<br /> <br /> <br />
                <div className="layout centerize">Best of three sets will be declared as win</div>
              </div>
              <div className={styles.event}>
                <div className="layout">
                  <div>
                    <b>Doubles</b>
                  </div>
                  <div className="spacer"></div>
                  <div>
                    <b>2</b> Playing and <b>1</b> Substitutes
                  </div>
                </div>
                <b>Serving</b><br />
                <b>Serving position</b><br />
                The Serving player is out of the playing side of court and non serving player remains at rest(non moving). once the ball crosses the net, serving player can get in and other can relax<br />
                the Serving player, feeds and kicks on his own being out of the playing court of his side.<br />
                each Player in the team gets the chance in alternate fashion<br />
                the teams get the serving chance in alternative<br />
                <b>Substituting rules</b><br />
                A team can have one individual substitutes or can substitute a player and make a re-entry on the same player on each set<br /> <br /> <br />
                <div className="layout centerize">Best of three sets will be declared as win</div>
              </div>
              <div className={styles.event}>
                <div className="layout">
                  <div>
                    <b>Quad</b>
                  </div>
                  <div className="spacer"></div>
                  <div>
                    <b>4</b> Playing and <b>2</b> Substitutes
                  </div>
                </div>
                <b>Serving position</b><br />
                The Serving player is out of the playing side of court and non serving players remain at rest(non moving). once the ball crosses the net, serving player can get in and others can relax<br />
                the Serving player, feeds and kicks on his own being out of the playing court of his side.<br />
                the team can choose a player to serve amoung themselves<br />
                the teams get the serving chance in alternative<br />
                <b>Substituting rules</b><br />
                A team can have two individual substitutes or can substitute a player and make a re-entry on the same player on each set<br /> <br /> <br />
                <div className="layout centerize">Best of three sets will be declared as win</div>
              </div>
              <div className={styles.event}>
                <div className="layout">
                  <div>
                  <b>Team - Regu</b>
                  </div>
                  <div className="spacer"></div>
                  <div>
                    <b>3regu (3*3) 9</b> Players and <b>3</b> Substitutes
                  </div>
                </div>

                <div className="layout centerize">Serving same as regu</div>
                <b>Substituting rules</b><br />
                A team can have two individual substitutes or can substitute a player and make a re-entry on the same player on each set. The played player cannot play on the other regu<br /> <br /> <br />

                <div className="layout centerize">Best of three Regu&apos;s will be declared as win</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}