public class CardBlueprint
{
	public int lv = -999;

	public int qualityBonus;

	public string idRace;

	public string idJob;

	public string idEle;

	public Rarity rarity = Rarity.Random;

	public BlessedState? blesstedState;

	public bool fixedMat;

	public bool tryLevelMatTier;

	public bool fixedQuality;

	public static CardBlueprint current;

	public static CardBlueprint _Default = new CardBlueprint();

	public static CardBlueprint CharaGenEQ = new CardBlueprint
	{
		tryLevelMatTier = true
	};

	public static CardBlueprint DebugEQ = new CardBlueprint
	{
		rarity = Rarity.Legendary
	};

	public static CardBlueprint Chara(int lv, Rarity rarity = Rarity.Normal)
	{
		return new CardBlueprint
		{
			rarity = rarity,
			lv = lv
		};
	}

	public static void Set(CardBlueprint _bp)
	{
		current = _bp;
	}

	public static void SetNormalRarity(bool fixedMat = false)
	{
		Set(new CardBlueprint
		{
			rarity = Rarity.Normal,
			fixedMat = fixedMat
		});
	}

	public static void SetRarity(Rarity q = Rarity.Normal)
	{
		Set(new CardBlueprint
		{
			rarity = q
		});
	}
}
