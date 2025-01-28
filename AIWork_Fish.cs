public class AIWork_Fish : AIWork
{
	public override int destDist => 1;

	public override bool FuncWorkPoint(Point p)
	{
		return p.IsWater;
	}

	public override AIAct GetWork(Point p)
	{
		return new AI_Fish
		{
			pos = p.Copy()
		};
	}
}
