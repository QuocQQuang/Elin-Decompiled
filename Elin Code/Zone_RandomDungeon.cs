public class Zone_RandomDungeon : Zone_Dungeon
{
	public override bool AlwaysLowblock => true;

	public override bool IsNefia => true;

	public override bool AddPrefix => true;

	public override bool LockExit => false;

	public override int MinLv => LvBoss;

	public override bool ScaleMonsterLevel
	{
		get
		{
			if (!EClass.player.flags.KilledBossInVoid || DangerLv < 50)
			{
				return DangerLv >= 200;
			}
			return true;
		}
	}

	public override string IDPlayList
	{
		get
		{
			if (base.lv != LvBoss)
			{
				return base.IDPlayList;
			}
			return "Dungeon_Boss";
		}
	}

	public virtual int LvBoss
	{
		get
		{
			Rand.SetSeed(GetTopZone().uid);
			int result = -2 - EClass.rnd(4);
			Rand.SetSeed();
			return result;
		}
	}

	public override string TextWidgetDate
	{
		get
		{
			if (base.Boss == null)
			{
				return "";
			}
			return "bossLevel".lang(base.Boss.Name);
		}
	}

	public override void OnGenerateMap()
	{
		if (base.lv == LvBoss)
		{
			base.Boss = SpawnMob(null, SpawnSetting.Boss(DangerLv, DangerLv));
			Chara boss = base.Boss;
			Hostility hostility2 = (base.Boss.c_originalHostility = Hostility.Enemy);
			boss.hostility = hostility2;
			foreach (Chara chara in EClass._map.charas)
			{
				if (chara.IsHostile())
				{
					chara.enemy = EClass.pc.party.members.RandomItem();
				}
			}
		}
		base.OnGenerateMap();
	}
}
