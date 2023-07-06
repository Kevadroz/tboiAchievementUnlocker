#!/bin/bash
cd..

echo '<items gfxroot="gfx/items/" version="1">' > content/items.xml
echo '<ItemPools>
	<Pool Name="shellGame">' > content/itempools.xml

for i in {1..637}
do
	echo '	<passive name="KZAchievementCheckerID'$i'" achievement="'$i'" gfx="collectibles_001_thesadonion.png"/>' >> content/items.xml
	echo '		<Item Name="KZAchievementCheckerID'$i'" Weight="1" DecreaseBy="1" RemoveOn="0.1"/>' >> content/itempools.xml
done

echo '</items>' >> content/items.xml
echo '	</Pool>
</ItemPools>' >> content/itempools.xml
