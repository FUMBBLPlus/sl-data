import json
import pathlib

import pyfumbbl

rulesetId = 69

dump_kwargs = (
    ("ensure_ascii", False),
    ("indent", "\t"),
    ("sort_keys", True),
)

if __name__ == "__main__":
  directory = pathlib.Path(__loader__.path).parent
  for subdirname in (
      "ruleset",
      "roster",
      "position",
  ):
    (directory / subdirname).mkdir(exist_ok=True)
  ruleset_data = pyfumbbl.ruleset.get(rulesetId)
  ruleset_file = directory / "ruleset" / f'{rulesetId}.json'
  print(ruleset_file)
  with ruleset_file.open("w") as f:
    json.dump(ruleset_data, f, **dict(dump_kwargs))
  prevpositionIds = set()
  positiondir = directory / "position"
  for d_roster in ruleset_data["rosters"]:
    rosterId = d_roster["id"]
    roster_data = pyfumbbl.roster.get(rosterId)
    roster_file = directory / "roster" / f'{rosterId}.json'
    print(roster_file)
    with roster_file.open("w") as f:
      json.dump(roster_data, f, **dict(dump_kwargs))
    for d_position in (
        d
        for k in ("positions", "stars")
        for d in roster_data[k]
    ):
      positionId = d_position["id"]
      if positionId in prevpositionIds:
        continue
      position_data = pyfumbbl.position.get(positionId)
      position_file = positiondir / f'{positionId}.json'
      print(position_file)
      with position_file.open("w") as f:
        json.dump(position_data, f, **dict(dump_kwargs))
      prevpositionIds.add(positionId)
