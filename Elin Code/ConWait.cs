public class ConWait : Condition
{
	public override bool ConsumeTurn => true;

	public override bool CancelAI => false;

	public override bool WillOverride => true;

	public override int GetPhase()
	{
		return 0;
	}
}
