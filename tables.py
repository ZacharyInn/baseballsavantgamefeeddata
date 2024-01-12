import sqlite3
import requests
import json
import os

#function to create all tables needed for the database
def create_tables(path):
    #defining connection and cursor
    conn = sqlite3.connect(path)

    cur = conn.cursor()

    #create Game table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Game (
        game_pk INTEGER unique PRIMARY KEY,
        gameDate TEXT,
        game_status_code TEXT,
        game_status TEXT,
        gamedayType TEXT,
        venue TEXT,
        home_team TEXT,
        away_team TEXT,
        home_team_id INTEGER,
        away_team_id INTEGER,
        home_team_runs INTEGER,
        away_team_runs INTEGER,
        home_team_hits INTEGER,
        away_team_hits INTEGER,
        home_team_errors INTEGER,
        away_team_errors INTEGER,
        home_team_lob INTEGER,
        away_team_lob INTEGER,
        probableAwayPitcherID TEXT,
        probableAwayPitcherName TEXT,
        probableHomePitcherID TEXT,
        probableHomePitcherName TEXT,
        cacheKey TEXT,
        cache_hit TEXT
    )
    ''')

    #create Linescore table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Linescore (
        game_pk INTEGER PRIMARY KEY,
        currentInning INTEGER,
        currentInningOrdinal TEXT,
        inningState TEXT,
        inningHalf TEXT,
        isTopInning BOOLEAN,
        scheduledInnings INTEGER
    )
    ''')

    #create InningWPA table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS InningWPA (
        game_pk INTEGER,
        homeTeamWinProbability REAL,
        awayTeamWinProbability REAL,
        homeTeamWinProbabilityAdded REAL,
        hwp REAL,
        awp REAL,
        atBatIndex INTEGER,
        inning TEXT,
        capIndex INTEGER,
        UNIQUE(game_pk, inning, capIndex, homeTeamWinProbability, awayTeamWinProbability, homeTeamWinProbabilityAdded, hwp, awp, atBatIndex)
    )
    ''')

    #create GameWPA table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS GameWPA (
        game_pk INTEGER PRIMARY KEY,
        lastPlayWPA REAL,
        lastPlayName TEXT,
        secondToLastPlayWPA REAL,
        secondToLastPlayName TEXT,
        thirdToLastPlayWPA REAL,
        thirdToLastPlayName TEXT,
        mostWPA REAL,
        mostWPAName TEXT,
        secondMostWPA REAL,
        secondMostWPAName TEXT,
        thirdMostWPA REAL,
        thirdMostWPAName TEXT
    )
    ''')

    #create PlayerExitVelocity table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS PlayerExitVelocity (
        game_pk INTEGER,
        teamID INTEGER,
        teamAbbreviation TEXT,
        batterName TEXT,
        batterID INTEGER,
        atBatIndex INTEGER,
        result TEXT,
        launchSpeed TEXT,
        launchAngle TEXT,
        distance TEXT,
        hitProbabilityFormatted TEXT,
        hitProbability REAL,
        UNIQUE(game_pk, teamID, teamAbbreviation, batterName, batterID, atBatIndex, result, launchSpeed, launchAngle, distance, hitProbabilityFormatted, hitProbability)
    )
    ''')

    #create TeamExitVelocity table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS TeamExitVelocity (
        game_pk INTEGER PRIMARY KEY,
        awayABs INTEGER,
        awaySum REAL,
        awayXBA REAL,
        homeABs INTEGER,
        homeSum REAL,
        homeXBA REAL
    )
    ''')
    
    #create CurrentPlay table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS CurrentPlay (
        game_pk INTEGER,
        type TEXT,
        event TEXT,
        eventType TEXT,
        description TEXT,
        rbi INTEGER,
        awayScore INTEGER,
        homeScore INTEGER,
        isOut BOOLEAN,
        atBatIndex INTEGER,
        halfInning TEXT,
        isTopInning BOOLEAN,
        inning INTEGER,
        startTime TEXT,
        endTime TEXT,
        isComplete BOOLEAN,
        isScoringPlay BOOLEAN,
        hasReview BOOLEAN,
        hasOut BOOLEAN,
        captivatingIndex INTEGER,
        balls INTEGER,
        strikes INTEGER,
        outs INTEGER,
        batterID INTEGER,
        pitcherID INTEGER,
        UNIQUE(game_pk, type, event, eventType, description, rbi, awayScore, homeScore, isOut, atBatIndex, halfInning, isTopInning, inning, startTime, endTime, isComplete, isScoringPlay, hasReview, hasOut, captivatingIndex, balls, strikes, outs, batterID, pitcherID)
    )
    ''')

    #create Inning table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Inning (
        game_pk INTEGER,
        num INTEGER,
        ordinalNum TEXT,
        home_team_runs INTEGER,
        away_team_runs INTEGER,
        home_team_hits INTEGER,
        away_team_hits INTEGER,
        home_team_errors INTEGER,
        away_team_errors INTEGER,
        home_team_lob INTEGER,
        away_team_lob INTEGER,
        UNIQUE(game_pk, num, ordinalNum, home_team_runs, away_team_runs, home_team_hits, away_team_hits, home_team_errors, away_team_errors, home_team_lob, away_team_lob)
    )
    ''')

    #create HomeTeam table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS HomeTeam (
        game_pk INTEGER,
        teamID INTEGER,
        name TEXT,
        link TEXT,
        UNIQUE(game_pk, teamID, name, link)
    )
    ''')

    #create AwayTeam table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS AwayTeam (
        game_pk INTEGER,
        teamID INTEGER,
        name TEXT,
        link TEXT,
        UNIQUE(game_pk, teamID, name, link)
    )
    ''')

    #create Person table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Person (
        playerID INTEGER PRIMARY KEY,
        fullName TEXT,
        link TEXT,
        jerseyNumber TEXT,
        positionCode TEXT,
        positionName TEXT,
        positionType TEXT,
        positionAbbreviation TEXT,
        statusCode TEXT,
        statusDescription TEXT,
        parentTeamId INTEGER
    )
    ''')

    #create Pitch table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Pitch (
        play_id TEXT PRIMARY KEY,
        game_pk INTEGER,
        inning INTEGER,
        ab_number INTEGER,
        cap_index INTEGER,
        outs INTEGER,
        batter INTEGER,
        stand TEXT,
        batter_name TEXT,
        pitcher INTEGER,
        p_throws TEXT,
        pitcher_name TEXT,
        team_batting TEXT,
        team_fielding TEXT,
        team_batting_id INTEGER,
        team_fielding_id INTEGER,
        result TEXT,
        des TEXT,
        events TEXT,
        homeRunBallparks INTEGER,
        strikes INTEGER,
        balls INTEGER,
        pre_strikes INTEGER,
        pre_balls INTEGER,
        call TEXT,
        call_name TEXT,
        pitch_type TEXT,
        pitch_name TEXT,
        description TEXT,
        result_code TEXT,
        pitch_call TEXT,
        is_strike_swinging BOOLEAN,
        balls_and_strikes TEXT,
        start_speed REAL,
        end_speed REAL,
        sz_top REAL,
        sz_bot REAL,
        extension REAL,
        plateTime REAL,
        zone INTEGER,
        spin_rate INTEGER,
        px REAL,
        pz REAL,
        x0 REAL,
        y0 REAL,
        z0 REAL,
        ax REAL,
        ay REAL,
        az REAL,
        vx0 REAL,
        vy0 REAL,
        vz0 REAL,
        pfxX REAL,
        pfxZ REAL,
        pfxZWithGravity REAL,
        pfxZWithGravityNice REAL,
        pfxZDirection TEXT,
        pfxXWithGravity REAL,
        pfxXNoAbs TEXT,
        pfxXDirection TEXT,
        breakX INTEGER,
        breakZ INTEGER,
        inducedBreakZ INTEGER,
        hit_speed_round TEXT,
        hit_speed TEXT,
        hit_distance TEXT,
        xba TEXT,
        hit_angle TEXT,
        is_barrel INTEGER,
        hc_x REAL,
        hc_x_ft REAL,
        hc_y REAL,
        hc_y_ft REAL,
        is_bip_out TEXT,
        pitch_number INTEGER,
        player_total_pitches INTEGER,
        player_total_pitches_pitch_types INTEGER,
        game_total_pitches INTEGER,
        row_id TEXT
    )
    ''')

    #create PitcherMetrics table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS PitcherMetrics (
        playerID INTEGER,
        playerName TEXT,
        oSwingMiss INTEGER,
        oFouls INTEGER,
        oInPlay INTEGER,
        oSwings INTEGER,
        zSwingMiss INTEGER,
        zFouls INTEGER,
        zInPlay INTEGER,
        zSwings INTEGER,
        o_swing REAL,
        z_swing REAL,
        o_contact REAL,
        z_contact REAL,
        zone_rate REAL,
        swings INTEGER,
        miss_percent TEXT,
        cs_plus_whiffs INTEGER,
        csw_percent TEXT,
        avg_rel_x TEXT,
        avg_rel_z TEXT,
        avg_rpm TEXT,
        max_rpm TEXT,
        min_rpm TEXT,
        avg_break_z TEXT,
        max_break_z TEXT,
        min_break_z TEXT,
        avg_break_x TEXT,
        max_break_x TEXT,
        min_break_x TEXT,
        min_pitch_speed TEXT,
        avg_pitch_speed TEXT,
        max_pitch_speed TEXT,
        avg_hit_speed TEXT,
        max_hit_speed TEXT,
        min_hit_speed TEXT,
        count INTEGER,
        balls INTEGER,
        strikes INTEGER,
        X INTEGER,
        fouls INTEGER,
        swinging_strikes INTEGER,
        called_strikes INTEGER,
        balls_in_play INTEGER,
        percent TEXT,
        pitch_type TEXT,
        UNIQUE (playerID, playerName, oSwingMiss, oFouls, oInPlay, oSwings, zSwingMiss, zFouls, zInPlay, zSwings, o_swing, z_swing, o_contact, z_contact, zone_rate, swings, miss_percent, cs_plus_whiffs, csw_percent, avg_rel_x, avg_rel_z, avg_rpm, max_rpm, min_rpm, avg_break_z, max_break_z, min_break_z, avg_break_x, max_break_x, min_break_x, min_pitch_speed, avg_pitch_speed, max_pitch_speed, avg_hit_speed, max_hit_speed, min_hit_speed, count, balls, strikes, X, fouls, swinging_strikes, called_strikes, balls_in_play, percent, pitch_type)
    )
    ''')

    #create GameBattingStats table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS GameBattingStats (
        game_pk INTEGER,
        playerID INTEGER,
        playerName TEXT,
        gamesPlayed INTEGER,
        flyOuts INTEGER,
        groundOuts INTEGER,
        runs INTEGER,
        doubles INTEGER,
        triples INTEGER,
        homeRuns INTEGER,
        strikeOuts INTEGER,
        baseOnBalls INTEGER,
        intentionalWalks INTEGER,
        hits INTEGER,
        hitByPitch INTEGER,
        atBats INTEGER,
        caughtStealing INTEGER,
        stolenBases INTEGER,
        stolenBasePercentage TEXT,
        groundIntoDoublePlay INTEGER,
        groundIntoTriplePlay INTEGER,
        plateAppearances INTEGER,
        totalBases INTEGER,
        rbi INTEGER,
        leftOnBase INTEGER,
        sacBunts INTEGER,
        sacFlies INTEGER,
        catchersInterference INTEGER,
        pickoffs INTEGER,
        atBatsPerHomeRun TEXT,
        UNIQUE(game_pk, playerID)
    )
    ''')

    #create SeasonBattingStats table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS SeasonBattingStats (
        game_pk INTEGER,
        playerID INTEGER,
        playerName TEXT,
        gamesPlayed INTEGER,
        flyOuts INTEGER,
        groundOuts INTEGER,
        runs INTEGER,
        doubles INTEGER,
        triples INTEGER,
        homeRuns INTEGER,
        strikeOuts INTEGER,
        baseOnBalls INTEGER,
        intentionalWalks INTEGER,
        hits INTEGER,
        hitByPitch INTEGER,
        avg TEXT,
        atBats INTEGER,
        obp TEXT,
        slg TEXT,
        ops TEXT,
        caughtStealing INTEGER,
        stolenBases INTEGER,
        stolenBasePercentage TEXT,
        groundIntoDoublePlay INTEGER,
        groundIntoTriplePlay INTEGER,
        plateAppearances INTEGER,
        totalBases INTEGER,
        rbi INTEGER,
        leftOnBase INTEGER,
        sacBunts INTEGER,
        sacFlies INTEGER,
        babip TEXT,
        catchersInterference INTEGER,
        pickoffs INTEGER,
        atBatsPerHomeRun TEXT,
        UNIQUE (game_pk, playerID, playerName, gamesPlayed, flyOuts, groundOuts, runs, doubles, triples, homeRuns, strikeOuts, baseOnBalls, intentionalWalks, hits, hitByPitch, avg, atBats, obp, slg, ops, caughtStealing, stolenBases, stolenBasePercentage, groundIntoDoublePlay, groundIntoTriplePlay, plateAppearances, totalBases, rbi, leftOnBase, sacBunts, sacFlies, babip, catchersInterference, pickoffs, atBatsPerHomeRun)
    )
    ''')

    #create GamePitchingStats table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS GamePitchingStats (
            game_pk INTEGER,
            playerID INTEGER,
            playerName TEXT,
            gamesPlayed INTEGER,
            gamesStarted INTEGER,
            groundOuts INTEGER,
            airOuts INTEGER,
            runs INTEGER,
            doubles INTEGER,
            triples INTEGER,
            homeRuns INTEGER,
            strikeOuts INTEGER,
            baseOnBalls INTEGER,
            intentionalWalks INTEGER,
            hits INTEGER,
            hitByPitch INTEGER,
            atBats INTEGER,
            caughtStealing INTEGER,
            stolenBases INTEGER,
            stolenBasePercentage TEXT,
            numberOfPitches INTEGER,
            inningsPitched TEXT,
            wins INTEGER,
            losses INTEGER,
            saves INTEGER,
            saveOpportunities INTEGER,
            holds INTEGER,
            blownSaves INTEGER,
            earnedRuns INTEGER,
            battersFaced INTEGER,
            outs INTEGER,
            gamesPitched INTEGER,
            completeGames INTEGER,
            shutouts INTEGER,
            pitchesThrown INTEGER,
            balls INTEGER,
            strikes INTEGER,
            strikePercentage TEXT,
            hitBatsmen INTEGER,
            balks INTEGER,
            wildPitches INTEGER,
            pickoffs INTEGER,
            rbi REAL,
            gamesFinished INTEGER,
            runsScoredPer9 TEXT,
            homeRunsPer9 TEXT,
            inheritedRunners INTEGER,
            inheritedRunnersScored INTEGER,
            catchersInterference INTEGER,
            sacBunts INTEGER,
            sacFlies INTEGER,
            passedBall INTEGER,
            UNIQUE(game_pk, playerID)
            )
    ''')

    #create SeasonPitchingStats table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS SeasonPitchingStats (
            game_pk INTEGER,
            playerID INTEGER,
            playerName TEXT,
            gamesPlayed INTEGER,
            gamesStarted INTEGER,
            groundOuts INTEGER,
            airOuts INTEGER,
            runs INTEGER,
            doubles INTEGER,
            triples INTEGER,
            homeRuns INTEGER,
            strikeOuts INTEGER,
            baseOnBalls INTEGER,
            intentionalWalks INTEGER,
            hits INTEGER,
            hitByPitch INTEGER,
            atBats INTEGER,
            obp TEXT,
            caughtStealing INTEGER,
            stolenBases INTEGER,
            stolenBasePercentage TEXT,
            numberOfPitches INTEGER,
            era TEXT,
            inningsPitched TEXT,
            wins INTEGER,
            losses INTEGER,
            saves INTEGER,
            saveOpportunities INTEGER,
            holds INTEGER,
            blownSaves INTEGER,
            earnedRuns INTEGER,
            whip TEXT,
            battersFaced INTEGER,
            outs INTEGER,
            gamesPitched INTEGER,
            completeGames INTEGER,
            shutouts INTEGER,
            pitchesThrown INTEGER,
            balls INTEGER,
            strikes INTEGER,
            strikePercentage TEXT,
            hitBatsmen INTEGER,
            balks INTEGER,
            wildPitches INTEGER,
            pickoffs INTEGER,
            groundOutsToAirouts TEXT,
            rbi REAL,
            winPercentage TEXT,
            pitchesPerInning TEXT,
            gamesFinished INTEGER,
            strikeoutWalkRatio TEXT,
            strikeoutPer9Inn TEXT,
            walksPer9Inn TEXT,
            hitsPer9Inn TEXT,
            runsScoredPer9 TEXT,
            homeRunsPer9 TEXT,
            inheritedRunners INTEGER,
            inheritedRunnersScored INTEGER,
            catchersInterference INTEGER,
            sacBunts INTEGER,
            sacFlies INTEGER,
            passedBall INTEGER,
            UNIQUE (game_pk, playerID, playerName, gamesPlayed, gamesStarted, groundOuts, airOuts, runs, doubles, triples, homeRuns, strikeOuts, baseOnBalls, intentionalWalks, hits, hitByPitch, atBats, obp, caughtStealing, stolenBases, stolenBasePercentage, numberOfPitches, era, inningsPitched, wins, losses, saves, saveOpportunities, holds, blownSaves, earnedRuns, whip, battersFaced, outs, gamesPitched, completeGames, shutouts, pitchesThrown, balls, strikes, strikePercentage, hitBatsmen, balks, wildPitches, pickoffs, groundOutsToAirouts, rbi, winPercentage, pitchesPerInning, gamesFinished, strikeoutWalkRatio, strikeoutPer9Inn, walksPer9Inn, hitsPer9Inn, runsScoredPer9, homeRunsPer9, inheritedRunners, inheritedRunnersScored, catchersInterference, sacBunts, sacFlies, passedBall)
        )
    ''')

    #create GameFieldingStats table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS GameFieldingStats (
            game_pk INTEGER,
            playerID INTEGER,
            playerName TEXT,
            gamesStarted INTEGER,
            caughtStealing INTEGER,
            stolenBases INTEGER,
            stolenBasePercentage TEXT,
            assists INTEGER,
            putOuts INTEGER,
            errors INTEGER,
            chances INTEGER,
            fieldingPercentage TEXT,
            passedBall INTEGER,
            pickoffs INTEGER,
            UNIQUE(game_pk, playerID)
            )
    ''')

    #create SeasonFieldingStats table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS SeasonFieldingStats (
            game_pk INTEGER,
            playerID INTEGER,
            playerName TEXT,
            gamesStarted INTEGER,
            caughtStealing INTEGER,
            stolenBases INTEGER,
            stolenBasePercentage TEXT,
            assists INTEGER,
            putOuts INTEGER,
            errors INTEGER,
            chances INTEGER,
            fieldingPercentage TEXT,
            passedBall INTEGER,
            pickoffs INTEGER,
            UNIQUE (game_pk, playerID, playerName, caughtStealing, stolenBases, stolenBasePercentage, assists, putOuts, errors, chances, fieldingPercentage, passedBall, pickoffs)
        )
    ''')

    #create Officials table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Officials (
            game_pk INTEGER,
            officialID INTEGER,
            fullName TEXT,
            link TEXT,
            officialType TEXT,
            UNIQUE (game_pk, officialID, fullName, link, officialType)
        )
    ''')

    print("Tables created successfully.")
    conn.commit()
    conn.close()

#function to insert data into the tables
def insert_data(conn, game_data):
    cursor = conn.cursor()
    
    #insert values into Game table
    try:
        cursor.execute('''
            INSERT INTO Game
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data.get('gameDate'), 
              game_data.get('game_status_code'), 
              game_data.get('game_status'), 
              game_data.get('gamedayType'), 
              game_data['boxscore']['info'][len(game_data['boxscore']['info']) - 2].get('value'), 
              game_data['scoreboard']['teams']['home'].get('name'), 
              game_data['scoreboard']['teams']['away'].get('name'), 
              game_data['scoreboard']['teams']['home'].get('id'), 
              game_data['scoreboard']['teams']['away'].get('id'), 
              game_data['scoreboard']['linescore']['teams']['home'].get('runs'), 
              game_data['scoreboard']['linescore']['teams']['away'].get('runs'), 
              game_data['scoreboard']['linescore']['teams']['home'].get('hits'), 
              game_data['scoreboard']['linescore']['teams']['away'].get('hits'), 
              game_data['scoreboard']['linescore']['teams']['home'].get('errors'), 
              game_data['scoreboard']['linescore']['teams']['away'].get('errors'), 
              game_data['scoreboard']['linescore']['teams']['home'].get('leftOnBase'), 
              game_data['scoreboard']['linescore']['teams']['away'].get('leftOnBase'), 
              game_data['scoreboard']['probablePitchers']['away'].get('id'), 
              game_data['scoreboard']['probablePitchers']['away'].get('fullName'), 
              game_data['scoreboard']['probablePitchers']['home'].get('id'), 
              game_data['scoreboard']['probablePitchers']['home'].get('fullName'), 
              game_data.get('cacheKey'), 
              game_data.get('cache_hit')))

    except:
        pass
        

    #insert values into Linescore table
    try:
        cursor.execute('''
            INSERT INTO Linescore
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data['scoreboard']['linescore'].get('currentInning'), 
              game_data['scoreboard']['linescore'].get('currentInningOrdinal'), 
              game_data['scoreboard']['linescore'].get('inningState'), 
              game_data['scoreboard']['linescore'].get('inningHalf'), 
              game_data['scoreboard']['linescore'].get('isTopInning'), 
              game_data['scoreboard']['linescore'].get('scheduledInnings')))
    
    except:
        pass

    #insert values into InningWPA table
    try:
        for count, value in enumerate(game_data['scoreboard']['stats']['wpa']['gameWpa']):
            cursor.execute('''
                INSERT OR IGNORE INTO InningWPA
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['scoreboard'].get('gamePk'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('homeTeamWinProbability'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('awayTeamWinProbability'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('homeTeamWinProbabilityAdded'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('hwp'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('awp'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('atBatIndex'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('i'), 
                  game_data['scoreboard']['stats']['wpa']['gameWpa'][count].get('capIndex')))
    except:
        pass   
    
    #insert values into GameWPA table
    try:
        cursor.execute('''
            INSERT INTO GameWPA
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][0].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][0].get('name'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][1].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][1].get('name'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][2].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['lastPlays'][2].get('name'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][0].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][0].get('name'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][1].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][1].get('name'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][2].get('wpa'), 
              game_data['scoreboard']['stats']['wpa']['topWpaPlayers'][2].get('name')))
    except:
        pass

    #insert values into PlayerExitVelocity table
    try:
        for count, value in enumerate(game_data['scoreboard']['stats']['exitVelocity']['top']):
            cursor.execute('''
                INSERT OR IGNORE INTO PlayerExitVelocity
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['scoreboard'].get('gamePk'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('team'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('teamAbbrev'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('batterName'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('batterId'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('atBatIndex'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('result'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('launchSpeed'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('launchAngle'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('distance'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('hitProbabilityFormatted'), 
                  game_data['scoreboard']['stats']['exitVelocity']['top'][count].get('hitProbability')))
        
        for count, value in enumerate(game_data['scoreboard']['stats']['exitVelocity']['lastEV']):
            cursor.execute('''
                INSERT OR IGNORE INTO PlayerExitVelocity
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['scoreboard'].get('gamePk'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('team'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('teamAbbrev'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('batterName'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('batterId'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('atBatIndex'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('result'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('launchSpeed'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('launchAngle'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('distance'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('hitProbabilityFormatted'), 
                  game_data['scoreboard']['stats']['exitVelocity']['lastEV'][count].get('hitProbability')))
        
        for count, value in enumerate(game_data['scoreboard']['stats']['exitVelocity']['topDistance']):
            cursor.execute('''
                INSERT OR IGNORE INTO PlayerExitVelocity
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['scoreboard'].get('gamePk'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('team'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('teamAbbrev'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('batterName'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('batterId'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('atBatIndex'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('result'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('launchSpeed'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('launchAngle'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('distance'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('hitProbabilityFormatted'), 
                  game_data['scoreboard']['stats']['exitVelocity']['topDistance'][count].get('hitProbability')))
    except:
        pass

    #insert values into TeamExitVelocity table
    try:
        cursor.execute('''
            INSERT INTO TeamExitVelocity
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'),
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['away'].get('abs'), 
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['away'].get('sum'), 
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['away'].get('xba'), 
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['home'].get('abs'), 
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['home'].get('sum'), 
              game_data['scoreboard']['stats']['exitVelocity']['xbaTeam']['home'].get('xba')))
    except:
        pass

    #insert values into CurrentPlay table
    try:
        cursor.execute('''
            INSERT INTO CurrentPlay
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data['scoreboard']['currentPlay']['result'].get('type'), 
              game_data['scoreboard']['currentPlay']['result'].get('event'), 
              game_data['scoreboard']['currentPlay']['result'].get('eventType'), 
              game_data['scoreboard']['currentPlay']['result'].get('description'), 
              game_data['scoreboard']['currentPlay']['result'].get('rbi'), 
              game_data['scoreboard']['currentPlay']['result'].get('awayScore'), 
              game_data['scoreboard']['currentPlay']['result'].get('homeScore'), 
              game_data['scoreboard']['currentPlay']['result'].get('isOut'), 
              game_data['scoreboard']['currentPlay']['about'].get('atBatIndex'), 
              game_data['scoreboard']['currentPlay']['about'].get('halfInning'), 
              game_data['scoreboard']['currentPlay']['about'].get('isTopInning'), 
              game_data['scoreboard']['currentPlay']['about'].get('inning'), 
              game_data['scoreboard']['currentPlay']['about'].get('startTime'), 
              game_data['scoreboard']['currentPlay']['about'].get('endTime'), 
              game_data['scoreboard']['currentPlay']['about'].get('isComplete'), 
              game_data['scoreboard']['currentPlay']['about'].get('isScoringPlay'), 
              game_data['scoreboard']['currentPlay']['about'].get('hasReview'), 
              game_data['scoreboard']['currentPlay']['about'].get('hasOut'), 
              game_data['scoreboard']['currentPlay']['about'].get('captivatingIndex'), 
              game_data['scoreboard']['currentPlay']['count'].get('balls'), 
              game_data['scoreboard']['currentPlay']['count'].get('strikes'), 
              game_data['scoreboard']['currentPlay']['count'].get('outs'), 
              game_data['scoreboard']['currentPlay']['matchup']['batter'].get('id'), 
              game_data['scoreboard']['currentPlay']['matchup']['pitcher'].get('id')))
    except:
        pass

    #insert values into Inning table
    for count, value in enumerate(game_data['scoreboard']['linescore']['innings']):
            cursor.execute('''
                INSERT OR IGNORE INTO Inning
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['scoreboard'].get('gamePk'), 
                  game_data['scoreboard']['linescore']['innings'][count].get('num'), 
                  game_data['scoreboard']['linescore']['innings'][count].get('ordinalNum'), 
                  game_data['scoreboard']['linescore']['innings'][count]['home'].get('runs'), 
                  game_data['scoreboard']['linescore']['innings'][count]['away'].get('runs'), 
                  game_data['scoreboard']['linescore']['innings'][count]['home'].get('hits'), 
                  game_data['scoreboard']['linescore']['innings'][count]['away'].get('hits'), 
                  game_data['scoreboard']['linescore']['innings'][count]['home'].get('errors'), 
                  game_data['scoreboard']['linescore']['innings'][count]['away'].get('errors'), 
                  game_data['scoreboard']['linescore']['innings'][count]['home'].get('leftOnBase'), 
                  game_data['scoreboard']['linescore']['innings'][count]['away'].get('leftOnBase')))

    
    #insert values into HomeTeam table
    try:
        cursor.execute('''
            INSERT INTO HomeTeam
            VALUES (?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data['scoreboard']['teams']['home'].get('id'), 
              game_data['scoreboard']['teams']['home'].get('name'), 
              game_data['scoreboard']['teams']['home'].get('link')))
    except:
        pass

    #insert values into AwayTeam table
    try:
        cursor.execute('''
            INSERT INTO AwayTeam
            VALUES (?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'), 
              game_data['scoreboard']['teams']['away'].get('id'), 
              game_data['scoreboard']['teams']['away'].get('name'), 
              game_data['scoreboard']['teams']['away'].get('link')))
    except:
        pass

    #insert values into Person table
    #insert the away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        cursor.execute('''
                INSERT OR IGNORE INTO Person
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['away_lineup'][count], 
                  game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'), 
                  game_data['boxscore']['teams']['away']['players'][playID]['person'].get('link'),
                  game_data['boxscore']['teams']['away']['players'][playID].get('jerseyNumber'), 
                  game_data['boxscore']['teams']['away']['players'][playID]['position'].get('code'), 
                  game_data['boxscore']['teams']['away']['players'][playID]['position'].get('name'), 
                  game_data['boxscore']['teams']['away']['players'][playID]['position'].get('type'),
                  game_data['boxscore']['teams']['away']['players'][playID]['position'].get('abbreviation'),
                  game_data['boxscore']['teams']['away']['players'][playID]['status'].get('code'),
                  game_data['boxscore']['teams']['away']['players'][playID]['status'].get('description'),
                  game_data['boxscore']['teams']['away']['players'][playID].get('parentTeamId')))
        
    #insert the home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        cursor.execute('''
                INSERT OR IGNORE INTO Person
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_data['home_lineup'][count], 
                  game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'), 
                  game_data['boxscore']['teams']['home']['players'][playID]['person'].get('link'),
                  game_data['boxscore']['teams']['home']['players'][playID].get('jerseyNumber'), 
                  game_data['boxscore']['teams']['home']['players'][playID]['position'].get('code'), 
                  game_data['boxscore']['teams']['home']['players'][playID]['position'].get('name'), 
                  game_data['boxscore']['teams']['home']['players'][playID]['position'].get('type'),
                  game_data['boxscore']['teams']['home']['players'][playID]['position'].get('abbreviation'),
                  game_data['boxscore']['teams']['home']['players'][playID]['status'].get('code'),
                  game_data['boxscore']['teams']['home']['players'][playID]['status'].get('description'),
                  game_data['boxscore']['teams']['home']['players'][playID].get('parentTeamId')))
        
    #insert values into Pitch table
    #home team pitches
    for count, value in enumerate(game_data['team_home']):
        cursor.execute('''
                INSERT OR IGNORE INTO Pitch
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['team_home'][count].get('play_id'),             
                  game_data['scoreboard'].get('gamePk'), 
                  game_data['team_home'][count].get('inning'), 
                  game_data['team_home'][count].get('ab_number'), 
                  game_data['team_home'][count].get('cap_index'), 
                  game_data['team_home'][count].get('outs'), 
                  game_data['team_home'][count].get('batter'), 
                  game_data['team_home'][count].get('stand'), 
                  game_data['team_home'][count].get('batter_name'), 
                  game_data['team_home'][count].get('pitcher'), 
                  game_data['team_home'][count].get('p_throws'), 
                  game_data['team_home'][count].get('pitcher_name'), 
                  game_data['team_home'][count].get('team_batting'), 
                  game_data['team_home'][count].get('team_fielding'), 
                  game_data['team_home'][count].get('team_batting_id'),
                  game_data['team_home'][count].get('team_fielding_id'),
                  game_data['team_home'][count].get('result'), 
                  game_data['team_home'][count].get('des'), 
                  game_data['team_home'][count].get('events'),
                  game_data['team_home'][count]['contextMetrics'].get('homeRunBallparks'),
                  game_data['team_home'][count].get('strikes'), 
                  game_data['team_home'][count].get('balls'), 
                  game_data['team_home'][count].get('pre_strikes'), 
                  game_data['team_home'][count].get('pre_balls'), 
                  game_data['team_home'][count].get('call'), 
                  game_data['team_home'][count].get('call_name'), 
                  game_data['team_home'][count].get('pitch_type'), 
                  game_data['team_home'][count].get('pitch_name'), 
                  game_data['team_home'][count].get('description'), 
                  game_data['team_home'][count].get('result_code'), 
                  game_data['team_home'][count].get('pitch_call'), 
                  game_data['team_home'][count].get('is_strike_swinging'), 
                  game_data['team_home'][count].get('balls_and_strikes'),
                  game_data['team_home'][count].get('start_speed'), 
                  game_data['team_home'][count].get('end_speed'), 
                  game_data['team_home'][count].get('sz_top'), 
                  game_data['team_home'][count].get('sz_bot'), 
                  game_data['team_home'][count].get('extension'), 
                  game_data['team_home'][count].get('plateTime'), 
                  game_data['team_home'][count].get('zone'), 
                  game_data['team_home'][count].get('spin_rate'), 
                  game_data['team_home'][count].get('px'), 
                  game_data['team_home'][count].get('pz'), 
                  game_data['team_home'][count].get('x0'), 
                  game_data['team_home'][count].get('y0'), 
                  game_data['team_home'][count].get('z0'), 
                  game_data['team_home'][count].get('ax'), 
                  game_data['team_home'][count].get('ay'), 
                  game_data['team_home'][count].get('az'), 
                  game_data['team_home'][count].get('vx0'), 
                  game_data['team_home'][count].get('vy0'), 
                  game_data['team_home'][count].get('vz0'), 
                  game_data['team_home'][count].get('pfxX'), 
                  game_data['team_home'][count].get('pfxZ'), 
                  game_data['team_home'][count].get('pfxZWithGravity'), 
                  game_data['team_home'][count].get('pfxZWithGravityNice'),
                  game_data['team_home'][count].get('pfxZDirection'),
                  game_data['team_home'][count].get('pfxXWithGravity'), 
                  game_data['team_home'][count].get('pfxXNoAbs'), 
                  game_data['team_home'][count].get('pfxXDirection'),
                  game_data['team_home'][count].get('breakX'), 
                  game_data['team_home'][count].get('breakZ'), 
                  game_data['team_home'][count].get('inducedBreakZ'), 
                  game_data['team_home'][count].get('hit_speed_round'), 
                  game_data['team_home'][count].get('hit_speed'), 
                  game_data['team_home'][count].get('hit_distance'),
                  game_data['team_home'][count].get('xba'),
                  game_data['team_home'][count].get('hit_angle'),
                  game_data['team_home'][count].get('is_barrel'),
                  game_data['team_home'][count].get('hc_x'),
                  game_data['team_home'][count].get('hc_x_ft'),
                  game_data['team_home'][count].get('hc_y'),
                  game_data['team_home'][count].get('hc_y_ft'),
                  game_data['team_home'][count].get('is_bip_out'),
                  game_data['team_home'][count].get('pitch_number'),
                  game_data['team_home'][count].get('player_total_pitches'),
                  game_data['team_home'][count].get('player_total_pitches_pitch_types'),
                  game_data['team_home'][count].get('game_total_pitches'),
                  game_data['team_home'][count].get('rowId')))       

    #away team pitches
    for count, value in enumerate(game_data['team_away']):
            cursor.execute('''
                INSERT OR IGNORE INTO Pitch
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['team_away'][count].get('play_id'),             
                  game_data['scoreboard'].get('gamePk'), 
                  game_data['team_away'][count].get('inning'), 
                  game_data['team_away'][count].get('ab_number'), 
                  game_data['team_away'][count].get('cap_index'), 
                  game_data['team_away'][count].get('outs'), 
                  game_data['team_away'][count].get('batter'), 
                  game_data['team_away'][count].get('stand'), 
                  game_data['team_away'][count].get('batter_name'), 
                  game_data['team_away'][count].get('pitcher'), 
                  game_data['team_away'][count].get('p_throws'), 
                  game_data['team_away'][count].get('pitcher_name'), 
                  game_data['team_away'][count].get('team_batting'), 
                  game_data['team_away'][count].get('team_fielding'), 
                  game_data['team_away'][count].get('team_batting_id'),
                  game_data['team_away'][count].get('team_fielding_id'),
                  game_data['team_away'][count].get('result'), 
                  game_data['team_away'][count].get('des'), 
                  game_data['team_away'][count].get('events'),
                  game_data['team_away'][count]['contextMetrics'].get('homeRunBallparks'),
                  game_data['team_away'][count].get('strikes'), 
                  game_data['team_away'][count].get('balls'), 
                  game_data['team_away'][count].get('pre_strikes'), 
                  game_data['team_away'][count].get('pre_balls'), 
                  game_data['team_away'][count].get('call'), 
                  game_data['team_away'][count].get('call_name'), 
                  game_data['team_away'][count].get('pitch_type'), 
                  game_data['team_away'][count].get('pitch_name'), 
                  game_data['team_away'][count].get('description'), 
                  game_data['team_away'][count].get('result_code'), 
                  game_data['team_away'][count].get('pitch_call'), 
                  game_data['team_away'][count].get('is_strike_swinging'), 
                  game_data['team_away'][count].get('balls_and_strikes'),
                  game_data['team_away'][count].get('start_speed'), 
                  game_data['team_away'][count].get('end_speed'), 
                  game_data['team_away'][count].get('sz_top'), 
                  game_data['team_away'][count].get('sz_bot'), 
                  game_data['team_away'][count].get('extension'), 
                  game_data['team_away'][count].get('plateTime'), 
                  game_data['team_away'][count].get('zone'), 
                  game_data['team_away'][count].get('spin_rate'), 
                  game_data['team_away'][count].get('px'), 
                  game_data['team_away'][count].get('pz'), 
                  game_data['team_away'][count].get('x0'), 
                  game_data['team_away'][count].get('y0'), 
                  game_data['team_away'][count].get('z0'), 
                  game_data['team_away'][count].get('ax'), 
                  game_data['team_away'][count].get('ay'), 
                  game_data['team_away'][count].get('az'), 
                  game_data['team_away'][count].get('vx0'), 
                  game_data['team_away'][count].get('vy0'), 
                  game_data['team_away'][count].get('vz0'), 
                  game_data['team_away'][count].get('pfxX'), 
                  game_data['team_away'][count].get('pfxZ'), 
                  game_data['team_away'][count].get('pfxZWithGravity'), 
                  game_data['team_away'][count].get('pfxZWithGravityNice'),
                  game_data['team_away'][count].get('pfxZDirection'),
                  game_data['team_away'][count].get('pfxXWithGravity'), 
                  game_data['team_away'][count].get('pfxXNoAbs'), 
                  game_data['team_away'][count].get('pfxXDirection'),
                  game_data['team_away'][count].get('breakX'), 
                  game_data['team_away'][count].get('breakZ'), 
                  game_data['team_away'][count].get('inducedBreakZ'), 
                  game_data['team_away'][count].get('hit_speed_round'), 
                  game_data['team_away'][count].get('hit_speed'), 
                  game_data['team_away'][count].get('hit_distance'),
                  game_data['team_away'][count].get('xba'),
                  game_data['team_away'][count].get('hit_angle'),
                  game_data['team_away'][count].get('is_barrel'),
                  game_data['team_away'][count].get('hc_x'),
                  game_data['team_away'][count].get('hc_x_ft'),
                  game_data['team_away'][count].get('hc_y'),
                  game_data['team_away'][count].get('hc_y_ft'),
                  game_data['team_away'][count].get('is_bip_out'),
                  game_data['team_away'][count].get('pitch_number'),
                  game_data['team_away'][count].get('player_total_pitches'),
                  game_data['team_away'][count].get('player_total_pitches_pitch_types'),
                  game_data['team_away'][count].get('game_total_pitches'),
                  game_data['team_away'][count].get('rowId')))

    #insert data into PitcherMetrics table
    #home pitcher metrics
    for count, value in enumerate(game_data['home_pitcher_lineup']):
        playID = game_data['home_pitcher_lineup'][count]
        for count1, value in enumerate(game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed']):
            cursor.execute('''
                    INSERT OR IGNORE INTO PitcherMetrics
                               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (playID,
                      game_data['home_pitchers'][str(playID)][0].get('pitcher_name'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oSwingMiss'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oFouls'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oInPlay'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oSwings'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zSwingMiss'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zFouls'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zInPlay'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zSwings'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('o_swing'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('z_swing'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('o_contact'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('z_contact'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zone_rate'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('swings'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('miss_percent'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('cs_plus_whiffs'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('csw_percent'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rel_x'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rel_z'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rpm'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_rpm'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_rpm'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_break_z'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_break_z'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_break_z'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_break_x'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_break_x'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_break_x'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_pitch_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_pitch_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_pitch_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_hit_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_hit_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_hit_speed'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('count'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('S'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('B'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('X'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('fouls'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('swinging_strikes'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('called_strikes'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('balls_in_play'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('percent'),
                      game_data['home_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('pitch_type'),))
    
    #away pitcher metrics
    for count, value in enumerate(game_data['away_pitcher_lineup']):
        playID = game_data['away_pitcher_lineup'][count]
        for count1, value in enumerate(game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed']):
            cursor.execute('''
                    INSERT OR IGNORE INTO PitcherMetrics
                               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (playID,
                      game_data['away_pitchers'][str(playID)][0].get('pitcher_name'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oSwingMiss'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oFouls'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oInPlay'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('oSwings'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zSwingMiss'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zFouls'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zInPlay'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zSwings'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('o_swing'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('z_swing'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('o_contact'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('z_contact'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('zone_rate'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('swings'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('miss_percent'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('cs_plus_whiffs'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('csw_percent'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rel_x'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rel_z'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_rpm'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_rpm'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_rpm'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_break_z'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_break_z'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_break_z'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_break_x'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_break_x'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_break_x'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_pitch_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_pitch_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_pitch_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('avg_hit_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('max_hit_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('min_hit_speed'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('count'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('S'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('B'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1]['results'].get('X'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('fouls'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('swinging_strikes'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('called_strikes'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('balls_in_play'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('percent'),
                      game_data['away_pitchers'][str(playID)][0]['avg_pitch_speed'][count1].get('pitch_type'),))
                
    #insert data into GameBattingStats table
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GameBattingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard']['gamePk'],
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('flyOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('groundOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('runs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('doubles'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('triples'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('homeRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('strikeOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('hits'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('hitByPitch'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('atBats'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('groundIntoDoublePlay'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('groundIntoTriplePlay'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('plateAppearances'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('totalBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('rbi'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('leftOnBase'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('sacBunts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('sacFlies'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('catchersInterference'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('pickoffs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['batting'].get('atBatsPerHomeRun')))
            
    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GameBattingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard']['gamePk'],
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('flyOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('groundOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('runs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('doubles'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('triples'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('homeRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('strikeOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('hits'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('hitByPitch'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('atBats'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('groundIntoDoublePlay'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('groundIntoTriplePlay'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('plateAppearances'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('totalBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('rbi'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('leftOnBase'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('sacBunts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('sacFlies'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('catchersInterference'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('pickoffs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['batting'].get('atBatsPerHomeRun')))
    
    #insert data into SeasonGameStats
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonBattingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('flyOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('groundOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('runs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('doubles'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('triples'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('homeRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('strikeOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('hits'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('hitByPitch'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('avg'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('atBats'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('obp'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('slg'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('ops'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('groundIntoDoublePlay'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('groundIntoTriplePlay'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('plateAppearances'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('totalBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('rbi'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('leftOnBase'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('sacBunts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('sacFlies'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('babip'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('catchersInterference'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('pickoffs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['batting'].get('atBatsPerHomeRun')))

    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonBattingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('flyOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('groundOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('runs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('doubles'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('triples'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('homeRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('strikeOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('hits'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('hitByPitch'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('avg'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('atBats'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('obp'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('slg'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('ops'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('groundIntoDoublePlay'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('groundIntoTriplePlay'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('plateAppearances'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('totalBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('rbi'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('leftOnBase'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('sacBunts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('sacFlies'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('babip'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('catchersInterference'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('pickoffs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['batting'].get('atBatsPerHomeRun')))
    
    #insert data into GamePitchingStats
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GamePitchingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('gamesStarted'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('groundOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('airOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('runs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('doubles'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('triples'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('homeRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('strikeOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('hits'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('hitByPitch'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('atBats'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('numberOfPitches'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('inningsPitched'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('wins'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('losses'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('saves'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('saveOpportunities'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('holds'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('blownSaves'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('earnedRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('battersFaced'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('outs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('gamesPitched'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('completeGames'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('shutouts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('pitchesThrown'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('balls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('strikes'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('strikePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('hitBatsmen'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('balks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('wildPitches'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('pickoffs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('rbi'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('gamesFinished'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('runsScoredPer9'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('homeRunsPer9'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('inheritedRunners'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('inheritedRunnersScored'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('catchersInterference'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('sacBunts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('sacFlies'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['pitching'].get('passedBall')))
    
    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GamePitchingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('gamesStarted'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('groundOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('airOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('runs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('doubles'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('triples'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('homeRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('strikeOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('hits'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('hitByPitch'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('atBats'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('numberOfPitches'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('inningsPitched'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('wins'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('losses'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('saves'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('saveOpportunities'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('holds'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('blownSaves'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('earnedRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('battersFaced'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('outs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('gamesPitched'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('completeGames'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('shutouts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('pitchesThrown'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('balls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('strikes'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('strikePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('hitBatsmen'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('balks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('wildPitches'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('pickoffs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('rbi'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('gamesFinished'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('runsScoredPer9'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('awayRunsPer9'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('inheritedRunners'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('inheritedRunnersScored'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('catchersInterference'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('sacBunts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('sacFlies'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['pitching'].get('passedBall')))
    
    #insert data into SeasonPitchingStats
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonPitchingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('gamesStarted'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('groundOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('airOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('runs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('doubles'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('triples'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('homeRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('strikeOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('hits'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('hitByPitch'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('atBats'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('obp'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('numberOfPitches'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('era'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('inningsPitched'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('wins'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('losses'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('saves'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('saveOpportunities'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('holds'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('blownSaves'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('earnedRuns'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('whip'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('battersFaced'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('outs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('gamesPitched'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('completeGames'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('shutouts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('pitchesThrown'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('balls'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('strikes'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('strikePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('hitBatsmen'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('balks'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('wildPitches'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('pickoffs'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('groundOutsToAirouts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('rbi'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('winPercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('pitchesPerInning'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('gamesFinished'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('strikeoutWalkRatio'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('strikeoutsPer9Inn'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('walksPer9Inn'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('hitsPer9Inn'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('runsScoredPer9'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('homeRunsPer9'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('inheritedRunners'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('inheritedRunnersScored'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('catchersInterference'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('sacBunts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('sacFlies'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['pitching'].get('passedBall')))
    
    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonPitchingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('gamesPlayed'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('gamesStarted'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('groundOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('airOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('runs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('doubles'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('triples'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('homeRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('strikeOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('baseOnBalls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('intentionalWalks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('hits'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('hitByPitch'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('atBats'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('obp'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('numberOfPitches'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('era'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('inningsPitched'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('wins'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('losses'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('saves'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('saveOpportunities'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('holds'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('blownSaves'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('earnedRuns'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('whip'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('battersFaced'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('outs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('gamesPitched'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('completeGames'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('shutouts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('pitchesThrown'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('balls'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('strikes'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('strikePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('hitBatsmen'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('balks'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('wildPitches'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('pickoffs'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('groundOutsToAirouts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('rbi'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('winPercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('pitchesPerInning'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('gamesFinished'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('strikeoutWalkRatio'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('strikeoutsPer9Inn'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('walksPer9Inn'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('hitsPer9Inn'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('runsScoredPer9'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('awayRunsPer9'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('inheritedRunners'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('inheritedRunnersScored'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('catchersInterference'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('sacBunts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('sacFlies'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['pitching'].get('passedBall')))
    
    #insert data into GameFieldingStats
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GameFieldingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('gamesStarted'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('assists'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('putOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('errors'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('chances'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('fielding'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('passedBall'),
                      game_data['boxscore']['teams']['home']['players'][playID]['stats']['fielding'].get('pickoffs')))
            
    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
            cursor.execute('''
                    INSERT OR IGNORE INTO GameFieldingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('gamesStarted'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('assists'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('putOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('errors'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('chances'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('fielding'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('passedBall'),
                      game_data['boxscore']['teams']['away']['players'][playID]['stats']['fielding'].get('pickoffs')))
    
    #insert data into SeasonFieldingStats
    #home players
    for count, value in enumerate(game_data['home_lineup']):
        playID = 'ID' + str(game_data['home_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['home']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonFieldingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['home']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('gamesStarted'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('caughtStealing'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('stolenBases'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('assists'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('putOuts'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('errors'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('chances'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('fielding'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('passedBall'),
                      game_data['boxscore']['teams']['home']['players'][playID]['seasonStats']['fielding'].get('pickoffs')))
    
    #away players
    for count, value in enumerate(game_data['away_lineup']):
        playID = 'ID' + str(game_data['away_lineup'][count])
        for count1, value1 in enumerate(game_data['boxscore']['teams']['away']['players']):
                cursor.execute('''
                    INSERT OR IGNORE INTO SeasonFieldingStats
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (game_data['scoreboard'].get('gamePk'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('id'),
                      game_data['boxscore']['teams']['away']['players'][playID]['person'].get('fullName'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('gamesStarted'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('caughtStealing'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('stolenBases'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('stolenBasePercentage'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('assists'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('putOuts'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('errors'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('chances'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('fielding'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('passedBall'),
                      game_data['boxscore']['teams']['away']['players'][playID]['seasonStats']['fielding'].get('pickoffs')))
    
    #insert data into Officials
    for count, value in enumerate(game_data['boxscore']['officials']):
        cursor.execute('''
            INSERT OR IGNORE INTO Officials
            VALUES(?, ?, ?, ?, ?)
        ''', (game_data['scoreboard'].get('gamePk'),
              game_data['boxscore']['officials'][count]['official'].get('id'),
              game_data['boxscore']['officials'][count]['official'].get('fullName'),
              game_data['boxscore']['officials'][count]['official'].get('link'),
              game_data['boxscore']['officials'][count].get('officialType')))
    
    print('Data inserted into all tables.')


    conn.commit()