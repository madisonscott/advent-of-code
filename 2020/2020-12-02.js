const fs = require('fs');
const path = require('path');

function parsePasswordsFromInput(input) {
    let passwords = [];
    
    let lines = input.split('\n');

    lines.forEach((line) => {
        let re = /([0-9]+)-([0-9]+)\s{1}([a-zA-Z]{1}):\s{1}([a-zA-Z]+)/;
        let matches = line.match(re);
        
        passwords.push({
            'password': matches[4],
            'requirement': {
                'letter': matches[3],
                'minimum': parseInt(matches[1]),
                'maximum': parseInt(matches[2]),
            }
        });
    });

    return passwords;
}

function isPasswordValid_Part1(passwordThing) {
    let numOccurrences = 0;
    let {requirement, password} = passwordThing;

    password.split('').forEach((char) => {
        if (char == requirement.letter) {
            numOccurrences++;
        }
    });

    return requirement.minimum <= numOccurrences && numOccurrences <= requirement.maximum;
}

function isPasswordValid_Part2(passwordThing) {
    let numOccurrences = 0;
    let {requirement, password} = passwordThing;

    if (password[requirement.minimum-1] == requirement.letter) {
        numOccurrences++;
    }

    if (password[requirement.maximum-1] == requirement.letter) {
        numOccurrences++;
    }

    return numOccurrences == 1;
}

function solve_puzzle(input, validationFunction) {
    let passwords = parsePasswordsFromInput(input);

    let numValid = 0;
    passwords.forEach((password) => {
        if (validationFunction(password)){
            numValid++;
        }
    });

    return numValid;
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

    console.log(solve_puzzle(input, isPasswordValid_Part1));
    console.log(solve_puzzle(input, isPasswordValid_Part2));
}

if (require.main === module) {
    main();
}



