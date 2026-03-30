[
  {
    "name": "__imported_at__",
    "mode": "NULLABLE",
    "type": "TIMESTAMP",
    "description": "",
    "fields": []
  },
  {
    "name": "_class",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "_id",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "assets",
    "mode": "REPEATED",
    "type": "RECORD",
    "description": "Data only available from 2026-02-28 onwards",
    "fields": [
      {
        "name": "url",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "type",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      }
    ]
  },
  {
    "name": "category",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "Values: positive, negative, cheat",
    "fields": []
  },
  {
    "name": "comment",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "competition",
    "mode": "NULLABLE",
    "type": "RECORD",
    "description": "",
    "fields": [
      {
        "name": "_id",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "type",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      }
    ]
  },
  {
    "name": "createdAt",
    "mode": "NULLABLE",
    "type": "TIMESTAMP",
    "description": "",
    "fields": []
  },
  {
    "name": "deltaFbi",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "",
    "fields": []
  },
  {
    "name": "faction1elo",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "",
    "fields": []
  },
  {
    "name": "faction1score",
    "mode": "NULLABLE",
    "type": "FLOAT",
    "description": "",
    "fields": []
  },
  {
    "name": "faction2elo",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "",
    "fields": []
  },
  {
    "name": "faction2score",
    "mode": "NULLABLE",
    "type": "FLOAT",
    "description": "",
    "fields": []
  },
  {
    "name": "game",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "gameData",
    "mode": "NULLABLE",
    "type": "RECORD",
    "description": "Data only available from 2026-02-28 onwards",
    "fields": [
      {
        "name": "rounds",
        "mode": "REPEATED",
        "type": "INTEGER",
        "description": "",
        "fields": []
      }
    ]
  },
  {
    "name": "matchId",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "matchType",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "organizerId",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "players",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "",
    "fields": []
  },
  {
    "name": "region",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "reportedUser",
    "mode": "NULLABLE",
    "type": "RECORD",
    "description": "",
    "fields": [
      {
        "name": "birthYear",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "country",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "elo",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "enemyComposition",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "membershipType",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "memberships",
        "mode": "REPEATED",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "opportunities",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "opportunitiesTm",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "teamComposition",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "teammate",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": []
      },
      {
        "name": "userId",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "won",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": []
      }
    ]
  },
  {
    "name": "reportedUserId",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "",
    "fields": []
  },
  {
    "name": "reporterUser",
    "mode": "NULLABLE",
    "type": "RECORD",
    "description": "",
    "fields": [
      {
        "name": "birthYear",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "country",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "elo",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "enemyComposition",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "membershipType",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "memberships",
        "mode": "REPEATED",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "opportunities",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "opportunitiesTm",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "",
        "fields": []
      },
      {
        "name": "teamComposition",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "teammate",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": []
      },
      {
        "name": "userId",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "",
        "fields": []
      },
      {
        "name": "won",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": []
      }
    ]
  },
  {
    "name": "smurfAccounts",
    "mode": "REPEATED",
    "type": "STRING",
    "description": "Data only available from 2026-02-28 onwards",
    "fields": []
  },
  {
    "name": "subCategory",
    "mode": "NULLABLE",
    "type": "STRING",
    "description": "Values: toxic, smurfing, griefing, cheating",
    "fields": []
  },
  {
    "name": "toxicityTypes",
    "mode": "REPEATED",
    "type": "STRING",
    "description": "Values: chat, voice. Data only available from 2026-02-28 onwards",
    "fields": []
  },
  {
    "name": "updatedAt",
    "mode": "NULLABLE",
    "type": "TIMESTAMP",
    "description": "",
    "fields": []
  },
  {
    "name": "version",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "",
    "fields": []
  },
  {
    "name": "urls",
    "mode": "REPEATED",
    "type": "STRING",
    "description": "Data only available from 2026-02-28 onwards",
    "fields": []
  }
]