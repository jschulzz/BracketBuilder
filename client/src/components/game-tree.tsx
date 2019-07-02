import React from "react";
import { Game } from "../types/types";
import TeamCard from "./team-card";

export const GameTree = ({ game }: gameTreeProps) => {
  console.log(game);
  return (
    // <div>{game.winner.name}</div>
    <React.Fragment>
    
      {game.winner.parent_match && <GameTree game={game.winner.parent_match} />}
      <TeamCard team={game.winner} />
      {game.loser.parent_match && <GameTree game={game.loser.parent_match} />}
    </React.Fragment>
  );
};

interface gameTreeProps {
  game: Game;
}
