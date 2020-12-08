const fs = require('fs');
const path = require('path');

function parseBagRulesFromInput(input) {
    let ruleRegex = /^(\w+ \w+) bags contain (.*)\.$/;
    let innerBagRegex = /(\d+) (\w+ \w+) bags*/g;

    let bagsToInnerBags = {};
    for (const line of input.split('\n')) {
        let [_, outerBag, unparsedInnerBags] = line.match(ruleRegex);

        let innerBags = {};
        while (innerBagMatch = innerBagRegex.exec(unparsedInnerBags)) {
            let [_, quantity, color] = innerBagMatch;
            innerBags[color] = quantity;
        }

        bagsToInnerBags[outerBag] = innerBags;
    }

    return bagsToInnerBags;
}

function mapBagsToDirectContainers(bagRules) {
    let bagsToContainers = {};
    for (const [outerColor, innerBags] of Object.entries(bagRules)) {
        for (const color of Object.keys(innerBags)) {
            addToLookup(bagsToContainers, color, outerColor);
        }
    }

    return bagsToContainers;
}

function addToLookup(lookup, key, value) {
    if (!!lookup[key]) {
        lookup[key].push(value);
    } else {
        lookup[key] = [value];
    }
}

function findContainingBags(bag, bagsToDirectContainers, allContainers) {
    let directContainers = bagsToDirectContainers[bag];
    if (!directContainers) {
        return;
    }

    for (const container of directContainers) {
        if (allContainers.has(container)) {
            continue;
        }

        allContainers.add(container);
        findContainingBags(container, bagsToDirectContainers, allContainers);
    }
}

function findNumberOfContainingBags(bagRules, color) {
    let bagsToDirectContainers = mapBagsToDirectContainers(bagRules);
    let results = new Set();
    findContainingBags(color, bagsToDirectContainers, results);
    return results.size;
}

function findNumberOfContainedBags(bagRules, color) {
    let containedBags = bagRules[color];
    let containedBagsCount = 0;
    
    for (const [containedColor, count] of Object.entries(containedBags)) {
        containedBagsCount +=
            count * (findNumberOfContainedBags(bagRules, containedColor) + 1);
    }

    return containedBagsCount;
}

function main() {
    let inputFileName = `${path.basename(__filename, '.js')}.txt`;
    let inputFilePath = path.join('input', inputFileName);

    let input = '';

    try {
        input = fs.readFileSync(inputFilePath, 'utf8')
    } catch (err) {
        console.error(err)
        return;
    }

    let bagRules = parseBagRulesFromInput(input);
    let shinyGold = 'shiny gold';

    console.log(findNumberOfContainingBags(bagRules, shinyGold));
    console.log(findNumberOfContainedBags(bagRules, shinyGold));
}

if (require.main === module) {
    main();
}



