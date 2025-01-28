using System.Collections.Generic;
using System.Linq;

public class TaskCullLife : Task
{
	public Point dest;

	public static bool CanCull(Card c)
	{
		if (c.c_minionType == MinionType.Friend)
		{
			return !c.IsPCFaction;
		}
		return false;
	}

	public override bool CanPerform()
	{
		return Act.TP.FindChara((Chara c) => CanCull(c)) != null;
	}

	public override bool CanManualCancel()
	{
		return true;
	}

	public override IEnumerable<Status> Run()
	{
		while (true)
		{
			Chara target = GetTarget();
			if (dest != null)
			{
				target = dest.FindChara((Chara c) => CanCull(c));
				dest = null;
			}
			if (target == null)
			{
				yield return Success();
			}
			bool fail = false;
			yield return DoGoto(target, delegate
			{
				fail = true;
				return Status.Running;
			});
			if (!fail && target.IsAliveInCurrentZone)
			{
				if (owner.Dist(target) > 1)
				{
					yield return Cancel();
				}
				owner.PlaySound("shear");
				Msg.Say("cull_life", EClass.pc, target);
				target.Die();
				Thing t = ThingGen.Create("ecopo").SetNum(EClass.rndHalf(target.LV / 10 + 6));
				EClass.pc.Pick(t);
				yield return KeepRunning();
			}
		}
	}

	public static Chara GetTarget()
	{
		List<Chara> list = new List<Chara>();
		foreach (Chara chara in EClass._map.charas)
		{
			if (CanCull(chara))
			{
				list.Add(chara);
			}
		}
		if (list.Count == 0)
		{
			return null;
		}
		list.Sort((Chara a, Chara b) => EClass.pc.Dist(a) - EClass.pc.Dist(b));
		return list.First();
	}
}
