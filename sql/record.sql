SELECT
        blb_season.name, wins.loc, wins.nick, wins.n, losses.n
FROM (
        SELECT
                blb_team.location as loc, blb_team.nickname as nick, blb_team.id as id, blb_game.season_id as sid, count(*) as n
        FROM
                blb_game, blb_team
        WHERE
                ((blb_game.home_team_id == blb_team.id AND blb_game.home_team_runs > blb_game.away_team_runs) OR
                (blb_game.away_team_id == blb_team.id AND blb_game.away_team_runs > blb_game.home_team_runs))
        GROUP BY
              blb_team.id
     ) wins,
     (
        SELECT
                blb_team.location as loc, blb_team.nickname as nick, blb_team.id as id, blb_game.season_id as sid, count(*) as n
        FROM
                blb_game, blb_team
        WHERE
                ((blb_game.home_team_id == blb_team.id AND blb_game.home_team_runs < blb_game.away_team_runs) OR
                (blb_game.away_team_id == blb_team.id AND blb_game.away_team_runs < blb_game.home_team_runs))
        GROUP BY
              blb_team.id
          
     ) losses,
     blb_season
WHERE
        wins.id == losses.id AND wins.sid == blb_season.id
ORDER BY
      wins.sid,
      losses.n
;
