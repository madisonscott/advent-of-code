const fs = require('fs');
const path = require('path');

function structurePassport(unstructuredPassport) {
    let fields = unstructuredPassport.replace(/\n/g, ' ').split(' ');
    let passport = {}

    fields.forEach((field) => {
        let keyValue = field.split(':');
        let key = keyValue[0];
        let value = keyValue[1];

        passport[key] = value;
    });

    return passport;
}

function parsePassportsFromInput(input) {
    let unstructuredPassports = input.split('\n\n');

    let passports = [];
    unstructuredPassports.forEach((unstructured) => {
        passports.push(structurePassport(unstructured));
    });

    return passports;
}

function isPassportValid_Part1(passport) {
    let requiredFields = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    ];

    for (const field of requiredFields) {
        if (!passport[field]) {
            return false;
        }
    }

    return true;
}

const yearRegex = /^\d{4}$/;
const heightRegex = /^(\d+)(cm|in)$/;

function isPassportValid_Part2(passport) {
    // On the fourth day of Christmas, no shits were given.
    let requirements = [
        { field: 'byr', regex: yearRegex, isValid: (val) => 1920 <= val && val <= 2002 },
        { field: 'iyr', regex: yearRegex, isValid: (val) => 2010 <= val && val <= 2020 },
        { field: 'eyr', regex: yearRegex, isValid: (val) => 2020 <= val && val <= 2030 },
        {
            field: 'hgt',
            regex: heightRegex,
            isValid: (val) => {
                let matches = val.match(heightRegex);
                let height = matches[1];
                let unit = matches[2];

                return (unit == 'cm' && 150 <= height && height <= 193)
                    || (unit == 'in' && 59 <= height && height <= 76);
            },
        },
        { field: 'hcl', regex: /^\#[0-9a-f]{6}$/ },
        { field: 'ecl', regex: /^amb|blu|brn|gry|grn|hzl|oth$/ },
        { field: 'pid', regex: /^\d{9}$/ },
    ];

    for (const requirement of requirements) {
        let { field, regex, isValid } = requirement;

        let value = passport[field];
        if (!value || !value.match(regex)) {
            return false;
        }

        if (!!isValid && !isValid(value)) {
            return false;
        }
    }

    return true;
}

function solvePuzzle(input, validator) {
    let passports = parsePassportsFromInput(input);
    
    let validPassports = 0;
    passports.forEach((passport) => {
        if (validator(passport)) {
            validPassports++;
        }
    });

    return validPassports;
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

    console.log(solvePuzzle(input, isPassportValid_Part1));
    console.log(solvePuzzle(input, isPassportValid_Part2));
}

if (require.main === module) {
    main();
}
