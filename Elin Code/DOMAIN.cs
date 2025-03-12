using UnityEngine;

public class DOMAIN
{
	public const int domEarth = 812;

	public const int domHealing = 811;

	public const int domEyth = 814;

	public const int domOblivion = 813;

	public const int domTest = 800;

	public const int domElement = 806;

	public const int domFaith = 802;

	public const int domLuck = 810;

	public const int domMachine = 809;

	public const int domHarvest = 808;

	public const int domWind = 807;

	public const int domComm = 805;

	public const int domArcane = 804;

	public const int domMiracle = 803;

	public const int domHarmony = 815;

	public const int domSurvival = 801;

	public static readonly int[] IDS = new int[16]
	{
		812, 811, 814, 813, 800, 806, 802, 810, 809, 808,
		807, 805, 804, 803, 815, 801
	};
}
public class Domain : EClass
{
	public SourceElement.Row source;

	public Sprite GetSprite()
	{
		string text = source.alias.Remove(0, 3).ToLower();
		return ResourceCache.Load<Sprite>("Media/Graphics/Image/Faction/" + text);
	}
}
