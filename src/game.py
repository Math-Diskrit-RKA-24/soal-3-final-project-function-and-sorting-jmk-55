PlayerList = []
def initPlayers():
    global PlayerList
    PlayerList = []
def createNewPlayer(name, damage=0, defensePower=0):
    return {"name": name,"score": 0,"damage": damage,"health": 100,"defensePower": defensePower,"defense": False}
def addPlayer(player):
    """Menambahkan pemain ke daftar PlayerList."""
    global PlayerList
    PlayerList.append(player)
def removePlayer(name):
    """Menghapus pemain berdasarkan nama."""
    global PlayerList
    for player in PlayerList:
        if player["name"] == name:
            PlayerList.remove(player)
            return
    print("There is no player with that name!")
def setPlayer(player, key, value):
    """Memperbarui nilai atribut tertentu pada pemain."""
    if key in player:
        player[key] = value
    else:
        print(f"Key '{key}' tidak ditemukan dalam pemain!")
def attackPlayer(attacker, target):
    """Melakukan serangan dari attacker ke target."""
    if target["defense"]:
        damage = max(0, attacker["damage"] - target["defensePower"])
        setPlayer(target, 'defense', False)
        score = 0.8
    else:
        damage = attacker["damage"]
        score = 1
    new_health = target["health"] - damage
    setPlayer(target, "health", new_health)
    setPlayer(attacker, "score", attacker["score"] + score)
def displayMatchResult():
    """Menampilkan hasil pertandingan."""
    global PlayerList
    sorted_players = sorted(PlayerList, key=lambda x: (-x["score"], -x["health"]))
    for rank, player in enumerate(sorted_players, start=1):
        print(f"Rank {rank}: {player['name']} | Score: {player['score']} | Health: {player['health']}")