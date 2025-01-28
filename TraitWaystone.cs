public class TraitWaystone : Trait
{
	public bool IsTemp => owner.id == "waystone_temp";

	public override bool CanUse(Chara c)
	{
		return IsTemp;
	}

	public override bool OnUse(Chara c)
	{
		owner.ModNum(-1);
		EClass.pc.MoveZone(EClass._zone.ParentZone);
		return false;
	}

	public override void TrySetAct(ActPlan p)
	{
		if (!EClass._zone.parent.IsRegion || (EClass._zone.IsInstance && !EClass._zone.IsUserZone) || EClass._zone is Zone_Dungeon || EClass._zone is Zone_Tent)
		{
			return;
		}
		p.TrySetAct("actNewZone", delegate
		{
			if (IsTemp)
			{
				owner.ModNum(-1);
			}
			EClass.pc.MoveZone(EClass._zone.ParentZone);
			return false;
		}, owner, CursorSystem.MoveZone);
		if (!EClass._zone.IsPCFaction && !EClass._zone.IsTown)
		{
			return;
		}
		if (EClass.player.spawnZone != EClass._zone)
		{
			p.TrySetAct("actSetSpawn", delegate
			{
				Effect.Get("aura_heaven").Play(EClass.pc.pos);
				EClass.Sound.Play("worship");
				EClass.player.spawnZone = EClass._zone;
				Msg.Say("setSpawn", owner);
				return true;
			}, owner);
		}
		else if (EClass.player.spawnZone != EClass.pc.homeZone || EClass._zone != EClass.pc.homeZone)
		{
			p.TrySetAct("actUnsetSpawn", delegate
			{
				EClass.Sound.Play("trash");
				EClass.player.spawnZone = EClass.pc.homeZone;
				Msg.Say("unsetSpawn", owner);
				return true;
			}, owner);
		}
	}
}
