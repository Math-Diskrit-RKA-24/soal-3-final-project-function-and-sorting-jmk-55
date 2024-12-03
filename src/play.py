import random

PlayerList = []

def initPlayers():
    """Inisialisasi daftar pemain."""
    global PlayerList
    PlayerList = []

def createNewPlayer(name, damage=0, defensePower=0):
    """Membuat pemain baru."""
    return {
        "name": name,
        "score": 0,
        "damage": damage,
        "health": 100,
        "defensePower": defensePower,
        "defense": False,
        "ability": None,
        "skipTurn": False  # Untuk ability Mind Manipulation
    }

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
    ability = attacker.get("ability")
    if ability == "Instant Kill":
        print(f"{attacker['name']} menggunakan Instant Kill!")
        setPlayer(target, "health", 0)
    elif ability == "Deathless Gambling":
        damage = random.randint(10, 100)
        print(f"{attacker['name']} menggunakan Deathless Gambling! Damage: {damage}")
        setPlayer(attacker, "damage", damage)
    else:
        if target["defense"]:
            damage = max(0, attacker["damage"] - target["defensePower"])
            setPlayer(target, 'defense', False)
        else:
            damage = attacker["damage"]
        new_health = max(0, target["health"] - damage)
        setPlayer(target, "health", new_health)

    setPlayer(attacker, "score", attacker["score"] + 1)

def displayMatchResult():
    """Menampilkan hasil pertandingan."""
    global PlayerList
    sorted_players = sorted(PlayerList, key=lambda x: (-x["score"], -x["health"]))
    for rank, player in enumerate(sorted_players, start=1):
        print(f"Rank {rank}: {player['name']} | Score: {player['score']} | Health: {player['health']} | Ability: {player['ability']}")
    return sorted_players

def inputPlayers():
    """Input pemain dengan nama, damage, dan defensePower."""
    num_players = int(input("Masukkan jumlah pemain: "))
    for i in range(num_players):
        name = input(f"Masukkan nama pemain ke-{i+1}: ")
        damage = int(input(f"Masukkan damage untuk {name}: "))
        defense_power = int(input(f"Masukkan defense power untuk {name}: "))
        player = createNewPlayer(name, damage, defense_power)
        addPlayer(player)

def assignAbility(player):
    """Memberikan ability acak kepada pemain."""
    abilities = ["Instant Kill", "Deathless Gambling", "God of life"]
    chosen_ability = random.choice(abilities)
    setPlayer(player, "ability", chosen_ability)
    if chosen_ability == "God of life":
        setPlayer(player, "health", 100)
        print(f"{player['name']} mendapatkan ability God of life! Health dipulihkan ke 100.")
    else:
        print(f"{player['name']} mendapatkan ability {chosen_ability}!")

def playerAction(player):
    """Memilih tindakan untuk pemain."""
    if player.get("skipTurn"):
        print(f"{player['name']} terkena Mind Manipulation dan tidak bisa bertindak!")
        setPlayer(player, "skipTurn", False)
        return

    action = input(f"\n{player['name']} (Health: {player['health']}, Score: {player['score']}): Pilih aksi (1: Attack, 2: Defense): ").strip()
    if action == "1":  # Serangan
        target_names = [p["name"] for p in PlayerList if p != player]
        if not target_names:
            print("Tidak ada target yang tersedia untuk diserang.")
            return
        print(f"Daftar target: {', '.join(target_names)}")
        target_name = input("Pilih target untuk diserang: ").strip()
        target = next((p for p in PlayerList if p["name"] == target_name), None)
        if target:
            print(f"{player['name']} menyerang {target['name']}!")
            attackPlayer(player, target)
            if target["health"] <= 0:
                print(f"{target['name']} telah kalah!")
                removePlayer(target["name"])
        else:
            print("Target tidak valid!")
    elif action == "2":  # Bertahan
        setPlayer(player, "defense", True)
        print(f"{player['name']} memilih bertahan.")
    else:
        print("Aksi tidak valid. Lewat giliran.")

def runRounds(rounds):
    """Menjalankan permainan dalam jumlah ronde tertentu."""
    for round_num in range(1, rounds + 1):
        if len(PlayerList) <= 1:
            break
        print(f"\n=== Ronde {round_num} ===")
        for player in PlayerList[:]: 
            if len(PlayerList) <= 1:
                break
            playerAction(player)

        print("\nStatus Pemain setelah ronde:")
        ranked_players = displayMatchResult()

        last_player = ranked_players[-1]
        assignAbility(last_player)

    if len(PlayerList) == 1:
        winner = PlayerList[0]
        print(f"\nPemenang adalah {winner['name']} dengan skor {winner['score']} dan kesehatan {winner['health']}!")
    else:
        print("\nPermainan selesai tanpa pemenang karena tidak ada aksi yang signifikan.")

if __name__ == "__main__":
    initPlayers()
    inputPlayers()
    total_rounds = int(input("Masukkan jumlah ronde: "))
    runRounds(total_rounds)