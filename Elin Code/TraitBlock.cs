public class TraitBlock : TraitTile
{
	public override TileRow source => EClass.sources.blocks.rows[owner.refVal];
}
