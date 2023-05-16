import pandas as pd
import os


def load_data():
    df_player_passing = pd.read_csv(
        "./Data/FIFA World Cup 2022 Player Data/player_passing.csv", delimiter=","
    )
    df_player_shooting = pd.read_csv(
        "./Data/FIFA World Cup 2022 Player Data/player_shooting.csv", delimiter=","
    )
    df_player_stats = pd.read_csv(
        "./Data/FIFA World Cup 2022 Player Data/player_stats.csv", delimiter=","
    )
    df = df_player_stats[df_player_stats["team"] == "Netherlands"][
        [
            "player",
            "position",
            "age",
            "club",
            "minutes",
            "minutes_90s",
            "goals",
            "assists",
            "goals_pens",
            "pens_made",
            "pens_att",
            "cards_yellow",
            "cards_red",
            "goals_per90",
            "assists_per90",
            "goals_assists_per90",
            "goals_pens_per90",
            "goals_assists_pens_per90",
        ]
    ]
    df_shooting = df_player_shooting[df_player_shooting["team"] == "Netherlands"][
        [
            "player",
            "shots",
            "shots_on_target",
            "shots_on_target_pct",
            "shots_per90",
            "shots_on_target_per90",
            "average_shot_distance",
            "shots_free_kicks",
            "pens_made",
            "pens_att",
        ]
    ]
    df = df.merge(df_shooting, on="player", how="left")
    df_passing = df_player_passing[df_player_passing["team"] == "Netherlands"][
        [
            "player",
            "passes_completed",
            "passes",
            "passes_total_distance",
            "passes_progressive_distance",
            "passes_completed_short",
            "passes_short",
            "passes_completed_medium",
            "passes_medium",
            "passes_completed_long",
            "passes_long",
            "assisted_shots",
            "passes_into_final_third",
            "passes_into_penalty_area",
        ]
    ]
    df = df.merge(df_passing, on="player", how="left")

    pictures = [
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Andries Noppert/Andries Noppert8.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Cody Gakpo/Cody Gakpo12.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Daley Blind/Daley Blind14.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Davy Klaassen/Davy Klaassen11.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Denzel Dumfries/Denzel Dumfries12.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Frenkie de Jong/Frenkie de Jong7.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Jurri+½n Timber/Jurri+½n Timber39.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Kenneth Taylor/Kenneth Taylor9.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Luuk de Jong/Luuk de Jong23.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Marten de Roon/Marten de Roon7.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Matthijs de Ligt/Matthijs de Ligt30.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Memphis Depay/Memphis Depay29.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Nathan Ak+®/Nathan Ak+®15.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Noa Lang/Noa Lang22.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Steven Berghuis/Steven Berghuis19.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Steven Bergwijn/Steven Bergwijn32.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Teun Koopmeiners/Teun Koopmeiners16.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Vincent Janssen/Vincent Janssen49.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Virgil van Dijk (captain)/Virgil van Dijk (captain)36.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Wout Weghorst/Wout Weghorst32.jpg",
    "./Data/FIFA World Cup 2022 Player Images/Images/Images/Group A/Netherlands Players/Images_Xavi Simons/Xavi Simons7.jpg"
    ]

    df['picture'] = pictures 

    df['age'] = df['age'].str[:2].astype(int) 

    return df