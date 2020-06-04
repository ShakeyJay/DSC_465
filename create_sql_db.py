import sqlite3
import csv

conn = sqlite3.connect('dsc465.db')  # open the connection
cursor = conn.cursor()


def create_tables():
    players_table = """
        CREATE TABLE IF NOT EXISTS players (
            id NUMBER(7),
            first_name VARCHAR(25),
            last_name VARCHAR(25),

            CONSTRAINT players_pk
                PRIMARY KEY(id)
        )
    """

    atbats_table = """
        CREATE TABLE IF NOT EXISTS atbats (
            ab_id NUMBER(20),
            batter_id NUMBER(7),
            event VARCHAR(15),
            pitcher_id NUMBER(7),

            CONSTRAINT atbat_pk
                PRIMARY KEY(ab_id),

            CONSTRAINT atbat_bat_fk
                FOREIGN KEY(batter_id)
                REFERENCES players(id),

            CONSTRAINT atbat_pitch_fk
                FOREIGN KEY(pitcher_id)
                REFERENCES players(id)
        )
    """

    pitches_table = """
        CREATE TABLE IF NOT EXISTS pitches (
            ab_id NUMBER(20),
            px DECIMAL(5,2),
            pz DECIMAL(5,2),
            zone NUMBER(2),
            code VARCHAR(1),
            type VARCHAR(1),
            pitch_type VARCHAR(2),
            b_count NUMBER(1),
            s_count NUMBER(1),


            CONSTRAINT pitches_fk
                FOREIGN KEY(ab_id)
                REFERENCES atbats(ab_id)
        )
    """

    cursor.execute(players_table)
    cursor.execute(atbats_table)
    cursor.execute(pitches_table)
    conn.commit()


def insert_players():
    with open('mlb_pitch_data/player_names.csv') as players:
        csv_reader = csv.reader(players)
        for player in csv_reader:
            insert_player = """INSERT OR IGNORE INTO players VALUES(?,?,?)"""

            cursor.execute(insert_player, player)

    conn.commit()


def insert_abs():
    with open('mlb_pitch_data/atbats.csv') as atbats:
        csv_reader = csv.reader(atbats)
        for atbat in csv_reader:
            insert_atbat = """INSERT OR IGNORE INTO atbats VALUES(?,?,?,?)"""

            cursor.execute(insert_atbat, [atbat[0], atbat[1], atbat[2], atbat[8]])

    conn.commit()


def insert_pitches():
    with open('mlb_pitch_data/pitches.csv') as pitches:
        csv_reader = csv.reader(pitches)
        for pitch in csv_reader:

            # ab_id -8, s_count -6, b_count -7, px 0, pz 1, -10 to -13  zone,code,type,pitch_type
            insert_pitch = """INSERT OR IGNORE INTO pitches VALUES(?,?,?,?,?,?,?,?,?)"""

            cursor.execute(
                insert_pitch,
                [
                    pitch[-8],
                    pitch[0],
                    pitch[1],
                    pitch[-14],
                    pitch[-11],
                    pitch[-12],
                    pitch[-13],
                    pitch[-7],
                    pitch[-6],
                ],
            )

    conn.commit()


if __name__ == "__main__":
    # create_tables()
    # insert_players()
    # insert_abs()
    # insert_pitches()
    tmp = cursor.execute('SELECT * FROM players LIMIT 10')

    for thing in tmp:
        print(thing)
