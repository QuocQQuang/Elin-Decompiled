using System;

public class Goal : AIAct
{
	public override bool InformCancel => false;

	public Goal Duplicate()
	{
		return Activator.CreateInstance(GetType()) as Goal;
	}
}
