public class TraitBarrelMaker : TraitCrafter
{
	public override string IdSource => "BarrelMaker";

	public override string CrafterTitle => "invMod";

	public override AnimeID IdAnimeProgress => AnimeID.Shiver;

	public override string idSoundProgress => "grind";

	public override string idSoundComplete => "grind_finish";

	public override int numIng => 2;

	public override bool StopSoundProgress => true;

	public override bool IsConsumeIng => false;

	public override bool ShouldConsumeIng(SourceRecipe.Row item, int index)
	{
		return false;
	}
}
