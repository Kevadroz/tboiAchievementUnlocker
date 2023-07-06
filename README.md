# This mod allows you to check what is unlocked with ease!

As many modders know, Isaacs Mod API does not have a way to check whether any achievement, character, collectible, etc. is unlocked or not. This library allows you to do just that.

## The API
First, all functions are located in `KZLibs.AchievementChecker` so you may create a local variable pointing to that.

Most functions use one of the game's mod API ENUMS as it's only parameter.

Using any invalid (outside of range) value as a parameter will return `nil`.

## Achievements
You can chack whether any of the 637 achievements are unlocked using `isAchievementUnlocked(<num>)`, where the parameter is the [numerical id](https://antifandom.com/bindingofisaacrebirth/wiki/The_Binding_of_Isaac:_Rebirth) of the achievements.

## Collectibles
To check for collectible items, use `isCollectibleUnlocked(<CollectibleType>)`.

## Players (Characters)
Use `isPlayerUnlocked(<PlayerType>)`.

## Trinkets
Use `isTrinketUnlocked(<TrinketType>)`.

## Cards (and runes)
Use `isPlayerUnlocked(<Card>)`.

## Pill Effect
Use `isPlayerUnlocked(<PillEffect>)`.
