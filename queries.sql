--Question 1
--Which pitchers threw the most pitches in a game? How many pitches did
--they throw? How many batters did they face?

--The query below will output the top 5 pitchers by total pitches thrown in a game,
--along with the number of batters they faced in that game.

SELECT
    playerName AS pitcher_name,
    MAX(pitchesThrown) AS max_pitches_in_game,
    MAX(battersFaced) AS batters_faced
FROM GamePitchingStats
GROUP BY playerName
ORDER BY max_pitches_in_game DESC
LIMIT 5;

--Question 2
--Who are the top batters by average exit velocity on balls in play, split by
--both pitcher handedness and batter handedness? What is their average
--exit velocity? How many balls in play did they have?

--The query below will output the top 3 batters by average exit velocity for each
--combination of pitcher and batter handedness on balls in play. It also outputs
--how many balls in play each player had.

WITH RankedBatters AS (
    SELECT
        batter_name,
        stand AS batter_handedness,
        p_throws AS pitcher_handedness,
        AVG(hit_speed) AS avg_exit_velocity,
        SUM(CASE WHEN call = 'X' THEN 1 ELSE 0 END) AS balls_in_play,
        ROW_NUMBER() OVER (PARTITION BY stand, p_throws ORDER BY AVG(hit_speed) DESC) AS row_num
    FROM Pitch
    GROUP BY batter_name, stand, p_throws
)
SELECT
    batter_name,
    batter_handedness,
    pitcher_handedness,
    avg_exit_velocity,
    balls_in_play
FROM RankedBatters
WHERE row_num <= 3
ORDER BY batter_handedness, pitcher_handedness, avg_exit_velocity DESC;

--Question 3
--What are the average pitch speed, spin rate, horizontal break, and induced
-- break for each pitch type?

--The query below will output the average pitch speed, spin rate, horizontal break,
--and induced vertical break for each pitch type.

SELECT
    pitch_type,
    pitch_name,
    AVG(start_speed) AS avg_pitch_speed,
    AVG(spin_rate) AS avg_spin_rate,
    AVG(breakX) AS avg_horizontal_break,
    AVG(inducedBreakZ) AS avg_induced_vertical_break
FROM Pitch
GROUP BY pitch_type, pitch_name;